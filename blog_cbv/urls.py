"""
URL configuration for blog_cbv project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings  # тут будет и весь blog_cbv.settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from apps.blog.feeds import LatestPostFeed

handler403 = 'apps.blog.views.tr_handler403'  # Для страницы ошибки 403
handler404 = 'apps.blog.views.tr_handler404'  # Для страницы ошибки 404
handler500 = 'apps.blog.views.tr_handler500'  # Для страницы ошибки 500

urlpatterns = [
    path("admin/", admin.site.urls),
    path('feeds/latest/', LatestPostFeed(), name='latest_post_feed'),  # RSS лента
    path('', include('apps.blog.urls')),
    path('', include('apps.accounts.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

# Для работы media в режиме DEBUG = True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # для Django Debug Toolbar
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
