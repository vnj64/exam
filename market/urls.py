from django.urls import path

from .views import MarketListView, CartView, AddCart, DeleteCartItem, Payout, TopProductsListView

urlpatterns = [
    path('', MarketListView.as_view(), name='home'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add_cart/<int:pk>', AddCart.as_view(), name='add_cart'),
    path('delete_cart/<int:pk>', DeleteCartItem.as_view(), name='delete_cart'),
    path('payout/', Payout.as_view(), name='payout'),
    path('top_products/', TopProductsListView.as_view(), name='top_products'),
]