from django.db import models
from django.contrib.auth.models import User

class Material(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Occasion(models.Model):
    name = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to='occasion/',null=True, blank=True)

    def __str__(self):
        return self.name
    
class Admin_login(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20, unique=True)

class Supplier(models.Model):
    name = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    def __str__(self):
        return self.name


class Product(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    occasion = models.ForeignKey(Occasion, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='images/',null=True, blank=True)
    stock=models.IntegerField(default=0)
    supplier=models.ForeignKey(Supplier,on_delete=models.CASCADE,null=True)
    stockrequest = models.BooleanField(default=False)
    
   
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name if self.name else 'Unnamed Product'
    



class cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)



class CartProduct(models.Model):
    cart = models.ForeignKey(cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    size=models.CharField(max_length=20)

    def __str__(self):
        return "cart:" + str(self.cart.id) + "cartproduct:" + str(self.id)


ORDER_STATUS = (
    ("order recived", "order recived"),
    ("order processing", "order processing"),
    ("order on the way", "order on the way"),
    ("order completed", "order completed"),
    ("order cancelled", "order cancelled")
)


class Orders(models.Model):
    cart = models.ForeignKey(cart, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=100,default="ssss")
    mobile  =models.CharField(max_length=50, default="45678")

    def __str__(self):
        return "order:" + str(self.id)
    

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.PositiveIntegerField(default=0)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return self.code


class user_details(models.Model):
    forget_password_token = models.CharField(max_length=100,null=True)
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
