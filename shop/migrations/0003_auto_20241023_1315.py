# Generated by Django 3.2.1 on 2024-10-23 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_product_product_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_image',
        ),
        migrations.AddField(
            model_name='product',
            name='product_image_1',
            field=models.ImageField(default=0, upload_to='images'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_image_2',
            field=models.ImageField(default=0, upload_to='images'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_image_3',
            field=models.ImageField(default=0, upload_to='images'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_image_4',
            field=models.ImageField(default=0, upload_to='images'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_image_5',
            field=models.ImageField(default=0, upload_to='images'),
        ),
    ]