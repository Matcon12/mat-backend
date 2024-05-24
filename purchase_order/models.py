from django.db import models

# Create your models here.

class CustomerMaster(models.Model):
    cust_name = models.TextField(db_column='Cust_Name', blank=True, null=True)  # Field name made lowercase.
    cust_id = models.TextField(db_column='Cust_ID', primary_key=True)  # Field name made lowercase.
    cust_addr1 = models.TextField(db_column='Cust_addr1', blank=True, null=True)  # Field name made lowercase.
    cust_addr2 = models.TextField(db_column='Cust_addr2', blank=True, null=True)  # Field name made lowercase.
    cust_city = models.TextField(db_column='Cust_City', blank=True, null=True)  # Field name made lowercase.
    cust_st_code = models.TextField(db_column='Cust_St_Code', blank=True, null=True)  # Field name made lowercase.
    cust_st_name = models.TextField(db_column='Cust_St_Name', blank=True, null=True)  # Field name made lowercase.
    cust_pin = models.TextField(db_column='Cust_PIN', blank=True, null=True)  # Field name made lowercase.
    cust_gst_id = models.TextField(db_column='Cust_GST_ID', blank=True, null=True)  # Field name made lowercase.
    phone_no = models.TextField(db_column='Phone_No', blank=True, null=True)  # Field name made lowercase.
    email = models.TextField(db_column='Email', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Customer_Master'
        
class CustomerPurchaseOrder(models.Model):
    slno = models.IntegerField(db_column='SlNo', primary_key=True)  # Field name made lowercase. The composite primary key (SlNo, PONo, Customer_ID, PO_Sl_No) found, that is not supported. The first column is selected.
    pono = models.TextField(db_column='PONo')  # Field name made lowercase.
    podate = models.TextField(db_column='PODate', blank=True, null=True)  # Field name made lowercase.
    quote_id = models.TextField(db_column='Quote_ID', blank=True, null=True)  # Field name made lowercase.
    quote_date = models.TextField(db_column='Quote_Date', blank=True, null=True)  # Field name made lowercase.
    customer_id = models.TextField(db_column='Customer_ID')  # Field name made lowercase.
    consignee_id = models.TextField(db_column='Consignee_ID', blank=True, null=True)  # Field name made lowercase.
    po_sl_no = models.TextField(db_column='PO_Sl_No')  # Field name made lowercase.
    prod_code = models.TextField(db_column='Prod_Code', blank=True, null=True)  # Field name made lowercase.
    additional_desc = models.TextField(db_column='Additional_Desc', blank=True, null=True)  # Field name made lowercase.
    pack_size = models.TextField(db_column='Pack_Size', blank=True, null=True)  # Field name made lowercase.
    quantity = models.TextField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.
    unit_price = models.TextField(db_column='Unit_Price', blank=True, null=True)  # Field name made lowercase.
    uom = models.TextField(db_column='UOM', blank=True, null=True)  # Field name made lowercase.
    total_price = models.TextField(db_column='Total_Price', blank=True, null=True)  # Field name made lowercase.
    qty_balance = models.TextField(db_column='Qty_Balance', blank=True, null=True)  # Field name made lowercase.
    qty_sent = models.TextField(db_column='Qty_Sent', blank=True, null=True)  # Field name made lowercase.
    delivery_date = models.TextField(db_column='Delivery_Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Customer_Purchase_Order'

        
class SupplierProductMaster(models.Model):
    prod_id = models.TextField(primary_key=True)  # The composite primary key (prod_id, pack_size) found, that is not supported. The first column is selected.
    supp_id = models.TextField(blank=True, null=True)
    prod_desc = models.TextField(blank=True, null=True)
    spec_id = models.TextField(blank=True, null=True)
    pack_size = models.TextField(blank=True, null=True)
    currency = models.TextField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'supplier_product_master'
