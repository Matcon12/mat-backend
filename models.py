# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


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


class CustomerMaster(models.Model):
    cust_id = models.CharField(primary_key=True, max_length=15)
    cust_name = models.CharField(max_length=50)
    cust_addr1 = models.CharField(max_length=50)
    cust_addr2 = models.CharField(max_length=50)
    cust_city = models.CharField(max_length=15)
    cust_st_code = models.CharField(max_length=2)
    cust_st_name = models.CharField(max_length=20)
    cust_pin = models.CharField(max_length=6)
    cust_gst_id = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'customer_master'


class CustomerPurchaseOrder(models.Model):
    po_no = models.CharField(max_length=50)
    po_date = models.DateField(blank=True, null=True)
    po_validity = models.DateField(blank=True, null=True)
    quote_id = models.CharField(max_length=15, blank=True, null=True)
    cust_id = models.CharField(max_length=15, blank=True, null=True)
    consignee_id = models.CharField(max_length=15, blank=True, null=True)
    po_sl_no = models.CharField(max_length=5, blank=True, null=True)
    prod_id = models.CharField(max_length=30, blank=True, null=True)
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
        unique_together = (('id', 'po_no'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Invoice(models.Model):
    party_name = models.TextField(db_column='Party Name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    po_date = models.TextField(db_column='PO Date', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    invoice_no = models.TextField(db_column='Invoice No', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    invoice_date = models.TextField(db_column='Invoice Date', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    product_code = models.TextField(db_column='Product Code', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    product_description = models.TextField(db_column='Product Description', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    specification = models.TextField(db_column='Specification', blank=True, null=True)  # Field name made lowercase.
    tariff_code = models.TextField(db_column='Tariff Code', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    pack_size = models.TextField(db_column='Pack Size', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    quantity = models.TextField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.
    uom = models.TextField(db_column='UOM', blank=True, null=True)  # Field name made lowercase.
    total_quantity = models.TextField(db_column='Total Quantity', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    currency = models.TextField(db_column='Currency', blank=True, null=True)  # Field name made lowercase.
    unit_price = models.TextField(db_column='Unit Price', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    total_amount = models.TextField(db_column='Total Amount', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rate = models.TextField(db_column='Rate', blank=True, null=True)  # Field name made lowercase.
    unit_price_in_rs = models.TextField(db_column='Unit Price In Rs', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    tot_amt_rs_field = models.TextField(db_column='Tot Amt Rs.', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    cd = models.TextField(db_column='CD', blank=True, null=True)  # Field name made lowercase.
    igst = models.TextField(db_column='IGST', blank=True, null=True)  # Field name made lowercase.
    foreign_freight_excl_gst_field = models.TextField(db_column='Foreign Freight\n ( Excl GST )', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    ex_works_freight_uk_excl_gst_field = models.TextField(db_column='Ex works Freight UK\n ( Excl GST)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    cha_charges_excl_gst_field = models.TextField(db_column='CHA Charges\n(Excl GST)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    total_incl_b_e_igst_excl_cha_igst = models.TextField(db_column='Total incl\nB/E IGST  Excl CHA IGST', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    unit_landed_cost_rs_col_24_col_12 = models.TextField(db_column='Unit Landed Cost (Rs.)\nCol 24/col 12', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    b_e_gross_weight_kgs = models.TextField(db_column='B/E Gross weight Kgs', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    field_f_freight_ex_works_freight_cha_charges_gw = models.TextField(db_column='(F  Freight+ Ex Works Freight+CHA charges)/\nGW', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    id = models.TextField(db_column='ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'invoice'


class InvoiceMymodel(models.Model):
    id = models.BigAutoField(primary_key=True)
    invoice_no = models.CharField(db_column='Invoice_No', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'invoice_mymodel'


class InwDc(models.Model):
    grn_no = models.CharField(primary_key=True, max_length=20)  # The composite primary key (grn_no, po_no, prod_id) found, that is not supported. The first column is selected.
    grn_date = models.DateField(blank=True, null=True)
    coc_no = models.CharField(db_column='CoC_no', max_length=20, blank=True, null=True)  # Field name made lowercase.
    invoive_no = models.CharField(max_length=12, blank=True, null=True)
    invoice_date = models.DateField(blank=True, null=True)
    po_no = models.CharField(max_length=20)
    po_date = models.DateField(blank=True, null=True)
    receiver_id = models.CharField(max_length=4, blank=True, null=True)
    consignee_id = models.CharField(max_length=4, blank=True, null=True)
    supp_id = models.CharField(max_length=4, blank=True, null=True)
    prod_id = models.CharField(max_length=20)
    prod_desc = models.CharField(max_length=25, blank=True, null=True)
    pack_size = models.CharField(max_length=5, blank=True, null=True)
    batch_number = models.CharField(max_length=5, blank=True, null=True)
    qty_received = models.IntegerField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    vat_amount = models.DecimalField(db_column='VAT_amount', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'inw_dc'
        unique_together = (('grn_no', 'po_no', 'prod_id'),)


class OtwDc(models.Model):
    gcn_no = models.CharField(primary_key=True, max_length=15)  # The composite primary key (gcn_no, po_no, prod_id) found, that is not supported. The first column is selected.
    gcn_date = models.DateField(blank=True, null=True)
    po_no = models.CharField(max_length=30)
    po_date = models.DateField(blank=True, null=True)
    cust_id = models.CharField(max_length=15, blank=True, null=True)
    consignee_id = models.CharField(max_length=15, blank=True, null=True)
    prod_id = models.CharField(max_length=30)
    prod_desc = models.CharField(max_length=50, blank=True, null=True)
    msrr = models.CharField(max_length=50, blank=True, null=True)
    qty_delivered = models.IntegerField(blank=True, null=True)
    pack_size = models.CharField(max_length=10, blank=True, null=True)
    unit_price = models.FloatField(blank=True, null=True)
    taxable_amt = models.FloatField(blank=True, null=True)
    cgst_price = models.FloatField(blank=True, null=True)
    sgst_price = models.FloatField(blank=True, null=True)
    igst_price = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'otw_dc'
        unique_together = (('gcn_no', 'po_no', 'prod_id'),)


class PriceList(models.Model):
    id = models.TextField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    product_code = models.TextField(db_column='Product Code', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    product_description = models.TextField(db_column='Product Description', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    number_2022_rates = models.TextField(db_column='2022 Rates', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it wasn't a valid Python identifier.
    percentage_change_22_23_field = models.TextField(db_column='Percentage change(22-23)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    number_2023_rates = models.TextField(db_column='2023 Rates', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it wasn't a valid Python identifier.
    percentage_change_23_24_field = models.TextField(db_column='Percentage change(23-24)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    number_2024_rates = models.TextField(db_column='2024 Rates', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it wasn't a valid Python identifier.

    class Meta:
        managed = False
        db_table = 'price_list'


class Quotation(models.Model):
    cust_id = models.CharField(primary_key=True, max_length=4)  # The composite primary key (cust_id, quote_id) found, that is not supported. The first column is selected.
    quote_id = models.CharField(max_length=10)
    quote_date = models.DateField(blank=True, null=True)
    cust_ref = models.CharField(max_length=4, blank=True, null=True)
    cust_ref_date = models.DateField(blank=True, null=True)
    prod_id = models.CharField(max_length=4, blank=True, null=True)
    pack_size = models.CharField(max_length=5, blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    quote_valid_till = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'quotation'
        unique_together = (('cust_id', 'quote_id'),)


class StaggeredDelivery(models.Model):
    po_no = models.CharField(primary_key=True, max_length=20)  # The composite primary key (po_no, cust_id, prod_id) found, that is not supported. The first column is selected.
    po_date = models.DateField(blank=True, null=True)
    cust_id = models.CharField(max_length=4)
    prod_id = models.CharField(max_length=4)
    pack_size = models.CharField(max_length=5, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    qty_sent = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'staggered_delivery'
        unique_together = (('po_no', 'cust_id', 'prod_id'),)


class SupplierInvoice(models.Model):
    party_name = models.TextField(db_column='Party Name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    po_date = models.TextField(db_column='PO Date', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    invoice_no = models.TextField(db_column='Invoice No', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    invoice_date = models.TextField(db_column='Invoice Date', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    product_code = models.TextField(db_column='Product Code', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    product_description = models.TextField(db_column='Product Description', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    specification = models.TextField(db_column='Specification', blank=True, null=True)  # Field name made lowercase.
    tariff_code = models.TextField(db_column='Tariff Code', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    pack_size = models.TextField(db_column='Pack Size', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    quantity = models.TextField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.
    uom = models.TextField(db_column='UOM', blank=True, null=True)  # Field name made lowercase.
    total_quantity = models.TextField(db_column='Total Quantity', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    currency = models.TextField(db_column='Currency', blank=True, null=True)  # Field name made lowercase.
    unit_price = models.TextField(db_column='Unit Price', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    total_amount = models.TextField(db_column='Total Amount', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rate = models.TextField(db_column='Rate', blank=True, null=True)  # Field name made lowercase.
    unit_price_in_rs = models.TextField(db_column='Unit Price In Rs', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    tot_amt_rs_field = models.TextField(db_column='Tot Amt Rs.', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    cd = models.TextField(db_column='CD', blank=True, null=True)  # Field name made lowercase.
    igst = models.TextField(db_column='IGST', blank=True, null=True)  # Field name made lowercase.
    foreign_freight_excl_gst_field = models.TextField(db_column='Foreign Freight\n ( Excl GST )', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    ex_works_freight_uk_excl_gst_field = models.TextField(db_column='Ex works Freight UK\n ( Excl GST)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    cha_charges_excl_gst_field = models.TextField(db_column='CHA Charges\n(Excl GST)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    total_incl_b_e_igst_excl_cha_igst = models.TextField(db_column='Total incl\nB/E IGST  Excl CHA IGST', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    unit_landed_cost_rs_col_24_col_12 = models.TextField(db_column='Unit Landed Cost (Rs.)\nCol 24/col 12', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    b_e_gross_weight_kgs = models.TextField(db_column='B/E Gross weight Kgs', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    field_f_freight_ex_works_freight_cha_charges_gw = models.TextField(db_column='(F  Freight+ Ex Works Freight+CHA charges)/\nGW', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    id = models.TextField(db_column='ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'supplier_invoice'


class SupplierMaster(models.Model):
    supp_id = models.CharField(primary_key=True, max_length=4)
    supp_name = models.CharField(max_length=50, blank=True, null=True)
    supp_addr1 = models.CharField(max_length=30, blank=True, null=True)
    supp_addr2 = models.CharField(max_length=30, blank=True, null=True)
    supp_city = models.CharField(max_length=15, blank=True, null=True)
    post_code = models.CharField(db_column='Post_Code', max_length=10, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=20, blank=True, null=True)  # Field name made lowercase.
    vat_code = models.CharField(db_column='VAT_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'supplier_master'


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


class SupplierPurchaseOrder(models.Model):
    po_no = models.CharField(primary_key=True, max_length=20)  # The composite primary key (po_no, prod_id) found, that is not supported. The first column is selected.
    po_date = models.DateField(blank=True, null=True)
    po_validity = models.DateField(blank=True, null=True)
    supp_id = models.CharField(max_length=4, blank=True, null=True)
    quote_ref_no = models.CharField(max_length=4, blank=True, null=True)
    receiver_id = models.CharField(max_length=4, blank=True, null=True)
    consignee_id = models.CharField(max_length=4, blank=True, null=True)
    prod = models.ForeignKey(SupplierProductMaster, models.DO_NOTHING)
    pack_size = models.CharField(max_length=5, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    qty_received = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'supplier_purchase_order'
        unique_together = (('po_no', 'prod'),)
