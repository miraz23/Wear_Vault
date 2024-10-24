from django.contrib import admin
from shop.models import Products, Orders, OrderUpdate

admin.site.register(Products)
admin.site.register(Orders)
admin.site.register(OrderUpdate)

# Register your models here.
