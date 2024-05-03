from django.http import HttpResponse
from django.shortcuts import render
from .models import SupplierProductMaster, CustomerMaster, CustomerPurchaseOrder
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def index(request):
  return HttpResponse("Hello, world. You're at the purchase_order index.")

@csrf_exempt
def get_pack_size(request):
    if request.method == 'GET':
        try:
            prod_id = request.GET.get('prodId')  # Change to GET
            if prod_id:
                result = SupplierProductMaster.objects.get(prod_id=prod_id)
                return JsonResponse({
                  'pack_size': result.pack_size,
                  'prod_desc': result.prod_desc,
                })
            else:
                return JsonResponse({'error': 'prodId parameter is missing'}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({'pack_size': '', 'prod_desc': ''})
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)  # Update error message

def get_customer_details(request):
  if request.method == 'GET':
    try:
      cust_id = request.GET.get('customerId')
      if cust_id:
        result = CustomerMaster.objects.get(cust_id=cust_id)
        return JsonResponse({
          'customer_name': result.cust_name
        })
      else:
        return JsonResponse({'error': 'customerId parameter is missing'}, status=400)
    except ObjectDoesNotExist:
      return JsonResponse({'customer_name': ''})
  else: 
    return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)
  
@csrf_exempt
def submit_form(request):
  if request.method == 'POST':   
    
    data = json.loads(request.body.decode('utf-8'))
    formData = data.get('formData')
    productDetails = data.get('productDetails')    
    
    response_data ={
      'formData': formData,
      'productDetails': productDetails
    }
    
    for i in range(0, len(productDetails)):
      CustomerPurchaseOrder.objects.create(
        po_no = formData.get('poNo'),
        po_date = formData.get('poDate'),
        po_validity = formData.get('poValidity'),
        quote_id = formData.get('quoteId'),
        cust_id = formData.get('customerId'),
        consignee_id = formData.get('consigneeId'),
        po_sl_no = productDetails[i].get('poSlNo'),
        prod_id = productDetails[i].get('prodId'),
        prod_desc = productDetails[i].get('prodDesc'),
        msrr = productDetails[i].get('msrr'),
        pack_size = productDetails[i].get('packSize'),
        quantity = productDetails[i].get('quantity'),
        staggered_delivery = productDetails[i].get('staggeredDelivery'),
        unit_price = productDetails[i].get('unitPrice'),
        qty_sent = productDetails[i].get('qtySent'),
        qty_bal = productDetails[i].get('qtyBal')
      )
    
    return JsonResponse({"message":"success"})
    # return JsonResponse(response_data)
  else:
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)