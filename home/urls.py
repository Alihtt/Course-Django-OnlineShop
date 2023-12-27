from django.urls import path
from . import views

app_name='home'
urlpatterns = [
    path('',view=views.HomeView.as_view(),name='home'),
    path('<slug:slug>/',view=views.ProductDetailView.as_view(),name='product_detail')
]