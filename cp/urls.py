from django.urls import path
from . import views
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', views.cp_index, name='cp_index'),
    path('orders', views.cp_orders, name='cp_orders'),
    path('update_status', views.update_status, name='update_status'),
    path('add_network', views.cp_add_network, name='cp_add_network'),
    path('networks', views.cp_networks, name='cp_networks'),
    path('get_networks', views.Cp_get_networks.as_view()),
    path('get_network/<int:pk>', views.Cp_get_network.as_view()),
    path('networks/update/', views.cp_networks_update, name='cp_networks_update'),
    path('del_service/<service_id>', views.cp_del_service, name='cp_del_service'),
    path('add_service/<network_id>', views.cp_add_service, name='cp_add_service'),
    path('service/<service_id>', views.cp_service, name='cp_service'),
    path('add_tarif/<service_id>', views.cp_add_tarif, name='cp_add_tarif'),
    path('login', views.cp_login, name='cp_login'),
    path('restore', views.cp_restore, name='cp_restore'),

   


]