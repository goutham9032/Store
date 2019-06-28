import json
from datetime import datetime

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import (HttpResponse, HttpResponseRedirect, JsonResponse)

from app.models import Discount, Store, Products, StoreDiscount

@csrf_exempt
def create_discount(request):
    body = json.loads(request.body.decode())
    start_date = body['start_date']
    end_date = body['end_date']
    products = list(map(lambda x:x['name'], body['ProductCategory']))
    product_list = Products.objects.filter(product_name__in=products)
    start_date_obj = datetime.strptime(start_date, '%d-%m-%Y')
    end_date_obj = datetime.strptime(end_date, '%d-%m-%Y')
    if start_date_obj > end_date_obj:
       return JsonResponse({'success':False, 'result':'start date is greatee than end date'})
    discount = Discount.objects.create(start_date=start_date_obj, end_date=end_date_obj)
    for pr in product_list:
        discount.products.add(pr)
    res = {'discountId':discount.id,
           'start_date':start_date,
           'end_date':end_date,
           'ProductCategory':list(discount.products.all().values('product_name','id'))}
    return JsonResponse({'success':True, 'data':res})

@csrf_exempt
def all_discounts(request):
    discounts = Discount.objects.all()
    lis = []
    for disc in discounts:
        dic  = {'discountId':disc.id,
                'start_date':disc.start_date.strftime('%d-%m-%Y'),
                'end_date':disc.end_date.strftime('%d-%m-%Y'),
                'ProductCategory':list(disc.products.all().values('product_name','id')),
               }
        lis.append(dic)
    return JsonResponse({'success':True, 'result':lis})

@csrf_exempt
def map_discount_store(request):
    if request.method == 'GET':
        pass # Todo : need to write for get request
    body = json.loads(request.body.decode())
    disc_id = body['discountId']
    stores = list(map(lambda x:x['name'], body['storeId']))
    stores_list = Store.objects.filter(store_name__in=stores)
    disc_obj = Discount.objects.get(id=disc_id)
    disc_start_date = disc_obj.start_date
    disc_end_date = disc_obj.end_date

    already_mapped = []
    for store in stores_list:
        objs = list(StoreDiscount.objects.filter(store=store).values('discount__start_date',
                                            'discount__end_date',
                                            'store__store_name','discount__id'))
        for obj in objs:
            start = obj['discount__start_date']
            end = obj['discount__start_date']
            if (disc_start_date >= start and disc_start_date <= end) or (disc_end_date >= start and disc_end_date <= end):
                dis_id = obj['discount__id']
                products = list(Discount.objects.filter(id=dis_id).values('products__id','products__product_name'))
                dic = {'storeId':store.id,
                       'productsCatagery':products,
                       'discount_id':dis_id,
                       'start_time':start.strftime('%d-%m-%Y'),
                       'end_time':end.strftime('%d-%m-%Y')}
                already_mapped.append(dic)
    if already_mapped:
        return JsonResponse({'success':False, 'discount_exists':already_mapped})

    res = []
    for store in stores_list:
        StoreDiscount.objects.create(store=store, discount=disc_obj)
        res.append({'name':store.store_name})
    return JsonResponse({'success':True, 'result':[{'discountId':disc_obj.id, 'storeId':res}]})













