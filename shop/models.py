from django.db import models
from django.utils.html import format_html
import json

# Create your models here.

class product(models.Model):
    CATEGORY_CHOICES = [
        ('drop-shoulders', 'Drop Shoulders'),
        ('baggy-joggers', 'Baggy Joggers'),
        ('baggy-shirts', 'Baggy Shirts'),
        ('cargo-pants', 'Cargo Pants'),
        ('head-wear', 'Head Wear'),
        ('baggy-shorts', 'Baggy Shorts'),
    ]
    
    LATEST_ARRIVAL_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    product_id = models.AutoField
    product_name = models.CharField(max_length=100)
    product_category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='drop-shoulders')
    product_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    product_desc = models.TextField()
    product_color = models.TextField()
    product_size = models.TextField()
    product_image_1 = models.ImageField(upload_to='images')
    product_image_2 = models.ImageField(upload_to='images')
    product_image_3 = models.ImageField(upload_to='images')
    product_image_4 = models.ImageField(upload_to='images')
    product_image_5 = models.ImageField(upload_to='images')
    latest_arrival = models.CharField(max_length=3, choices=LATEST_ARRIVAL_CHOICES, default='no')

    def __str__(self):
        return self.product_name


class order(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json =  models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=90)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    oid=models.CharField(max_length=150,blank=True)
    amountpaid=models.CharField(max_length=500,blank=True,null=True)
    paymentstatus=models.CharField(max_length=20,blank=True)
    phone = models.CharField(max_length=100,default="")

    def formatted_items(self):
        try:
            items = json.loads(self.items_json)  # Parse items_json
            formatted = ""
            for item_id, details in items.items():
                qty, name, price, color, size, image_url = details
                formatted += f"""
                    <div>
                        <strong>Product Name:</strong> {name}<br>
                        <strong>Quantity:</strong> {qty}<br>
                        <strong>Price:</strong> ${price}<br>
                        <strong>Color:</strong> {color}<br>
                        <strong>Size:</strong> {size}<br>
                        <img src="{image_url}" alt="{name}" style="width: 50px; height: 50px;"/><br><br>
                    </div>
                """
            return format_html(formatted)
        except (ValueError, KeyError, TypeError):
            return "Invalid items format"

    formatted_items.short_description = "Order Details"

    def __str__(self):
        return self.name

class orderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    delivered=models.BooleanField(default=False)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."