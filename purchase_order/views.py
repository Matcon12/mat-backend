from django.http import HttpResponse
from django.shortcuts import render
from .models import SupplierProductMaster, CustomerMaster, CustomerPurchaseOrder
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Max
from django.db import transaction, DatabaseError, connection

# Create your views here.
def index(request):
  customer_purchase_order = CustomerPurchaseOrder.objects.all()
  return JsonResponse(list(customer_purchase_order.values()), safe=False)
  # return HttpResponse("Hello, world. You're at the purchase_order index.")

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

        response_data = {
            'formData': formData,
            'productDetails': productDetails
        }

        max_slno = CustomerPurchaseOrder.objects.aggregate(Max('slno'))['slno__max']
        new_slno = max_slno + 1 if max_slno else 1  # Increment or start with 1

        for product in productDetails:
            msrrResult = ", ".join(product.get('additionalDesc', []))
            CustomerPurchaseOrder.objects.create(
                slno=new_slno,
                pono=formData.get('poNo'),
                podate=formData.get('poDate'),
                quote_id=formData.get('quoteId'),
                quote_date=formData.get('poValidity'),
                customer_id=formData.get('customerId'),
                consignee_id=formData.get('consigneeId'),
                po_sl_no=product.get('poSlNo'),
                prod_code=product.get('prodId'),
                additional_desc=msrrResult,
                pack_size=product.get('packSize'),
                quantity=product.get('quantity'),
                unit_price=product.get('unitPrice'),
                uom=product.get('uom'),
                total_price=product.get('totalPrice'),
                qty_sent="0",
                qty_balance=product.get('quantity'),
                delivery_date=product.get('deliveryDate')
            )

        return JsonResponse({"message": "Success", "details": response_data})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

def get_data_purchase_order(request):
  if request.method == 'GET':
    try:
      cust_id = request.GET.get('cust_id')
      po_no = request.GET.get('po_no')
      po_sl_no = request.GET.get('po_sl_no')
      if cust_id and po_no and po_sl_no:        
        data = list(CustomerPurchaseOrder.objects.filter(customer_id=cust_id, pono=po_no, po_sl_no=po_sl_no).values())
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
            
            # Extract search inputs
            search_inputs = result.get('searchInputs', {})
            cust_id = search_inputs.get('cust_id')
            po_no = search_inputs.get('po_no')
            po_sl_no = search_inputs.get('po_sl_no')
            
            if not all([cust_id, po_no, po_sl_no]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            
            # Fetch the record to update
            record = CustomerPurchaseOrder.objects.get(customer_id=cust_id, pono=po_no, po_sl_no=po_sl_no)
            
            # Update the record with new values from searchData
            search_data = result.get('searchData', {})
            for key, value in search_data.items():
                if hasattr(record, key):
                    setattr(record, key, value)
                else:
                    print(f"Invalid key: {key}")
            
            record.save()
            
            return JsonResponse({'success': True})
        except CustomerPurchaseOrder.DoesNotExist:
            return JsonResponse({'error': 'Record not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
def add_customer_details(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            data = data.get('formData', {})
            
            # Logging for debugging
            print(data)
            
            with transaction.atomic():
                customer = CustomerMaster.objects.create(
                    cust_id=data.get('Cust_ID'),
                    cust_name=data.get('Cust_Name'),
                    cust_addr1=data.get('Cust_addr1'),
                    cust_addr2=data.get('Cust_addr2'),
                    cust_city=data.get('Cust_City'),
                    cust_st_code=data.get('Cust_St_Code'),
                    cust_st_name=data.get('Cust_St_Name'),
                    cust_pin=data.get('Cust_PIN'),
                    cust_gst_id=data.get('Cust_GST_ID'),
                    phone_no=data.get('Phone_Num'),
                    email=data.get('Email')
                )
            
            # Ensure the connection is closed
            connection.close()
            
            return JsonResponse({'success': True, 'customer_id': customer.cust_id})
        
        except DatabaseError as e:
            return JsonResponse({'error': 'Database error: ' + str(e)}, status=500) 
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

    
def get_customer_data(request):
   if request.method =='GET':
      try:
         cust_id = request.GET.get('cust_id')
         if cust_id:
            result = CustomerMaster.objects.get(cust_id=cust_id)
            return JsonResponse({
               'cust_name': result.cust_name,
               'cust_addr1': result.cust_addr1,
               'cust_addr2': result.cust_addr2,
               'cust_city': result.cust_city,
               'cust_st_code': result.cust_st_code,
               'cust_st_name': result.cust_st_name,
               'cust_pin': result.cust_pin,
               'cust_gst_id': result.cust_gst_id,
               'phone_no': result.phone_no,
               'email': result.email,
            })
         else:
            return JsonResponse({'error': 'cust_id parameter is missing'}, status=400)
      except ObjectDoesNotExist:
         return JsonResponse({'customer_name': ''})
   else: 
      return JsonResponse({"error: Only GET requests are allowed"}, status=405)

@csrf_exempt
def update_customer_details(request):
    if request.method == 'PUT':
        try:
            data = request.body.decode('utf-8')
            result = json.loads(data)
            result = result.get('formData', {})
            print(result)
            
            # Fetch the record to update
            record = CustomerMaster.objects.get(cust_id=result.get('cust_id'))
            # Update the record with new values from searchData
            for key, value in result.items():
                if hasattr(record, key):
                    setattr(record, key, value)
                else:
                    print(f"Invalid key: {key}")
            
            record.save()
            
            return JsonResponse({'success': True})
        except CustomerPurchaseOrder.DoesNotExist:
            return JsonResponse({'error': 'Record not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
       return JsonResponse({"error: Only PUT requests are allowed"}, status=405)
    
@csrf_exempt
def add_product_details(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            data = data.get('formData', {})
            
            # Logging for debugging
            print(data)
            
            with transaction.atomic():
                customer = SupplierProductMaster.objects.create(
                   prod_id=data.get('Prod_ID'),
                   supp_id=data.get('Supp_ID'),
                   prod_desc=data.get('Prod_Desc'),
                   spec_id=data.get('Spec_ID'),
                   pack_size=data.get('Pack_Size'),
                   currency=data.get('Currency'),
                   price=data.get('Price'),
                )
            
            # Ensure the connection is closed
            connection.close()
            
            return JsonResponse({'success': True, 'customer_id': customer.prod_id})
        
        except DatabaseError as e:
            return JsonResponse({'error': 'Database error: ' + str(e)}, status=500) 
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

def get_product_details(request):
   if request.method =='GET':
      try:
         prod_id = request.GET.get('prod_id')
         if prod_id:
            result = SupplierProductMaster.objects.get(prod_id=prod_id)
            return JsonResponse({
               'cust_name': result.cust_name,
               'cust_addr1': result.cust_addr1,
               'cust_addr2': result.cust_addr2,
               'cust_city': result.cust_city,
               'cust_st_code': result.cust_st_code,
               'cust_st_name': result.cust_st_name,
               'cust_pin': result.cust_pin,
               'cust_gst_id': result.cust_gst_id,
               'phone_no': result.phone_no,
               'email': result.email,
            })
         else:
            return JsonResponse({'error': 'cust_id parameter is missing'}, status=400)
      except ObjectDoesNotExist:
         return JsonResponse({'customer_name': ''})
   else: 
      return JsonResponse({"error: Only GET requests are allowed"}, status=405)