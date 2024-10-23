from django.db import models

# Create your models here.

class product(models.Model):
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
