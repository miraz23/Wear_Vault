from django.contrib import admin
from shop.models import product, order, orderUpdate

admin.site.register(product)
admin.site.register(order)
admin.site.register(orderUpdate)

# Register your models here.
