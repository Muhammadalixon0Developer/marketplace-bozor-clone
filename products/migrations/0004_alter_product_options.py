# Generated by Django 5.0.1 on 2024-01-10 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_rename_addres_product_address_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-id',)},
        ),
    ]
