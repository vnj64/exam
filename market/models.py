from django.contrib.auth.models import User
from django.db import models


class Store(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=120)
    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.store}'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_created=True, auto_now=True)

    def add_item(self, product, quantity, price):
        item = CartItem.objects.create(
            cart=self,
            product=product,
            quantity=quantity,
            price=price
        )
        return item

    def total_price(self):
        return sum(item.price * item.quantity for item in self.cartitem_set.all())

    def __str__(self):
        return f'{self.user} Cart'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.cart} - {self.product}'


class TopProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.product} - {self.count}'
