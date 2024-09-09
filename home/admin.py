from django.contrib import admin

# Register your models here.
from . models import *

admin.site.register(Product)
admin.site.register(Color)
admin.site.register(Material)
admin.site.register(Occasion)
admin.site.register(Supplier)
admin.site.register(Admin_login)
admin.site.register(Orders)
admin.site.register(cart)
admin.site.register(CartProduct)
admin.site.register(Coupon)
admin.site.register(user_details)