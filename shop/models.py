from django.db import models

# Create your models here.

class Products(models.Model):
    CATEGORY_CHOICES = [
        ('drop_shoulders', 'Drop Shoulders'),
        ('baggy-joggers', 'Baggy Joggers'),
        ('baggy_shirts', 'Baggy Shirts'),
        ('cargo_pants', 'Cargo Pants'),
        ('head_wear', 'Head Wear'),
        ('baggy_shorts', 'Baggy Shorts'),
    ]

    product_id = models.AutoField
    product_name = models.CharField(max_length=100)
    product_category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='drop_shoulders')
    product_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    product_desc = models.TextField()
    product_color = models.TextField()
    product_size = models.TextField()
    product_image_1 = models.ImageField(upload_to='images')
    product_image_2 = models.ImageField(upload_to='images')
    product_image_3 = models.ImageField(upload_to='images')
    product_image_4 = models.ImageField(upload_to='images')
    product_image_5 = models.ImageField(upload_to='images')

    def __str__(self):
        return self.product_name


class Orders(models.Model):
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

    def __str__(self):
        return self.name

class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    delivered=models.BooleanField(default=False)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."