import decimal
import json
from datetime import datetime,timedelta
import requests
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from cp.models import SocialNetwork,Order,Payment
import settings
from django.utils.http import urlquote
from urllib.request import urlopen
from xml.etree.ElementTree import parse

def index(request):
    pageTitle = 'SMM'
    pageDescription = 'SMM'
    networks = SocialNetwork.objects.all()
    return render(request, 'front/index.html', locals())

def status(request,order_id):
    pageTitle = 'SMM'
    pageDescription = 'SMM'
    order = Order.objects.get(id=order_id)
    return render(request, 'front/status.html', locals())
def new_order(request):
    request_unicode = request.body.decode('utf-8')
    request_body = json.loads(request_unicode)
    print(request_body)
    var_url = urlopen('https://www.cbr-xml-daily.ru/daily_utf8.xml')
    xmldoc = parse(var_url)
    rate = 45
    for item in xmldoc.iterfind('Valute'):
        title = item.findtext('CharCode')
        if title == 'AZN':
            rate = item.findtext('Value')
            print(rate)
            continue
    rate=rate.replace(',','.')
    total_cost=decimal.Decimal(request_body['total_cost']) * decimal.Decimal(rate)
    total_cost = f'{"{:.2f}".format(round(float(total_cost), 2))}'
    print(total_cost)
    new_order=Order.objects.create(social_network_id=request_body['network_id'],
                         service_id=request_body['service'],
                         tarif_id=request_body['tarif'],
                         total_number=request_body['total_number'],
                         url=request_body['url'],
                         email=request_body['email'],
                         total_cost=decimal.Decimal(request_body['total_cost']),
                         )
    new_pay = Payment.objects.create(order=new_order,
                                     amount=float(request_body['total_cost'])
                                     )
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        "Authorization": f'Bearer {settings.QIWI_SECRET}'
    }
    print('data',(datetime.now() + timedelta(hours=3)).strftime('%Y-%m-%dT%H:%M:%S+03:00'))
    data = {
        "amount": {
            "currency": "RUB",
            "value": total_cost #f'{"{:.2f}".format(round(float(request_body["total_cost"]), 2))}'
        },
        "comment": f'Пополнение счета {request.user.first_name} {request.user.last_name}. Номер : {new_pay.id}',
        "expirationDateTime": f"{(datetime.now() + timedelta(hours=3)).strftime('%Y-%m-%dT%H:%M:%S+03:00')}",
        "customer": {
            'email': request_body['email'],
            'account': request_body['email'],
        },
        "customFields": {},
    }
    respond = requests.put(f'https://api.qiwi.com/partner/bill/v1/bills/{new_pay.id}', headers=headers,
                           data=json.dumps(data))
    print(respond.json())
    pay_url = respond.json()['payUrl']
    return_url = urlquote(u'{}qiwi&pid={}'.format(settings.SUCCES_URL, new_pay.payment_id))
    full_url = f'{pay_url}&paySource=qw&allowedPaySources=qw&successUrl={return_url}'

    return JsonResponse({'url':full_url}, safe=False)

def order(request,network_id):
    pageTitle = 'SMM-Order'
    pageDescription = 'SMM'
    network = get_object_or_404(SocialNetwork,id=network_id)
    return render(request, 'front/order.html', locals())
