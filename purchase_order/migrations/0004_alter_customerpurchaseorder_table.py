# Generated by Django 4.2.7 on 2024-05-22 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_order', '0003_delete_custpo_alter_customermaster_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='customerpurchaseorder',
            table='Customer_Purchase_Order',
        ),
    ]
