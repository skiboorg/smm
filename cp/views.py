import json
import decimal
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, logout,authenticate
from django.http import  HttpResponseRedirect
from .forms import *
from .serializers import *
from django.http import JsonResponse

def cp_index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/cp/orders')
    else:
        return HttpResponseRedirect('/cp/login')

@login_required
def cp_orders(request):
    pageTitle = 'SMM-Orders'
    pageDescription = 'SMM'
    networks = SocialNetwork.objects.all()
    orders = Order.objects.filter(is_payed=True)
    statuses = Status.objects.all()
    cur_network_id=0

    if request.GET.get('filter'):


        if request.GET.get('network') != '0':
            cur_network = SocialNetwork.objects.get(id=request.GET.get('network'))
            cur_network_id = cur_network.id
            cur_services = Service.objects.filter(social_network=cur_network)
            orders = orders.filter(social_network_id=request.GET.get('network'))

        if request.GET.get('service') != '0':
            orders = orders.filter(service_id=request.GET.get('service'))

        if request.GET.get('status') != '0':
            orders = orders.filter(status_id=request.GET.get('status'))


    else:

        if request.GET.get('network'):
            cur_network = SocialNetwork.objects.get(id=request.GET.get('network'))
            cur_network_id = cur_network.id
            cur_services = Service.objects.filter(social_network=cur_network)


    return render(request, 'cp/orders.html', locals())

def cp_login(request):
    pageTitle = 'SMM-Login'
    pageDescription = 'SMM'
    if request.POST:
        user = authenticate(username=request.POST.get('login'), password=request.POST.get('password'))

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/cp/orders')
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'cp/login.html', locals())

def cp_restore(request):
    pageTitle = 'SMM-Restore'
    pageDescription = 'SMM'
    return render(request, 'cp/restore.html', locals())

def cp_del_tarif(request,tarif_id):
    tarif = Tarif.objects.get(id=tarif_id)
    tarif.delete()
    return HttpResponseRedirect(f'/cp/service/{tarif.service.id}')
def cp_edit_tarif(request,tarif_id):
    if request.POST:
        print(tarif_id)
        form = TarifAddForm(request.POST, instance=Tarif.objects.get(id=tarif_id))
        if form.is_valid():
            new_tarif = form.save()
            return HttpResponseRedirect(f'/cp/service/{new_tarif.service.id}')
        else:
            print(form.errors)
    pageTitle = 'SMM-Add Tarif'
    pageDescription = 'SMM'
    form = TarifAddForm()
    tarif = Tarif.objects.get(id=tarif_id)
    service = tarif.service
    return render(request, 'cp/edit_tarif.html', locals())
def cp_add_tarif(request,service_id):
    if request.POST:
        print(request.POST)
        form = TarifAddForm(request.POST, request.FILES)
        if form.is_valid():
            new_tarif = form.save(commit=False)
            new_tarif.service_id = request.POST.get('service_id')
            new_tarif.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print(form.errors)
    pageTitle = 'SMM-Add Tarif'
    pageDescription = 'SMM'
    service = get_object_or_404(Service,id=service_id)
    form = TarifAddForm()
    return render(request, 'cp/add_tarif.html', locals())

def cp_service(request,service_id):

    service = get_object_or_404(Service,id=service_id)
    pageDescription = 'SMM'
    pageTitle = f'SMM-{service.name}'
    return render(request, 'cp/service.html', locals())


def cp_del_network(request,network_id):
    network = get_object_or_404(SocialNetwork, id=network_id)
    network.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def cp_del_service(request,service_id):
    service = get_object_or_404(Service, id=service_id)
    service.delete()
    return HttpResponseRedirect('/cp/add_network')

def cp_add_service(request,network_id):
    network = get_object_or_404(SocialNetwork,id=network_id)
    print(network)
    if request.POST:
        Service.objects.create(social_network_id=request.POST.get('network_id'),name=request.POST.get('name'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'cp/add_service.html', locals())

def update_status(request):
    request_unicode = request.body.decode('utf-8')
    request_body = json.loads(request_unicode)
    print(request_body)
    order = Order.objects.get(id=request_body['order_id'])
    order.status_id = int(request_body['status_id'])
    order.save()
    return JsonResponse({'status': 'ok'})
def cp_networks_update(request):
    request_unicode = request.body.decode('utf-8')
    request_body = json.loads(request_unicode)

    network = SocialNetwork.objects.get(id=request_body['network_id'])
    if request_body['data']['discount']!='':
        network.discount = int(request_body['data']['discount'])
    else:
        network.discount = 0
    network.slogan = request_body['data']['slogan']
    network.save()

    for service in request_body['data']['services']:
        print(service['id'])
        service_obj = Service.objects.get(id=service['id'])
        tarif_obj = Tarif.objects.get(id=service_obj.tarifs.first().id)
        tarif_obj.price = decimal.Decimal(service['price'])
        tarif_obj.price_w_discount = decimal.Decimal(service['price_w_discount'])
        tarif_obj.save()
    return JsonResponse({'status': 'ok'})


class Cp_get_networks(generics.ListAPIView):
    queryset = SocialNetwork.objects.all()
    serializer_class = NetworksSerializer

class Cp_get_network(generics.RetrieveAPIView):
    queryset = SocialNetwork.objects.filter()
    serializer_class = NetworkSerializer


def cp_networks(request):
    pageTitle = 'SMM-All Networks'
    pageDescription = 'SMM'

    return render(request, 'cp/networks.html', locals())
def cp_add_network(request):
    if request.POST:
        print(request.POST)
        form = SocialNetworkAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print(form.errors)
    pageTitle = 'SMM-ADD Network'
    pageDescription = 'SMM'
    allNetworks = SocialNetwork.objects.all()
    form = SocialNetworkAddForm()
    return render(request, 'cp/add_network.html', locals())