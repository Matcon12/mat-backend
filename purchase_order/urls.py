from django.urls import path
from . import views

app_name = 'purchase_order'

urlpatterns = [
  path('', views.index, name='index'),
  path('packSize', views.get_pack_size, name='purchase'),
  path('customerName', views.get_customer_details, name='customer'),
  path('submitForm', views.submit_form, name='submitForm'),
  path('getData', views.get_data_purchase_order, name='updateForm'),
  path('updateForm', views.update_purchase_order, name='updateForm'),
  path('addCustomerDetails', views.add_customer_details, name='addCustomerDetails'),
  path('getCustomerData', views.get_customer_data, name="getCustomerData"),
  path("updateCustomerDetails", views.update_customer_details, name="updateCustomerDetails"),
  path("addProductDetails", views.add_product_details, name="addProductDetails"),
  path("getProductDetails", views.get_product_details, name="getProductDetails"),
  path("updateProductDetails", views.update_product_details, name="updateProductDetails"),
  path("invoiceProcessing", views.invoice_processing, name="invoiceProcessing"),
  path("invoiceGeneration", views.invoice_generation, name="invoiceGeneration"),
  path("getInvoiceData", views.get_invoice_data, name="getInvoiceData"),
  path("getStateData", views.get_state_data, name="getStateData"),
  path("signup", views.signup, name="signup"),
  path("login", views.login, name="login"),
  path("test_token", views.test_token, name="test_token"),
  path("logout", views.logout, name="logout")
]