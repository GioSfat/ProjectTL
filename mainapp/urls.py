from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('', include('django.contrib.auth.urls')),
    path('logout/', views.logout, name='logout'),
    path('bus_pg/', views.business_page, name='business_page'),
    path('change_info_cus/', views.change_info_cus, name='change_info_cus'),
    path('change_info_bus/', views.change_info_bus, name='change_info_bus'),
    path('customer/', views.customer, name='customer'),
    path('bus_sbm/', views.business_submit, name='business_submit'),

]
