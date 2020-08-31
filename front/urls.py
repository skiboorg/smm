from django.urls import path
from . import views
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', views.index, name='articles'),
    path('order/<network_id>', views.order, name='order'),
    path('new_order', views.new_order, name='new_order'),
    path('status/<order_id>', views.status, name='status'),

   


]