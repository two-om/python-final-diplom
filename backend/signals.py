from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """Отправка приветственного письма при регистрации"""
    if created:
        subject = 'Добро пожаловать в наш магазин!'
        message = f'''
        Здравствуйте, {instance.first_name or instance.username}!

        Благодарим за регистрацию в нашем сервисе закупок.
        Теперь вы можете просматривать товары и оформлять заказы.

        С уважением,
        Команда сервиса закупок
        '''
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL or 'noreply@example.com',
            [instance.email],
            fail_silently=True,
            )