from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .import_products import import_products_from_yaml
from .models import Order, Product
from .serializers import (
    OrderItemSerializer,
    OrderSerializer,
    ProductSerializer,
    UserRegistrationSerializer,
)


class ProductListView(generics.ListAPIView):
    """Список всех товаров с фильтрацией и поиском"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["category", "product_infos__shop"]
    search_fields = ["name", "description"]


class ProductDetailView(generics.RetrieveAPIView):
    """Детальная информация о товаре"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class UserRegistrationView(generics.CreateAPIView):
    """Регистрация нового пользователя"""

    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": {
                    "email": user.email,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )


class OrderListView(generics.ListCreateAPIView):
    """Список заказов пользователя и создание нового заказа"""

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, state="basket")


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Детали заказа"""

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class AddToCartView(generics.CreateAPIView):
    """Добавление товара в корзину"""

    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        order, created = Order.objects.get_or_create(
            user=self.request.user, state="basket"
        )
        serializer.save(order=order)


class ImportProductsView(generics.CreateAPIView):
    """Импорт товаров из YAML-файла"""

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        shop_name = request.data.get("shop_name")

        if not file or not shop_name:
            return Response(
                {"error": "Необходимо указать file и shop_name"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        file_path = f"/tmp/{file.name}"
        with open(file_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        try:
            import_products_from_yaml(file_path, shop_name)
            return Response(
                {
                    "status": "OK",
                    "message": f"Товары импортированы в магазин {shop_name}",
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
