from django.urls import path
from shop import views

urlpatterns = [
    path('', views.shop, name="shop"),
    path('product-details/<int:id>/', views.productDetails, name="productDetails"),
]