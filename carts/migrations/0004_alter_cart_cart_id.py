# Generated by Django 4.2 on 2024-05-13 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0003_cartitem_variation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cart_id',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
