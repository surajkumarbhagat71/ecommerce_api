from rest_framework import serializers
from .models import *



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Product
        fields = '__all__'


class AddTocartSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddToCart
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Address
        fields = '__all__'



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'



class PaymentSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
