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
]