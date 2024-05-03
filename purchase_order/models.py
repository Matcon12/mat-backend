from django.db import models

# Create your models here.
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