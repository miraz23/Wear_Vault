# Generated by Django 3.2.1 on 2024-10-23 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20241023_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_color',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_desc',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_size',
            field=models.CharField(max_length=20),
        ),
    ]