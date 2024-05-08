from django.db import models

# Create your models here.

class CustomerMaster(models.Model):
    cust_id = models.CharField(primary_key=True, max_length=4)
    cust_name = models.CharField(max_length=50, blank=True, null=True)
    cust_addr1 = models.CharField(max_length=30, blank=True, null=True)
    cust_addr2 = models.CharField(max_length=30, blank=True, null=True)
    cust_city = models.CharField(max_length=15, blank=True, null=True)
    cust_st_code = models.IntegerField(blank=True, null=True)
    cust_st_name = models.CharField(max_length=20, blank=True, null=True)
    cust_pin = models.CharField(max_length=6, blank=True, null=True)
    cust_gst_id = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_master'
        
class CustomerPurchaseOrder(models.Model):
    po_no = models.CharField(max_length=30)
    po_date = models.DateField(blank=True, null=True)
    po_validity = models.DateField(blank=True, null=True)
    quote_id = models.CharField(max_length=15, blank=True, null=True)
    cust_id = models.CharField(max_length=15)
    consignee_id = models.CharField(max_length=15, blank=True, null=True)
    po_sl_no = models.CharField(max_length=5, blank=True, null=True)
    prod_id = models.CharField(max_length=30)
    prod_desc = models.CharField(max_length=50, blank=True, null=True)
    msrr = models.CharField(max_length=50, blank=True, null=True)
    pack_size = models.CharField(max_length=10, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    staggered_delivery = models.IntegerField(blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    qty_sent = models.IntegerField(blank=True, null=True)
    qty_bal = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_purchase_order'
        unique_together = (('id', 'po_no', 'cust_id', 'prod_id'),)
        
class SupplierProductMaster(models.Model):
    prod_id = models.CharField(primary_key=True, max_length=30)  # The composite primary key (prod_id, supp_id) found, that is not supported. The first column is selected.
    supp_id = models.CharField(max_length=4)
    prod_desc = models.CharField(max_length=75, blank=True, null=True)
    spec_id = models.CharField(max_length=4, blank=True, null=True)
    pack_size = models.CharField(max_length=10, blank=True, null=True)
    currency = models.CharField(max_length=4, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'supplier_product_master'
        unique_together = (('prod_id', 'supp_id'),)
        
class CustPo(models.Model):
    po_no = models.CharField(max_length=100, blank=True, null=True)
    po_date = models.DateField(blank=True, null=True)
    po_validity = models.DateField(blank=True, null=True)
    quote_id = models.CharField(max_length=50, blank=True, null=True)
    cust_id = models.CharField(max_length=30, blank=True, null=True)
    consignee_id = models.CharField(max_length=30, blank=True, null=True)
    po_sl_no = models.CharField(max_length=15, blank=True, null=True)
    prod_id = models.CharField(max_length=50, blank=True, null=True)
    prod_desc = models.CharField(max_length=100, blank=True, null=True)
    msrr = models.CharField(max_length=100, blank=True, null=True)
    pack_size = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.CharField(max_length=30, blank=True, null=True)
    staggered_deliver = models.CharField(max_length=45, blank=True, null=True)
    unit_price = models.CharField(max_length=20, blank=True, null=True)
    qty_sent = models.CharField(max_length=15, blank=True, null=True)
    qty_bal = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cust_po'