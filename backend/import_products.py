import yaml
from django.db import transaction
from .models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter


def import_products_from_yaml(file_path, shop_name):
    """
    Импорт товаров из YAML-файла.

    Args:
        file_path: путь к YAML-файлу
        shop_name: название магазина (поставщика)
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)

    shop, created = Shop.objects.get_or_create(
        name=shop_name,
        defaults={'state': True}
    )

    if created:
        print(f'Создан магазин: {shop_name}')
    else:
        print(f'Используем существующий магазин: {shop_name}')

    for item in data.get('goods', []):
        category_name = item.get('category')
        if category_name:
            category, _ = Category.objects.get_or_create(name=category_name)
        else:
            category = None

        product_name = item.get('name')
        if product_name:
            product, _ = Product.objects.get_or_create(
                name=product_name,
                defaults={
                    'category': category,
                    'description': item.get('description', ''),
                    'price': 0,
                    'quantity': 0
                }
            )
        else:
            continue

        external_id = item.get('id')
        price = item.get('price')
        quantity = item.get('quantity', 0)

        if external_id and price:
            product_info, created = ProductInfo.objects.get_or_create(
                product=product,
                shop=shop,
                external_id=external_id,
                defaults={
                    'price': price,
                    'quantity': quantity
                }
            )

            if not created:
                product_info.price = price
                product_info.quantity = quantity
                product_info.save()

            parameters = item.get('parameters', {})
            for param_name, param_value in parameters.items():
                parameter, _ = Parameter.objects.get_or_create(name=param_name)

                ProductParameter.objects.update_or_create(
                    product_info=product_info,
                    parameter=parameter,
                    defaults={'value': str(param_value)}
                )

    print('Импорт завершён!')