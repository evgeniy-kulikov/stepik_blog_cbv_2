from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


"""
create_user_profile это функция приемника, 
которая запускается каждый раз при создании пользователя. 
Пользователь является отправителем, который несет ответственность за отправку уведомления.

post_save это сигнал, который отправляется в конце метода сохранения.

В общем, вышеприведенный код делает то, что после того, 
как метод модели пользователя save() завершил выполнение, 
он отправляет сигнал post_save в функцию-приемник create_user_profile, 
затем эта функция получит сигнал 
для создания и сохранения экземпляра профиля для этого пользователя.

Следующим шагом является подключение приемников методом ready() конфигурации приложения 
путем импорта модуля сигналов в модуль apps.py.
"""
