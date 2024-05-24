from django.http import HttpResponse
from django.shortcuts import render
from .models import SupplierProductMaster, CustomerMaster, CustomerPurchaseOrder, GstRates, GstStateCode, OtwDc
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Max, F
from django.db import transaction, DatabaseError, connection
import pandas as pd
from django.shortcuts import get_object_or_404
import datetime as d

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
    
@csrf_exempt
def invoice_processing(request):
    data = json.loads(request.body.decode('utf-8'))
    
    po_no = data.get('poNo')
    cust_id = data.get('customerId')
    new_cons_id = data.get('newConsigneeName')

    po_sl_numbers = []
    qty_tobe_del = []
    
    for item in data['items']:
        po_sl_numbers.append(item['po_sl_no'])
        qty_tobe_del.append(item['quantity'])
    
    # Creating a dataframe with the relevant Inw Delivery records
    data_inw = CustomerPurchaseOrder.objects.filter(pono=po_no, po_sl_no__in=po_sl_numbers)
    data_dict_inw = list(data_inw.values())
    print(data_dict_inw)
    df_inw = pd.DataFrame(data_dict_inw)
    # print("Columns",df_inw.columns)

    # Checking if the Inward DC is valid
    if df_inw.empty:
        print(f"Purchase Order No '{po_no}' does not exist in the database.")
        return JsonResponse({"message": 'po_no does not exists'})

    # # Checking the validity if Open PO 
    # grn_date = df_inw.iloc[0]['grn_date']
    # po_no = df_inw.iloc[0]['po_no']
    
    # for po_sl_no in po_sl_numbers:
    #     open_po = get_object_or_404(CustomerPurchaseOrder, cust_id = cust_id, po_no=po_no,po_sl_no=po_sl_no).open_po
    #     open_po_validity = get_object_or_404(CustomerPurchaseOrder, cust_id = cust_id, po_no=po_no,po_sl_no=po_sl_no).open_po_validity
    #     if (open_po) :
    #         if grn_date > open_po_validity:
    #             print("Expired Open PO")
    #             return ('open_po_validity')

    # Checking for the current financial year and resetting gcn_no for new fin_year
    current= d.datetime.now()
    current_yyyy = current.year
    current_mm = current.month
    fin_year = int(get_object_or_404(GstRates, id=1).fin_year)

    if  fin_year < current_yyyy and current_mm >3:
        fin_year=current_yyyy
        GstRates.objects.filter(id=1).update(fin_yr=fin_year, last_gcn_no = 0)
    f_year=fin_year+1
    fyear=str(f_year)
    fyear=fyear[2:]

    # Derive the new gcn_no for this invoice
    gcn_no = get_object_or_404(GstRates,id=1).last_gcn_no
    # print("Prev Invoice No:", gcn_no)
    new_gcn_no = gcn_no + 1
    # print("Current Invoice No:", new_gcn_no)

    # rework_dc = df_inw.iloc[0]['rework_dc']
    # if (rework_dc):
    #     flag='R'
    # else:
    #     flag=''    
    gcn_num = (str(new_gcn_no).zfill(3)+ "/" + str(fin_year)+"-"+str(fyear))
        
    current_date = current
    date = str(current_date.strftime('%Y-%m-%d'))

    # Populating the columns with values for updating the Outward_Delivery Table
    df_inw.rename(columns={"id": "matcode", "cust_id_id": "cust_id"}, inplace=True)

    df_inw["cust_id"] = cust_id
    df_inw["gcn_no"] = gcn_num
    df_inw["gcn_date"] = date
    df_inw["consignee_id"] = cust_id if (new_cons_id == '') else new_cons_id

    # Getting the corresponding 'qty_tobe_del' for the po_sl_no
    qty_dict = dict(zip(po_sl_numbers, qty_tobe_del))
    df_inw['qty_tobe_del'] = df_inw['po_sl_no'].map(qty_dict)

    #Checking if 'qty_tobe_del' <= 'qty_balance' for all items
    for index, row in df_inw.iterrows():
        qty_tobe_del = row['qty_tobe_del']
        qty_balance = row['qty_balance']
        
        quantity = row['quantity']
        if qty_tobe_del is not None and qty_balance is not None and quantity is not None:
            if (int(qty_tobe_del) > int(qty_balance)) or (int(qty_tobe_del) > int(quantity)):
                print("ERROR: Insufficient Quantity")
                return JsonResponse({"error": "Insufficient Quantity"})
        else:
            print("ERROR: Quantity information missing")
            return JsonResponse({"error": "Quantity information missing"})


    # Getting GST Rates from the table
    gst_instance = GstRates.objects.get()
    cgst_r = float(gst_instance.cgst_rate)/100
    sgst_r = float(gst_instance.sgst_rate)/100
    igst_r = float(gst_instance.igst_rate)/100
    
    # Calculate the taxable_amt and GST for each items based on the State_Code
    df_inw["taxable_amt"] = df_inw["qty_tobe_del"].astype(float) * df_inw["unit_price"].astype(float)

    # # Setting taxable_amt to zero for rejected items
    # # df_inw["taxable_amt"] = 0.0 if ritem else df_inw["taxable_amt"]
    
    state_code = CustomerMaster.objects.filter(cust_id=cust_id).values_list('cust_st_code', flat=True).first()

    if state_code == 29:
        df_inw["cgst_price"] = cgst_r * (df_inw["taxable_amt"].astype(float))
        df_inw["sgst_price"] = sgst_r * (df_inw["taxable_amt"].astype(float))
        df_inw["igst_price"] = 0.0
    else:
        df_inw["cgst_price"] = 0.0
        df_inw["sgst_price"] = 0.0
        df_inw["igst_price"] = igst_r * (df_inw["taxable_amt"].astype(float))

    # Format the result
    df_inw["cgst_price"] = df_inw["cgst_price"].apply(lambda x: '{:.2f}'.format(x))
    df_inw["sgst_price"] = df_inw["sgst_price"].apply(lambda x: '{:.2f}'.format(x))
    df_inw["igst_price"] = df_inw["igst_price"].apply(lambda x: '{:.2f}'.format(x))
    
    

    # Updating the qty_delivered and qty_balance for Inward DC
    df_inw["qty_sent"] = df_inw["qty_sent"].astype(float) + df_inw["qty_tobe_del"].astype(float)
    df_inw["qty_balance"] = df_inw["qty_balance"].astype(float) - df_inw["qty_tobe_del"].astype(float)

    
    # Insert Outward_DC table with new records
    # Iterate over each row in the DataFrame
    for index, row in df_inw.iterrows():
        max_slno = CustomerPurchaseOrder.objects.aggregate(Max('sl_no'))['sl_no__max']
        new_slno = max_slno + 1 if max_slno else 1
        OtwDc_instance = OtwDc(
            id = new_slno,
            gcn_no   = row['gcn_no'],
            gcn_date = row['gcn_date'],
            po_no    = row['pono'],
            po_date  = row['podate'],
            consignee_id = row['consignee_id'],
            po_sl_no = row['po_sl_no'],
            prod_id = row['prod_code'],
            additional_desc = row['additional_desc'],
            qty_delivered = row['qty_tobe_del'],
            pack_size = row['pack_size'],
            unit_price = row['unit_price'],
            taxable_amt = row['taxable_amt'],
            cgst_price = row['cgst_price'],
            sgst_price = row['sgst_price'],
            igst_price = row['igst_price'],
            cust_id = row['cust_id']
        )
        # Save the instance to the database
        OtwDc_instance.save()

    # # Update Inward_DC table with new qty_delivered & qty_balance
    # for index, row in df_inw.iterrows():
    #     try:
    #         # Retrieve the record from the database table
    #         record = CustomerPurchaseOrder.objects.get(
    #             cust_id = row['cust_id'],
    #             grn_no  = row['grn_no'],
    #             po_sl_no= row['po_sl_no']
    #         )
            
    #         # Update the record
    #         record.qty_delivered = F('qty_delivered') + row['qty_tobe_del']
    #         record.qty_balance   = F('qty_balance') - row['qty_tobe_del']
    #         record.save()
            
    #     except ObjectDoesNotExist:
    #         # If the record doesn't exist, raise an error
    #         raise Exception(f"Record with cust_id={row['cust_id']}, po_sl_no={row['po_sl_no']} does not exist.")
    #         return

    # # Update PO table with new qty_sent values
    # for index, row in df_inw.iterrows():
    #     try:
    #         # Retrieve the record from the database table
    #         record = CustomerPurchaseOrder.objects.get(
    #             cust_id = row['cust_id'],
    #             po_no   = row['po_no'],
    #             po_sl_no= row['po_sl_no']
    #         )
            
    #         # Update the record
    #         record.qty_sent = F('qty_sent') + row['qty_tobe_del']
    #         record.save()
            
    #     except ObjectDoesNotExist:
    #         # If the record doesn't exist, raise an error
    #         raise Exception(f"Record with cust_id={row['cust_id']}, po_no={row['po_no']}, po_sl_no={row['po_sl_no']} does not exist.")
    #         return
    
    # # Update the last_gcn_no in mat_company table
    # GstRates.objects.filter(id=1).update(last_gcn_no = new_gcn_no)

    # # Returning with success message
    # response_data = {'message': 'success','gcn_no': gcn_num, }
    # print(type(response_data))
    # return response_data 
    
    
    return JsonResponse({"success": True})