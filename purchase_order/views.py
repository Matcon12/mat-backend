from django.http import HttpResponse
from django.shortcuts import render
from .models import SupplierProductMaster, CustomerMaster, CustomerPurchaseOrder, CustPo
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
      msrrResult = ", ".join(productDetails[i].get('additionalDesc'))
      CustPo.objects.create(
        po_no = formData.get('poNo'),
        po_date = formData.get('poDate'),
        po_validity = formData.get('poValidity'),
        quote_id = formData.get('quoteId'),
        cust_id = formData.get('customerId'),
        consignee_id = formData.get('consigneeId'),
        po_sl_no = productDetails[i].get('poSlNo'),
        prod_id = productDetails[i].get('prodId'),
        prod_desc = productDetails[i].get('productDesc'),
        msrr = msrrResult,
        pack_size = productDetails[i].get('packSize'),
        quantity = productDetails[i].get('quantity'),
        # staggered_delivery = productDetails[i].get('staggeredDelivery'),
        unit_price = productDetails[i].get('unitPrice'),
        qty_sent = productDetails[i].get('qtySent'),
        qty_bal = productDetails[i].get('qtyBal')
      )
    
    return JsonResponse({"message": msrrResult})
    # return JsonResponse(response_data)
  else:
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
  

def get_data_purchase_order(request):
  if request.method == 'GET':
    try:
      cust_id = request.GET.get('cust_id')
      po_no = request.GET.get('po_no')
      po_sl_no = request.GET.get('po_sl_no')
      print(cust_id, po_no, po_sl_no)
      if cust_id and po_no and po_sl_no:        
        data = list(CustPo.objects.filter(cust_id=cust_id, po_no=po_no, po_sl_no=po_sl_no).values())
        return JsonResponse(data, safe=False)
      else:
        return JsonResponse({'error': 'parameters are missing'}, status=400)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'data not found'}, status=400)

@csrf_exempt
def update_purchase_order(request):
    if request.method == 'PUT':
        try:
            data = request.body.decode('utf-8')
            result = json.loads(data)
            
            print(result)
            
            cust_id = result.get('customerId')
            po_no = result.get('poNo')    
            po_sl_no = result.get('poSlNo')
            
            
            record = CustPo.objects.get(cust_id=cust_id, po_no=po_no, po_sl_no=po_sl_no)
            
            for key, value in result.items():
              setattr(record, key, value)
            
            record.save()
            
            return JsonResponse({'success': True})
        except CustPo.DoesNotExist:
            return JsonResponse({'error': 'Record not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
