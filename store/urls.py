

from django.urls import path

from . import views
from .views import category

urlpatterns = [

    path('', views.home, name='home'),
    path('store/', views.store, name='store'),
    path('product/<slug:product_slug>/',views.product_info,name='product_info'),

    path('search/<slug:category_slug>/',views.list_category,name='list-category'),
    path("contact/", views.contact, name="contact"),



]














