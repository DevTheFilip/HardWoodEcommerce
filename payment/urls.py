from django.urls import path

from . import views

urlpatterns = [


    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.payment_success, name='payment-success'),
    path('complete-order/', views.complete_order, name='complete-order'),
    path('failed/', views.payment_failed, name='payment-failed'),

]