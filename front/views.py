import decimal
import json

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from cp.models import SocialNetwork,Order

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
    Order.objects.create(social_network_id=request_body['network_id'],
                         service_id=request_body['service'],
                         tarif_id=request_body['tarif'],
                         total_number=request_body['total_number'],
                         url=request_body['url'],
                         email=request_body['email'],
                         total_cost=decimal.Decimal(request_body['total_cost']),
                         )
    return JsonResponse({'status': 'ok'})

def order(request,network_id):
    pageTitle = 'SMM-Order'
    pageDescription = 'SMM'
    network = get_object_or_404(SocialNetwork,id=network_id)
    return render(request, 'front/order.html', locals())
