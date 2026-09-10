from django.contrib.auth.models import AbstractUser
from django.db import models


STATE_CHOICES = (
    ('basket', 'Корзина'),
    ('new', 'Новый'),
    ('confirmed', 'Подтверждён'),
    ('assembled', 'Собран'),
    ('sent', 'Отправлен'),
    ('delivered', 'Доставлен'),
    ('canceled', 'Отменён'),
)


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'backend_user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Shop(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    url = models.URLField(verbose_name='Ссылка', null=True, blank=True)
    state = models.BooleanField(verbose_name='Статус получения заказов', default=True)

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class ProductInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_infos', verbose_name='Товар')
    external_id = models.CharField(max_length=100, verbose_name='Внешний ID')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='product_infos', verbose_name='Магазин')

    class Meta:
        verbose_name = 'Информация о товаре'
        verbose_name_plural = 'Информация о товарах'

    def __str__(self):
        return f"{self.product.name} - {self.shop.name}"


class Parameter(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название характеристики')

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'
        ordering = ('name',)

    def __str__(self):
        return self.name


class ProductParameter(models.Model):
    product_info = models.ForeignKey(
        ProductInfo,
        on_delete=models.CASCADE,
        related_name='product_parameters',
        verbose_name='Информация о товаре'
    )
    parameter = models.ForeignKey(
        Parameter,
        on_delete=models.CASCADE,
        related_name='product_parameters',
        verbose_name='Характеристика'
    )
    value = models.CharField(max_length=100, verbose_name='Значение')

    class Meta:
        verbose_name = 'Параметр товара'
        verbose_name_plural = 'Параметры товаров'
        constraints = [
            models.UniqueConstraint(fields=['product_info', 'parameter'], name='unique_product_parameter')
        ]

    def __str__(self):
        return f"{self.product_info.name} - {self.parameter.name}: {self.value}"


class Contact(models.Model):
        user = models.ForeignKey(
            User,
            on_delete=models.CASCADE,
            related_name='contacts',
            verbose_name='Пользователь'
        )
        city = models.CharField(max_length=50, verbose_name='Город')
        street = models.CharField(max_length=100, verbose_name='Улица')
        house = models.CharField(max_length=15, verbose_name='Дом', blank=True)
        structure = models.CharField(max_length=15, verbose_name='Корпус', blank=True)
        building = models.CharField(max_length=15, verbose_name='Строение', blank=True)
        apartment = models.CharField(max_length=15, verbose_name='Квартира', blank=True)
        phone = models.CharField(max_length=20, verbose_name='Телефон')

        class Meta:
            verbose_name = 'Контакт'
            verbose_name_plural = 'Контакты'

        def __str__(self):
            return f'{self.city}, {self.street} {self.house}'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='Пользователь')
    dt = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='basket', verbose_name='Статус')
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Контакт')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-dt',)

    def __str__(self):
        return f'Заказ #{self.id} от {self.dt.strftime("%d.%m.%Y %H:%M")}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE, related_name='order_items', verbose_name='Товар')
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'
        constraints = [
            models.UniqueConstraint(fields=['order', 'product_info'], name='unique_order_item')
        ]

    def __str__(self):
        return f'{self.product_info.product.name} x {self.quantity}'

