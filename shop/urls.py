from django.urls import path
from shop import views

urlpatterns = [
    path('', views.shop, name="shop"),
    path('<str:category>/', views.shop, name='shop_category'),
    path('product-details/<int:id>/', views.productDetails, name="productDetails"),
]