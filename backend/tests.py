from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Category, Product, Shop, ProductInfo

User = get_user_model()


class UserRegistrationTest(TestCase):
    """Тесты регистрации пользователя"""

    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        """Тест успешной регистрации"""
        url = reverse('register')
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'test123',
            'first_name': 'Тест',
            'last_name': 'Пользователь'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().email, 'test@example.com')


class ProductAPITest(TestCase):
    """Тесты API товаров"""

    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='Смартфоны')
        self.product = Product.objects.create(
            name='iPhone 15',
            category=self.category,
            price=75000.00,
            quantity=10
        )

    def test_product_list(self):
        """Тест получения списка товаров"""
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'iPhone 15')

    def test_product_detail(self):
        """Тест получения деталей товара"""
        url = reverse('product-detail', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'iPhone 15')