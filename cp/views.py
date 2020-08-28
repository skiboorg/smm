from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, logout,authenticate
from django.http import  HttpResponseRedirect
from .forms import *

def cp_index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/cp/orders')
    else:
        return HttpResponseRedirect('/cp/login')

@login_required
def cp_orders(request):
    pageTitle = 'SMM-Orders'
    pageDescription = 'SMM'
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

def cp_networks(request):
    pageTitle = 'SMM-All Networks'
    pageDescription = 'SMM'
    networks = SocialNetwork.objects.all()
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