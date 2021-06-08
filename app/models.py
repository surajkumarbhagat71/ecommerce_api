from django.db import models
from django.contrib.auth.models import User
from django.conf import settings



class Product(models.Model):
    pro_id  = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    brand   = models.CharField(max_length=200)
    price = models.IntegerField()
    dis_price = models.IntegerField()
    image = models.ImageField(upload_to='media/')


    def __str__(self):
        return self.name

    def product_price(self):
        return self.price


    def pro_discount_price(self):
        return self.price - self.dis_price



class AddToCart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pro_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    dateTime  = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    qty  = models.IntegerField(default=1)


    def total_price(self):
        return self.qty * self.pro_id.price



    def discount_price(self):
        dis_price = (self.total_price() * self.pro_id.dis_price)/100
        return dis_price


    def final_price(self):
        if self.pro_id.dis_price:
            return self.discount_price()
        else:
            return self.total_price()


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    contact = models.IntegerField()
    email = models.EmailField(null=True,blank=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    pin_code = models.CharField(max_length=200)
    landmark = models.CharField(max_length=200)
    alternative_no = models.IntegerField(null=True,blank=True)


    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items = models.ManyToManyField(AddToCart)
    ordered = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(Address,on_delete=models.CASCADE, null=True ,blank=True)


    def __str__(self):
        return self.address.name


    def get_total_price(self):
        total = 0
        for foo in self.items.all():
            total += foo.final_price()

        return total



class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE)
    amount = models.IntegerField()
    ordered  = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True)






