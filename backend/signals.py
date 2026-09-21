from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created

User = get_user_model()


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """Отправка приветственного письма при регистрации"""
    if created:
        subject = "Добро пожаловать в наш магазин!"
        message = (
            f"Здравствуйте, {instance.first_name or instance.username}!\n\n"
            f"Благодарим за регистрацию в нашем сервисе закупок.\n"
            f"Теперь вы можете просматривать товары и оформлять заказы.\n\n"
            f"С уважением,\n"
            f"Команда сервиса закупок"
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL or "noreply@example.com",
            [instance.email],
            fail_silently=True,
        )


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, **kwargs):
    """Отправка письма со ссылкой для сброса пароля"""
    subject = "Сброс пароля"
    message = (
        f"Здравствуйте!\n\n"
        f"Вы запросили сброс пароля. Ваш токен:\n\n"
        f"{reset_password_token.key}\n\n"
        f"Если вы не запрашивали сброс пароля, проигнорируйте это письмо.\n\n"
        f"С уважением,\n"
        f"Команда сервиса закупок"
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL or "noreply@example.com",
        [reset_password_token.user.email],
        fail_silently=True,
    )
