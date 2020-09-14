import decimal
import json
from datetime import datetime,timedelta
import requests
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from cp.models import *
import settings
from django.utils.http import urlquote
from urllib.request import urlopen
from xml.etree.ElementTree import parse

def index(request):
    pageTitle = 'SMM'
    pageDescription = 'SMM'
    networks = SocialNetwork.objects.all()
    if request.GET.get('pay_complete'):
        try:
            order = Order.objects.get(uu=request.GET.get('pay_complete'))
            if not order.is_payed:
                order.is_payed=True
                order.save()
        except:
            pass

    return render(request, 'front/index.html', locals())

def status(request,order_id):
    pageTitle = 'SMM'
    pageDescription = 'SMM'
    order = Order.objects.get(uu=order_id)
    return render(request, 'front/status.html', locals())
def new_order(request):
    request_unicode = request.body.decode('utf-8')
    request_body = json.loads(request_unicode)
    print(request_body)
    var_url = urlopen('https://www.cbr-xml-daily.ru/daily_utf8.xml')
    xmldoc = parse(var_url)
    rate = 1
    # for item in xmldoc.iterfind('Valute'):
    #     title = item.findtext('CharCode')
    #     if title == 'AZN':
    #         rate = item.findtext('Value')
    #         print(rate)
    #         continue
    # rate=rate.replace(',','.')
    total_cost=decimal.Decimal(request_body['total_cost']) * decimal.Decimal(rate)
    total_cost = f'{"{:.2f}".format(round(float(total_cost), 2))}'
    print(total_cost)
    network=SocialNetwork.objects.get(id=request_body['network_id'])

    print(network)
    service = Service.objects.get(id=request_body['service'])

    print(service)
    tarif = Tarif.objects.get(id=request_body['tarif'])
    print(tarif)

    new_order=Order.objects.create(social_network=network,
                         service=service,
                         tarif=tarif,
                         text=request_body['text'],
                         total_number=request_body['total_number'],
                         url=request_body['url'],
                         email=request_body['email'],
                         total_cost=decimal.Decimal(request_body['total_cost']),
                         )
    print('order created')
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
        "comment": f'Оплата услуги {new_order.service.name}',
        "expirationDateTime": f"{(datetime.now() + timedelta(hours=3)).strftime('%Y-%m-%dT%H:%M:%S+03:00')}",
        "customer": {
            'email': request_body['email'],
            'account': new_pay.id,
        },
        "customFields": {},
    }
    respond = requests.put(f'https://api.qiwi.com/partner/bill/v1/bills/{new_pay.id}', headers=headers,
                           data=json.dumps(data))
    print(respond.json())
    pay_url = respond.json()['payUrl']
    return_url = urlquote(u'{}?pay_complete={}'.format(settings.SUCCES_URL, new_order.uu))
    full_url = f'{pay_url}&paySource=card&allowedPaySources=qw,card&successUrl={return_url}'

    return JsonResponse({'url':full_url}, safe=False)

def order(request,network_id):
    pageTitle = 'SMM-Order'
    pageDescription = 'SMM'
    network = get_object_or_404(SocialNetwork,id=network_id)
    return render(request, 'front/order.html', locals())
