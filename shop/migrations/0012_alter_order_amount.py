# Generated by Django 5.0.4 on 2024-11-08 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_product_latest_arrival_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
