from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import SupplierProductMaster, CustomerMaster, CustomerPurchaseOrder, GstRates, GstStateCode, OtwDc
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Max, F, Sum
from django.db import transaction, DatabaseError, connection
import pandas as pd
import datetime as d
from babel.numbers import format_currency
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.forms.models import model_to_dict

from .serializers import UserSerializer

import logging
import decimal

import xlsxwriter

# Set up logging
logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
  customer_purchase_order = CustomerPurchaseOrder.objects.all()
  return JsonResponse(list(customer_purchase_order.values()), safe=False)
  # return HttpResponse("Hello, world. You're at the purchase_order index.")

def convert_rupees_to_words(amount):
    ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", 
            "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen","Seventeen", "Eighteen", "Nineteen"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    thousands = ["", "Thousand", "Lakh", "Crore"]
    def convert_two_digits(num):
        if num < 20:
            return ones[num] + " "
        else:
            return tens[num // 10] + " " + ones[num % 10]
    def convert_three_digits(num):
        if num < 100:
            return convert_two_digits(num)
        else:
            return ones[num // 100] + " Hundred " + convert_two_digits(num % 100)
    result = ""    
    amount = format(amount, ".2f")
    RsPs = str(amount).split('.')
    Rs = int(RsPs[0])
    Ps = int(RsPs[1])
    if Rs == 0:
        result += "Zero "
    else:
        for i in range(4):
            if i == 0 or i == 3:
                chunk = Rs % 1000
                Rs //= 1000
            else:
                chunk = Rs % 100
                Rs //= 100
            if chunk != 0:
                result = convert_three_digits(chunk) + " " + thousands[i] + " " +result
    if Ps > 0:
        result = result.strip() + " and Paise " + convert_two_digits(Ps)        
    result = "Rupees " + result.strip() + " Only"
    return result.upper()

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

def get_customer_detail(request):
  if request.method == 'GET':
    try:
      cust_id = request.GET.get('customerId')
      if cust_id:
        result = CustomerMaster.objects.get(cust_id=cust_id)
        return JsonResponse({
          'customer_name': result.cust_name,
          'gst_exception': result.gst_exception,
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
        # return JsonResponse({"message": "Success", "details": response_data})

        for product in productDetails:
            max_slno = CustomerPurchaseOrder.objects.aggregate(Max('slno'))['slno__max']
            new_slno = max_slno + 1 if max_slno else 1  # Increment or start with 1
            # msrrResult = ", ".join(product.get('additionalDesc', []))
            CustomerPurchaseOrder.objects.create(
                slno=new_slno,
                pono=formData.get('poNo'),
                podate=formData.get('poDate'),
                quote_id=formData.get('quoteId'),
                quote_date=formData.get('poValidity'),
                customer_id=formData.get('customerId'),
                consignee_id=formData.get('consigneeId'),
                gst_exception=formData.get('gst_exception'),
                po_sl_no=product.get('poSlNo'),
                prod_code=product.get('prodId'),
                prod_desc=product.get('productDesc'),
                additional_desc=product.get('msrr'),
                omat=product.get('omat'),
                hsn_sac=product.get('hsn_sac'),
                pack_size=product.get('packSize'),
                quantity=product.get('quantity'),
                unit_price=product.get('unitPrice'),
                uom=product.get('uom'),
                total_price=product.get('totalPrice'),
                qty_sent="0",
                qty_balance=product.get('quantity'),
                delivery_date=product.get('deliveryDate'),
                po_validity=product.get('poValidity'),
            )

        return JsonResponse({"message": "Success", "details": response_data})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

def get_data_purchase_order(request):
    if request.method == 'GET':
        try:
            po_no = request.GET.get('pono')
            data = CustomerPurchaseOrder.objects.filter(pono=po_no).first()
            if data:    
                data_dict = model_to_dict(data)
                return JsonResponse({"success": True, "data": data_dict})
            else:
                return JsonResponse({"success": False, "error": "Data not found"})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'data not found'}, status=400)
        
def get_data_po_cust(request):
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
            search_inputs = result.get('searchData', {})
            cust_id = search_inputs.get('customer_id')
            po_no = search_inputs.get('pono')
            po_sl_no = search_inputs.get('po_sl_no')
            print(f"Customer ID: {cust_id}, PO Number: {po_no}, PO SL Number: {po_sl_no}")
            
            if not all([cust_id, po_no, po_sl_no]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            
            # Fetch the record to update
            record = CustomerPurchaseOrder.objects.get(customer_id=cust_id, pono=po_no, po_sl_no=po_sl_no)
            print(f"Record before update: {record.__dict__}")
            
            # Update the record with new values from searchData
            search_data = result.get('searchData', {})
            print(search_data)
            for key, value in search_data.items():
                if hasattr(record, key):
                    setattr(record, key, value)
                else:
                    print(f"Invalid key: {key}")
            
            record.save()
            print(f"Record after update: {record.__dict__}")
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

    
def get_customer_details(request):
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
               'contact_name_1': result.contact_name_1,
               'contact_phone_1': result.contact_phone_1,
               'contact_email_1': result.contact_email_1,
               'contact_name_2': result.contact_name_2,
               'contact_phone_2': result.contact_phone_2,
               'contact_email_2': result.contact_email_2,
               'gst_exception': result.gst_exception,
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
            
            with transaction.atomic():
                customer = SupplierProductMaster.objects.create(
                   prod_id=data.get('Prod_ID'),
                   supp_id=data.get('Supp_ID'),
                   prod_desc=data.get('Prod_Desc'),
                   spec_id=data.get('Spec_ID'),
                   pack_size=data.get('Pack_Size'),
                   currency=data.get('Currency'),
                   price=data.get('Price'),
                   hsn_code=data.get("hsn_code"),
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
                "prod_id": result.prod_id,
                "supp_id": result.supp_id,
                "prod_desc": result.prod_desc,
                "spec_id": result.spec_id,
                "pack_size": result.pack_size,
                "currency": result.currency,
                "price": result.price, 
                "hsn_code": result.hsn_code,
            })
         else:
            return JsonResponse({'error': 'prod_id parameter is missing'}, status=400)
      except ObjectDoesNotExist:
         return JsonResponse({'customer_name': ''})
   else: 
      return JsonResponse({"error: Only GET requests are allowed"}, status=405)
   
@csrf_exempt
def update_product_details(request):
    if request.method == 'PUT':
        try:
            data = request.body.decode('utf-8')
            result = json.loads(data)
            result = result.get('formData', {})
            
            # Fetch the record to update
            record = SupplierProductMaster.objects.get(prod_id=result.get('prod_id'))
            # Update the record with new values from searchData
            for key, value in result.items():
                if hasattr(record, key):
                    setattr(record, key, value)
                else:
                    print(f"Invalid key: {key}")
            
            record.save()
            
            return JsonResponse({'success': True})
        except SupplierProductMaster.DoesNotExist:
            return JsonResponse({'error': 'Record not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
       return JsonResponse({"error: Only PUT requests are allowed"}, status=405)
    
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd
from datetime import datetime as d
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Max

@csrf_exempt
def invoice_processing(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)

    try:
        po_no = data['formData2'].get('poNo').strip()
        cust_id = data['formData2'].get('customerId')
        new_cons_id = data['formData2'].get('newConsigneeName', '')
        contact_name = data['formData2'].get('contactName')
        gst_exception = data['formData2'].get('gstException')
        freight_charges = data['formData2'].get('freightCharges')
        insurance_charges = data['formData2'].get('insuranceCharges')
        other_charges = data['formData2'].get('otherCharges')
    except KeyError as e:
        return JsonResponse({"error": f"Missing key: {e}"}, status=400)
    
    try:
        contact_nums = CustomerMaster.objects.filter(cust_id=cust_id).values().first()
        if not contact_nums:
            return JsonResponse({"error": "Customer not found"}, status=404)
        contact = contact_nums['contact_phone_1'] if contact_nums['contact_name_1'] == contact_name else contact_nums['contact_phone_2']
    except CustomerMaster.DoesNotExist:
        return JsonResponse({"error": "Customer not found"}, status=404)

    po_sl_numbers = []
    qty_tobe_del = []
    hsn = []
    batch = []
    coc = []

    try:
        for item in data['formData2']['items']:
            po_sl_numbers.append(item['poSlNo'])
            qty_tobe_del.append(item['quantity'])
            hsn.append(item['hsnSac'])
            batch.append(item['batch'])
            coc.append(item['coc'])
    except KeyError as e:
        return JsonResponse({"error": f"Missing key in items: {e}"}, status=400)
    
    try:
        data_inw = CustomerPurchaseOrder.objects.filter(pono=po_no, po_sl_no__in=po_sl_numbers)
    except Exception as e:
        return JsonResponse({"error": e}, status=404)
    
    data_dict_inw = list(data_inw.values())
    df_inw = pd.DataFrame(data_dict_inw)

    if df_inw.empty:
        return JsonResponse({"error": "No matching records in the database"}, status=404)

    if gst_exception is None:
        gst_exception = df_inw.iloc[0].get('gst_exception', gst_exception)

    if freight_charges:
        new_row = {
            'slno': '',
            'pono': '',
            'podate': None,
            'quote_id': '',
            'quote_date': None,
            'customer_id': '',
            'consignee_id': '',
            'po_sl_no': '',
            'prod_code': '',
            'prod_desc': 'Packing forwarding with Freight charges',
            'additional_desc': '',
            'omat': '',
            'pack_size': '',
            'quantity': 1,
            'unit_price': freight_charges,
            'uom': 'No',
            'hsn_sac': '9965',
            'total_price': freight_charges,
            'qty_balance': 1,
            'qty_sent': 1,
            'delivery_date': None,
            'po_validity': None,
            'gst_exception': '',
        }

        po_sl_numbers.append('')
        qty_tobe_del.append(1)
        hsn.append('9965')
        batch.append('')
        coc.append('')
        index_to_insert = len(df_inw)
        df_inw.loc[index_to_insert] = new_row

    if insurance_charges:
        new_row = {
            'slno': '',
            'pono': '',
            'podate': None,
            'quote_id': '',
            'quote_date': None,
            'customer_id': '',
            'consignee_id': '',
            'po_sl_no': '',
            'prod_code': '',
            'prod_desc': 'Insurance Charges',
            'additional_desc': '',
            'omat': '',
            'pack_size': '',
            'quantity': 1,
            'unit_price': insurance_charges,
            'uom': 'No',
            'hsn_sac': '9971',
            'total_price': insurance_charges,
            'qty_balance': 1,
            'qty_sent': 1,
            'delivery_date': None,
            'po_validity': None,
            'gst_exception': '',
        }

        po_sl_numbers.append('')
        qty_tobe_del.append(1)
        hsn.append('9971')
        batch.append('')
        coc.append('')
        index_to_insert = len(df_inw)
        df_inw.loc[index_to_insert] = new_row

    if other_charges:
        new_row = {
            'slno': '',
            'pono': '',
            'podate': None,
            'quote_id': '',
            'quote_date': None,
            'customer_id': '',
            'consignee_id': '',
            'po_sl_no': '',
            'prod_code': '',
            'prod_desc': 'Other Charges',
            'additional_desc': '',
            'omat': '',
            'pack_size': '',
            'quantity': 1,
            'unit_price': other_charges,
            'uom': 'No',
            'hsn_sac': '9971',
            'total_price': other_charges,
            'qty_balance': 1,
            'qty_sent': 1,
            'delivery_date': None,
            'po_validity': None,
            'gst_exception': '',
        }

        po_sl_numbers.append('')
        qty_tobe_del.append(1)
        hsn.append('')
        batch.append('')
        coc.append('')
        index_to_insert = len(df_inw)
        df_inw.loc[index_to_insert] = new_row

    current = d.now()
    current_yyyy = current.year
    current_mm = current.month

    try:
        fin_year = int(get_object_or_404(GstRates, id=1).fin_year)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "GST Rates not found"}, status=404)

    if fin_year < current_yyyy and current_mm > 3:
        fin_year = current_yyyy
        GstRates.objects.filter(id=1).update(fin_yr=fin_year, last_gcn_no=0)
    f_year = fin_year + 1
    fyear = str(f_year)[2:]

    try:
        gcn_no = get_object_or_404(GstRates, id=1).last_gcn_no
        new_gcn_no = gcn_no + 1
    except ObjectDoesNotExist:
        return JsonResponse({"error": "GST Rates not found"}, status=404)

    gcn_num = f"{str(new_gcn_no).zfill(3)}/{str(fin_year)}-{str(fyear)}"

    current_date = current
    date = str(current_date.strftime('%Y-%m-%d'))

    df_inw.rename(columns={"id": "matcode", "cust_id_id": "cust_id"}, inplace=True)

    df_inw["cust_id"] = cust_id
    df_inw["gcn_no"] = gcn_num
    df_inw["gcn_date"] = date
    df_inw["consignee_id"] = cust_id if new_cons_id == '' else new_cons_id

    qty_dict = dict(zip(po_sl_numbers, qty_tobe_del))
    df_inw['qty_tobe_del'] = df_inw['po_sl_no'].map(qty_dict)

    for index, row in df_inw.iterrows():
        print(index, row)
        qty_tobe_del = row['qty_tobe_del']
        qty_balance = row['qty_balance']
        quantity = row['quantity']

        print("\nqty_tobe_del: ", qty_tobe_del)
        print("qty_balance: ", qty_balance)
        print("quantity: ", quantity)

        if qty_tobe_del is not None and qty_balance is not None and quantity is not None:
            if (float(qty_tobe_del) > float(qty_balance)) or (float(qty_tobe_del) > float(quantity)):
                return JsonResponse({"error": "Insufficient Quantity"}, status=400)
        else:
            return JsonResponse({"error": "Quantity information missing"}, status=400)

    try:
        state_code = CustomerMaster.objects.filter(cust_id=cust_id).values_list('cust_st_code', flat=True).first()
        if not state_code:
            return JsonResponse({"error": "State code not found for the given customer id"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    try:
        gst_instance = GstRates.objects.get()
        cgst_r = float(gst_instance.cgst_rate) / 100
        sgst_r = float(gst_instance.sgst_rate) / 100
        igst_r = float(gst_instance.igst_rate) / 100
    except GstRates.DoesNotExist:
        return JsonResponse({"error": "GST Rates not found"}, status=404)

    df_inw["taxable_amt"] = df_inw["qty_tobe_del"].astype(float) * df_inw["unit_price"].astype(float)
    
    if gst_exception:
        if int(state_code) == 29:
            df_inw["cgst_price"] = 0.0
            df_inw["sgst_price"] = 0.0
            df_inw["igst_price"] = 0.0
        else:
            df_inw["cgst_price"] = 0.0
            df_inw["sgst_price"] = 0.0
            df_inw["igst_price"] = 0.0
    else:
        if int(state_code) == 29:
            df_inw["cgst_price"] = cgst_r * df_inw["taxable_amt"].astype(float)
            df_inw["sgst_price"] = sgst_r * df_inw["taxable_amt"].astype(float)
            df_inw["igst_price"] = 0.0
        else:
            df_inw["cgst_price"] = 0.0
            df_inw["sgst_price"] = 0.0
            df_inw["igst_price"] = igst_r * df_inw["taxable_amt"].astype(float)

    df_inw["cgst_price"] = df_inw["cgst_price"].apply(lambda x: '{:.2f}'.format(x))
    df_inw["sgst_price"] = df_inw["sgst_price"].apply(lambda x: '{:.2f}'.format(x))
    df_inw["igst_price"] = df_inw["igst_price"].apply(lambda x: '{:.2f}'.format(x))

    df_inw["qty_sent"] = df_inw["qty_sent"].astype(float) + df_inw["qty_tobe_del"].astype(float)
    df_inw["qty_balance"] = df_inw["qty_balance"].astype(float) - df_inw["qty_tobe_del"].astype(float)

    skip_index = []
    if freight_charges or insurance_charges or other_charges:
        i = 0
        if freight_charges:
            i += 1
            skip_index.append(len(df_inw) - i)
        if insurance_charges:
            i += 1
            skip_index.append(len(df_inw) - i)
        if other_charges:
            i += 1
            skip_index.append(len(df_inw) - i)

    for index, row in df_inw.iterrows():
        try:
            hsn_value = hsn[index]
            batch_value = batch[index]
            coc_value = coc[index]

            max_slno = OtwDc.objects.aggregate(Max('sl_no'))['sl_no__max']
            new_slno = max_slno + 1 if max_slno else 1

            # print("row ", index, ": \n", row)
            OtwDc_instance = OtwDc(
                sl_no=new_slno,
                gcn_no=row.get('gcn_no', ''),
                gcn_date=row.get('gcn_date', ''),
                po_no=row.get('pono', ''),
                po_date=row.get('podate', ''),
                consignee_id=row.get('consignee_id', ''),
                po_sl_no=row.get('po_sl_no', ''),
                prod_id=row.get('prod_code', ''),
                prod_desc=row.get('prod_desc', ''),
                additional_desc=row.get('additional_desc', ''),
                omat=row.get('omat', ''),
                qty_delivered=row.get('qty_tobe_del', ''),
                pack_size=row.get('pack_size', ''),
                unit_price=row.get('unit_price', ''),
                taxable_amt=row.get('taxable_amt', ''),
                cgst_price=row.get('cgst_price', ''),
                sgst_price=row.get('sgst_price', ''),
                igst_price=row.get('igst_price', ''),
                cust_id=row.get('cust_id', ''),
                hsn_sac=hsn_value,
                batch=batch_value,
                coc=coc_value,
                contact_name=contact_name,
                contact_number=contact
            )
            OtwDc_instance.save()
        except KeyError as e:
            print(f"Missing key in row: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

        if index not in skip_index:
            try:
                record = CustomerPurchaseOrder.objects.get(
                    customer_id=row['customer_id'],
                    pono=row['pono'],
                    po_sl_no=row['po_sl_no']
                )
                record.qty_balance = float(record.qty_balance) - float(row['qty_tobe_del'])
                record.qty_sent = float(record.qty_sent) + float(row["qty_tobe_del"])
                record.save()
            except ObjectDoesNotExist:
                return JsonResponse({"error": f"Record with cust_id={row['customer_id']}, po_sl_no={row['po_sl_no']} does not exist."}, status=404)

    GstRates.objects.filter(id=1).update(last_gcn_no=new_gcn_no)

    return JsonResponse({"success": True, "gcn_no": new_gcn_no})


@csrf_exempt
def invoice_generation(request):
    if request.method == "GET":
        gcn_no = request.GET.get("gcn_no")
        if not gcn_no:
            return JsonResponse({"error": "GCN number is required"}, status=400)
        
        # Derive the complete gcn_no for this invoice
        gst_rate = get_object_or_404(GstRates, id=1)
        fin_year = int(gst_rate.fin_year)
        f_year = fin_year + 1
        fyear = str(f_year)[2:]
        # gcn_no = gst_rate.last_gcn_no
        print("gcn_no: ", gcn_no)
        gcn_num = f"{str(gcn_no).zfill(3)}/{fin_year}-{fyear}"

        print("gcn_num: ", gcn_num)
        # Get data from otw_dc table
        otwdc_values = OtwDc.objects.filter(gcn_no=gcn_num)
        print("otwdc_values: ", otwdc_values.values())
        if not otwdc_values.exists():
            return JsonResponse({"error": "No records found for the provided GCN number"}, status=404)

        def model_to_dic(instance):
            return {
                'sl_no': instance.sl_no,
                'gcn_no': instance.gcn_no,
                'gcn_date': str(instance.gcn_date),  # Convert date to string
                'po_no': instance.po_no,
                'po_date': str(instance.po_date),  # Convert date to string
                'cust_id': instance.cust_id,
                'consignee_id': instance.consignee_id,
                'prod_id': instance.prod_id,
                'po_sl_no': instance.po_sl_no,
                'prod_desc': instance.prod_desc,
                'additional_desc': instance.additional_desc,
                'omat': instance.omat,
                'hsn': instance.hsn_sac,
                'batch': instance.batch,
                'coc': instance.coc,
                'qty_delivered': instance.qty_delivered,
                'pack_size': instance.pack_size,
                'unit_price': instance.unit_price,
                'taxable_amt': instance.taxable_amt,
                'cgst_price': instance.cgst_price,
                'sgst_price': instance.sgst_price,
                'igst_price': instance.igst_price,
                "contact_name": instance.contact_name
            }

        otwdc_result = [model_to_dic(otwdc_value) for otwdc_value in otwdc_values]

        odc1 = otwdc_values.first()
        
        r = get_object_or_404(CustomerMaster, cust_id=odc1.cust_id)
        c = get_object_or_404(CustomerMaster, cust_id=odc1.consignee_id)
        
        total_qty = otwdc_values.aggregate(total_qty=Sum('qty_delivered'))['total_qty'] or 0
        total_taxable_value = otwdc_values.aggregate(total_taxable_value=Sum('taxable_amt'))['total_taxable_value'] or 0
        total_cgst = otwdc_values.aggregate(total_cgst=Sum('cgst_price'))['total_cgst'] or 0
        total_sgst = otwdc_values.aggregate(total_sgst=Sum('sgst_price'))['total_sgst'] or 0
        total_igst = otwdc_values.aggregate(total_igst=Sum('igst_price'))['total_igst'] or 0

        grand_total = round(total_taxable_value + total_cgst + total_sgst + total_igst)
        gt = format_currency(grand_total, 'INR', locale='en_IN')
        aw = convert_rupees_to_words(grand_total)

        context = {
            'odc': otwdc_result,
            'r': model_to_dict(r),
            'c': model_to_dict(c),
            'gr': model_to_dict(gst_rate),
            'odc1': model_to_dict(odc1),
            'amount': aw,
            'total_taxable_value': "{:.2f}".format(total_taxable_value),
            'total_cgst': "{:.2f}".format(total_cgst),
            'total_sgst': "{:.2f}".format(total_sgst),
            'total_igst': "{:.2f}".format(total_igst),
            'gt': gt,
            'total_qty': total_qty
        }
        return JsonResponse({"message": "success", "context": context}, safe=False)
    else:
        return JsonResponse({"error": "Only GET requests are allowed"}, status=405)

def get_invoice_data(request):
    if request.method == 'GET': 
        try:
            po_no = request.GET.get("poNo")
            if po_no:
                result = CustomerPurchaseOrder.objects.filter(pono=po_no)
                result_first = result.first()  
                
                if not result_first:
                    return JsonResponse({"error": "No matching CustomerPurchaseOrder found"}, status=404)
                
                contact = CustomerMaster.objects.filter(cust_id=result_first.customer_id).values()
                
                if contact.exists():
                    contact_names = [
                        contact[0].get('contact_name_1'),
                        contact[0].get('contact_name_2')
                    ]
                else:
                    contact_names = [None, None]
                    
                print('contact: ', contact_names)
                
                cust_id = result_first.customer_id
                consignee_id = result_first.consignee_id
                invoice_header_data = {
                    'customerId': cust_id,
                    'consigneeId': consignee_id,
                    'contact_names': contact_names
                }
                
                # Serialize the result queryset to a list of dictionaries
                result_data = list(result.values())
                
                result_data = list(result.values())
                filtered_result_data = [
                    {
                        'poNo': item['pono'],
                        'po_sl_no': item['po_sl_no'],
                        'unit_price': item['unit_price'],
                        'prod_code': item['prod_code'],
                        'prod_desc': item['prod_desc'], 
                        'hsnSac': item['hsn_sac']
                    }
                    for item in result_data
                ]
                return JsonResponse({"success": True, "invoice_header_data": invoice_header_data, "result": filtered_result_data})
            else:
                return JsonResponse({"error": "po_no parameter is missing"}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Object does not exist"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Only GET requests are allowed"}, status=405)

@api_view(["GET"])
def get_state_data(request):
    try:
        print('entered')
        state_data = GstStateCode.objects.all().values().order_by('state_name')
        return JsonResponse({"success": True, "state_data": list(state_data)})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})

@api_view(["GET"])
def get_customer_data(request):
    try:
        print('entered')
        customer_data = CustomerMaster.objects.all().values().order_by('cust_id')
        return JsonResponse({"success": True, "customerData": list(customer_data)})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
    
@api_view(["GET"])
def get_purchase_order(request):
    try:
        print('entered')
        # state_data = CustomerPurchaseOrder.objects.all().distinct().values()
        distinct_pono = list(CustomerPurchaseOrder.objects.values('pono').distinct().order_by('pono'))
        return JsonResponse({"success": True, "distinct_pono": distinct_pono})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
    
@api_view(["GET"])
def get_product_data(request):
    try:
        print('entered')
        product_data = SupplierProductMaster.objects.all().values()
        return JsonResponse({"success": True, "products": list(product_data)})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})

@csrf_exempt
def invoice_report(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            start_date_str = data.get('startDate')
            end_date_str = data.get('endDate')

            start_datetime = datetime.strptime(start_date_str, "%d-%m-%Y")
            end_datetime = datetime.strptime(end_date_str, "%d-%m-%Y")
            print("start_datetime: ", start_datetime)
            start_date = start_datetime.date()
            end_date = end_datetime.date()

            result = OtwDc.objects.filter(gcn_date__range=(start_date, end_date)).select_related('cust_id').values(
                'gcn_no', 'gcn_date', 'qty_delivered', 'taxable_amt', 'cgst_price', 'sgst_price', 'igst_price',
                'cust_id__cust_name', 'cust_id__cust_gst_id', 'hsn_sac'
            ).order_by('gcn_date')

            df = pd.DataFrame(result, columns=['gcn_no', 'gcn_date', 'qty_delivered', 'taxable_amt', 'cgst_price', 'sgst_price', 'igst_price', 'cust_id__cust_name', 'cust_id__cust_gst_id', 'hsn_sac'])
            df = df[['cust_id__cust_name', 'cust_id__cust_gst_id', 'gcn_no', 'gcn_date', 'hsn_sac', 'qty_delivered', 'taxable_amt', 'cgst_price', 'sgst_price', 'igst_price']]

            df.insert(0, 'Sl No', range(1, len(df) + 1))
            df = df.rename(columns={
                'gcn_no': 'Invoice Number',
                'gcn_date': 'Invoice Date',
                'hsn_sac': 'HSN/SAC',
                'qty_delivered': 'Quantity',
                'taxable_amt': 'Ass.Value',
                'cgst_price': 'CGST Price (9%)',
                'sgst_price': 'SGST Price (9%)',
                'igst_price': 'IGST Price (18%)',
                'cust_id__cust_name': 'Customer Name',
                'cust_id__cust_gst_id': 'Customer GST Num',
            })

            grouped = df.groupby(['Invoice Number', 'Invoice Date', 'HSN/SAC']).agg({
                'Quantity': 'sum',
                'Ass.Value': 'sum',
                'CGST Price (9%)': 'sum',
                'SGST Price (9%)': 'sum',
                'IGST Price (18%)': 'sum'
            }).reset_index()

            df1 = df[['Invoice Number', 'Customer Name', 'Customer GST Num', 'HSN/SAC']].drop_duplicates()

            combined_df = pd.merge(df1, grouped, on=['Invoice Number', 'HSN/SAC'], how='left')
            combined_df['Sl No'] = range(1, len(combined_df) + 1)

            total_taxable_amt = grouped['Ass.Value'].sum()
            total_cgst_price = grouped['CGST Price (9%)'].sum()
            total_sgst_price = grouped['SGST Price (9%)'].sum()
            total_igst_price = grouped['IGST Price (18%)'].sum()

            combined_df['Invoice Date'] = pd.to_datetime(combined_df['Invoice Date'], errors='coerce').dt.date
            combined_df['Invoice Date'] = pd.to_datetime(combined_df['Invoice Date'], format='%Y-%m-%d').dt.strftime('%d-%m-%Y')
            combined_df['Invoice Date'] = combined_df['Invoice Date'].astype(str)

            total_row = pd.DataFrame({
                'Sl No': 'Total',
                'Customer Name': '',
                'Customer GST Num': '',
                'Invoice Date': '',
                'Invoice Number': '',
                'HSN/SAC': '',
                'Quantity': '',
                'Ass.Value': total_taxable_amt,
                'CGST Price (9%)': total_cgst_price,
                'SGST Price (9%)': total_sgst_price,
                'IGST Price (18%)': total_igst_price,
                'Round Off': '',
            }, index=[0])

            combined_df = pd.concat([combined_df, total_row], ignore_index=True)

            combined_df['Invoice Value'] = combined_df['Ass.Value'] + combined_df['IGST Price (18%)'] + combined_df['CGST Price (9%)'] + combined_df['SGST Price (9%)']
            combined_df['Invoice Value'] = pd.to_numeric(combined_df['Invoice Value']).round()

            combined_df['Round Off'] = combined_df.apply(
                lambda row: float(row['Invoice Value']) - (
                    float(row['Ass.Value']) +
                    float(row['IGST Price (18%)']) +
                    float(row['CGST Price (9%)']) +
                    float(row['SGST Price (9%)'])
                ) if row['Sl No'] != 'Total' else None,
                axis=1
            )

            combined_df[['Ass.Value', 'IGST Price (18%)', 'CGST Price (9%)', 'SGST Price (9%)', 'Invoice Value', 'Round Off']] = combined_df[['Ass.Value', 'IGST Price (18%)', 'CGST Price (9%)', 'SGST Price (9%)', 'Invoice Value', 'Round Off']].apply(lambda x: x.map('{:.2f}'.format))

            combined_df.loc[combined_df['Sl No'] == 'Total', ['Round Off', 'HSN/SAC']] = ''

            column_order = ['Sl No', 'Customer Name', 'Customer GST Num', 'Invoice Number', 'Invoice Date', 'HSN/SAC', 'Quantity', 'Ass.Value', 'IGST Price (18%)', 'CGST Price (9%)', 'SGST Price (9%)', 'Invoice Value', 'Round Off']
            combined_df = combined_df[column_order]
            print("df")

            with pd.ExcelWriter('invoiceReports.xlsx', engine='xlsxwriter') as excel_writer:
                combined_df.to_excel(excel_writer, index=False)

            json_data = combined_df.to_json(orient='records')
            print(json_data, "json data")

            return JsonResponse(json.loads(json_data), safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    token = request.GET.get("token")
    user = request.GET.get("user")
    # return Response("passed!", {token: token, valid: True})
    return JsonResponse({"valid": True, "token": token, "user": user})

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    # Delete the token
    request.user.auth_token.delete()
    return Response("Logged out successfully!")