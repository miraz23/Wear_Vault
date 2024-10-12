# Generated by Django 3.2.1 on 2024-10-12 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_name', models.CharField(max_length=150, verbose_name='Name')),
                ('contact_email', models.CharField(max_length=150, verbose_name='Email')),
                ('contact_subject', models.CharField(max_length=500, verbose_name='Subject')),
                ('contact_message', models.CharField(max_length=1500, verbose_name='Message')),
            ],
        ),
    ]
