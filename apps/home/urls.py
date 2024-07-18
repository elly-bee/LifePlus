# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views as home_views

app_name = 'apps_home'
urlpatterns = [
    # The home page
    path('', home_views.index, name='index'),
    path('dashboard', home_views.dashboard, name='dashboard'), 
    path('test', home_views.test, name='test'), 
    path('Registration', home_views.create_user, name='Registration'), # Using the 'index' function from the 'home' views
    path ('products', home_views.ProductView.as_view(), name='products'),
    path('user_create_info/<int:pk>/', home_views.create_user_details, name='user_create_info'),
    path('user_detail', home_views.user_detail, name='user_detail'),
    path('product_detail/<int:pk>', home_views.ProductDetials.as_view(), name='product_detail'),
    path('client_product_detail/<int:pk>', home_views.ClientProductDetail.as_view(), name='client_ProDetail'),
    path('transactionDetail/<int:pk>/', home_views.TransactionDetail.as_view(), name='transactionDetail'),
    #path('dashboard', home_views.cases_all, name='dashboard'),
   
    #path('cases_all', home_views.cases_all, name='cases_all'),
    
]
