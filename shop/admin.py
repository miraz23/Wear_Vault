from django.contrib import admin
from shop.models import product, order, orderUpdate

admin.site.register(product)
admin.site.register(orderUpdate)

class orderAdmin(admin.ModelAdmin):
    list_display = ('email', 'formatted_items')
    readonly_fields = ('formatted_items',)

admin.site.register(order, orderAdmin)

# Register your models here.
