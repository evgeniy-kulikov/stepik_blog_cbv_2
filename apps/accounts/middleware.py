from django.contrib.auth.models import User
from django.core.cache import cache
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


class ActiveUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and request.session.session_key:
            cache_key = f'last-seen-{request.user.id}'
            last_login = cache.get(cache_key)

            if not last_login:
                User.objects.filter(id=request.user.id).update(last_login=timezone.now())
                # Устанавливаем кэширование на 300 секунд с текущей датой по ключу last-seen-id-пользователя
                cache.set(cache_key, timezone.now(), 300)


"""
Этот код представляет собой Middlewareкласс ActiveUserMiddleware, 
который используется для обновления статуса "онлайн" пользователя в Django с помощью кэширования.  
Более подробнее о Middleware:  https://docs.djangoproject.com/en/4.2/topics/http/middleware/

Middlewareкласс ActiveUserMiddleware определяет метод process_request(), 
который вызывается для каждого входящего запроса. 
В этом методе проверяется, авторизован ли пользователь, и имеет ли его сессия уникальный идентификатор session_key.

Если пользователь авторизован и имеет уникальный session_key, 
то обновляется его статус "последний раз в сети" с помощью метода cache.set() 
и сохраняется в кэше на время 300 секунд (можем установить любое значение).

Если в кэше нет записи для пользователя, 
то его последнее время входа в систему обновляется на текущее время 
с помощью метода User.objects.filter().update(), и время записывается в кэш.
"""
