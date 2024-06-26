# Generated by Django 4.2.7 on 2024-04-08 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('party_name', models.TextField(blank=True, db_column='Party Name', null=True)),
                ('po_date', models.TextField(blank=True, db_column='PO Date', null=True)),
                ('invoice_no', models.IntegerField(db_column='Invoice No', primary_key=True, serialize=False)),
                ('invoice_date', models.DateField(db_column='Invoice Date')),
                ('product_code', models.CharField(db_column='Product Code', max_length=50)),
                ('product_description', models.CharField(db_column='Product Description', max_length=100)),
                ('specification', models.TextField(blank=True, db_column='Specification', null=True)),
                ('tariff_code', models.TextField(blank=True, db_column='Tariff Code', null=True)),
                ('pack_size', models.FloatField(db_column='Pack Size')),
                ('quantity', models.FloatField(db_column='Quantity')),
                ('uom', models.TextField(blank=True, db_column='UOM', null=True)),
                ('total_quantity', models.IntegerField(blank=True, db_column='Total Quantity', null=True)),
                ('currency', models.TextField(blank=True, db_column='Currency', null=True)),
                ('unit_price', models.FloatField(blank=True, db_column='Unit Price', null=True)),
                ('total_amount', models.FloatField(blank=True, db_column='Total Amount', null=True)),
                ('rate', models.FloatField(blank=True, db_column='Rate', null=True)),
                ('tot_amt_rs_field', models.FloatField(blank=True, db_column='Tot Amt Rs.', null=True)),
                ('cd', models.TextField(blank=True, db_column='CD', null=True)),
                ('igst', models.TextField(blank=True, db_column='IGST', null=True)),
                ('foreign_freight', models.TextField(blank=True, db_column='Foreign Freight', null=True)),
                ('cha_charges', models.TextField(blank=True, db_column='CHA Charges', null=True)),
                ('total', models.TextField(blank=True, db_column='Total', null=True)),
                ('unit_landed_cost_rs_field', models.TextField(blank=True, db_column='Unit Landed Cost (Rs.)', null=True)),
                ('myunknowncolumn', models.TextField(blank=True, db_column='MyUnknownColumn', null=True)),
            ],
            options={
                'db_table': 'invoice',
                'managed': False,
            },
        ),
    ]
