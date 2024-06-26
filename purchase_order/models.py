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
    contact_name_1 = models.TextField(db_column='Contact_Name_1', blank=True, null=True)  # Field name made lowercase.
    contact_phone_1 = models.TextField(db_column='Contact_Phone_1', blank=True, null=True)  # Field name made lowercase.
    contact_email_1 = models.TextField(db_column='Contact_Email_1', blank=True, null=True)  # Field name made lowercase.
    contact_name_2 = models.TextField(db_column='Contact_Name_2', blank=True, null=True)  # Field name made lowercase.
    contact_phone_2 = models.TextField(db_column='Contact_Phone_2', blank=True, null=True)  # Field name made lowercase.
    contact_email_2 = models.TextField(db_column='Contact_Email_2', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Customer_Master'
        
class CustomerPurchaseOrder(models.Model):
    slno = models.TextField(db_column='SlNo', primary_key=True)  # Field name made lowercase. The composite primary key (SlNo, PONo, Customer_ID, PO_Sl_No) found, that is not supported. The first column is selected. This field type is a guess.
    pono = models.TextField(db_column='PONo')  # Field name made lowercase.
    podate = models.TextField(db_column='PODate', blank=True, null=True)  # Field name made lowercase.
    quote_id = models.TextField(db_column='Quote_ID', blank=True, null=True)  # Field name made lowercase.
    quote_date = models.TextField(db_column='Quote_Date', blank=True, null=True)  # Field name made lowercase.
    customer_id = models.TextField(db_column='Customer_ID')  # Field name made lowercase.
    consignee_id = models.TextField(db_column='Consignee_ID', blank=True, null=True)  # Field name made lowercase.
    po_sl_no = models.TextField(db_column='PO_Sl_No')  # Field name made lowercase.
    prod_code = models.TextField(db_column='Prod_Code', blank=True, null=True)  # Field name made lowercase.
    prod_desc = models.TextField(db_column='Prod_Desc', blank=True, null=True)  # Field name made lowercase.
    additional_desc = models.TextField(db_column='Additional_Desc', blank=True, null=True)  # Field name made lowercase.
    omat = models.TextField(db_column='Omat', blank=True, null=True)  # Field name made lowercase.
    pack_size = models.TextField(db_column='Pack_Size', blank=True, null=True)  # Field name made lowercase.
    quantity = models.TextField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.
    unit_price = models.TextField(db_column='Unit_Price', blank=True, null=True)  # Field name made lowercase.
    uom = models.TextField(db_column='UOM', blank=True, null=True)  # Field name made lowercase.
    hsn_sac = models.TextField(db_column='Hsn_Sac', blank=True, null=True)  # Field name made lowercase.
    total_price = models.TextField(db_column='Total_Price', blank=True, null=True)  # Field name made lowercase.
    qty_balance = models.TextField(db_column='Qty_Balance', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    qty_sent = models.TextField(db_column='Qty_Sent', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    delivery_date = models.TextField(db_column='Delivery_Date', blank=True, null=True)  # Field name made lowercase.
    po_validity = models.TextField(db_column='Po_Validity', blank=True, null=True)  # Field name made lowercase.
    gst_applicable = models.BooleanField(blank=True, null=True)

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

class GstRates(models.Model):
    cgst_rate = models.IntegerField(blank=True, null=True)
    sgst_rate = models.IntegerField(blank=True, null=True)
    igst_rate = models.IntegerField(blank=True, null=True)
    fin_year = models.IntegerField(blank=True, null=True)
    last_gcn_no = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gst_rates'


class GstStateCode(models.Model):
    state_code = models.AutoField(primary_key=True)
    state_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gst_state_code'
        
class OtwDc(models.Model):
    sl_no = models.AutoField(primary_key=True)  # The composite primary key (sl_no, gcn_no, po_no, po_sl_no) found, that is not supported. The first column is selected.
    gcn_no = models.TextField()
    gcn_date = models.TextField(blank=True, null=True)
    po_no = models.TextField()
    po_date = models.TextField(blank=True, null=True)
    cust_id = models.TextField(blank=True, null=True)
    consignee_id = models.TextField(blank=True, null=True)
    prod_id = models.TextField(blank=True, null=True)
    po_sl_no = models.TextField()
    prod_desc = models.TextField(blank=True, null=True)
    additional_desc = models.TextField(blank=True, null=True)
    omat = models.TextField(blank=True, null=True)
    qty_delivered = models.TextField(blank=True, null=True)
    pack_size = models.TextField(blank=True, null=True)
    unit_price = models.TextField(blank=True, null=True)
    taxable_amt = models.TextField(blank=True, null=True)
    cgst_price = models.TextField(blank=True, null=True)
    sgst_price = models.TextField(blank=True, null=True)
    igst_price = models.TextField(blank=True, null=True)
    hsn_sac = models.TextField(blank=True, null=True)
    batch = models.TextField(blank=True, null=True)
    coc = models.TextField(blank=True, null=True)
    contact_name = models.TextField(blank=True, null=True)
    contact_number = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'otw_dc'