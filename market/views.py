from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView

from accounts.models import Profile, Transaction
from .models import Product, Cart, CartItem, TopProducts


class MarketListView(View):
    template_name = 'market/home.html'

    def get(self, request, *args, **kwargs):
        queryset = Product.objects.filter(quantity__gt=0).all()
        data = {'products': queryset if queryset else []}
        return render(request, self.template_name, data)


class TopProductsListView(ListView):
    model = TopProducts
    template_name = 'market/top_products.html'
    queryset = TopProducts.objects.all().order_by('-count')

    def get_context_data(self, *, object_list=None, **kwargs):
        return {'top_products': self.queryset if self.queryset else []}


class CartView(DetailView):
    model = Cart
    template_name = 'market/cart.html'

    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart).all()
        total_price = cart.total_price()
        return render(request, self.template_name, {'cart_items': cart_items, 'total_price': total_price})


class AddCart(View):

    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        product_id = kwargs.get('pk')
        product = Product.objects.get(pk=product_id)
        cart = Cart.objects.get(user=user)
        if cart:
            try:
                item = CartItem.objects.get(cart=cart, product=product)
                item.quantity += 1
                item.save()
            except:
                cart.add_item(product, 1, product.price)
                cart.save()
        else:
            cart = Cart.objects.create(user=user)
            cart.add_item(product, 1, product.price)
            cart.save()
        return redirect(reverse('market:home'))


class DeleteCartItem(View):

    def get(self, request, *args, **kwargs):
        cart_item_id = kwargs.get('pk')
        cart_item = CartItem.objects.get(pk=cart_item_id)
        if cart_item.quantity == 1:
            cart_item.delete()
            return redirect(reverse('market:cart'))

        cart_item.quantity -= 1
        cart_item.save()

        return redirect(reverse('market:cart'))


class Payout(View):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart).all()
        profile = Profile.objects.get(user=user)
        user_balance = profile.balance
        cart_price = cart.total_price()
        if user_balance >= cart_price:
            for cart_item in cart_items:
                product = Product.objects.filter(pk=cart_item.product.pk).first()
                product.quantity -= cart_item.quantity
                product.save()
                try:
                    top_product = TopProducts.objects.get(product=product)
                    top_product.count += cart_item.quantity
                    top_product.save()
                except:
                    TopProducts.objects.create(product=product, count=cart_item.quantity)

            profile.balance -= cart_price
            profile.save()
            cart.delete()
            Cart.objects.create(user=user)
            Transaction.objects.create(user=user, transaction=cart_price)

            transactions = Transaction.objects.filter(user=user).all()
            sum_transactions = sum([trans.transaction for trans in transactions])
            profile = Profile.objects.get(user=user)
            if 1000 <= sum_transactions < 5000:
                profile.status = 'silver'
                print('silver')
            elif sum_transactions >= 5000:
                profile.status = 'gold'
                print('gold')
            profile.save()
            return redirect(reverse('market:cart'))
        else:
            cart_items = CartItem.objects.filter(cart=cart).all()
            return render(request, 'market/cart.html',
                          {'cart_items': cart_items, 'total_price': cart.total_price(), 'message': 'Not enough money'})
