from django.urls import path
from .views import *

urlpatterns = [
    path('',Products.as_view(),name = 'products'),

    path('addtocart/<int:pk>',AddToCartView.as_view(),name="addtocart"),

    path('removeformcart/<int:pk>',RemoveItemFormCart.as_view(),name="removeformcart"),

    path('myaddress',MyAddress.as_view(),name='myaddress'),

    path('checkout/<int:pk>',Checkout.as_view(),name="checkout"),

    path('checkoutbynewaddress',CheckoutByNewAddress.as_view(),name='checkoutbynewaddress'),

    path('payment',PaymentView.as_view(),name='payment'),

    path('mycart',MyCart.as_view(),name='mycart'),

]
