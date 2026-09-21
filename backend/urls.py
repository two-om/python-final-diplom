from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    AddToCartView,
    ImportProductsView,
    OrderDetailView,
    OrderListView,
    ProductDetailView,
    ProductListView,
    UserRegistrationView,
)

urlpatterns = [
    # Товары
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    # Регистрация и авторизация
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Заказы и корзина
    path("orders/", OrderListView.as_view(), name="order-list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("cart/", AddToCartView.as_view(), name="add-to-cart"),
    # Импорт товаров
    path("import/", ImportProductsView.as_view(), name="import-products"),
]
