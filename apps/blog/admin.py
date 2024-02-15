from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin  # улучшить визуальный вид раздела категорий в админ панели
# from mptt.admin import DraggableMPTTAdmin
from .models import Post, Category

# admin.site.register(Post)
"""
Параметр prepopulated_fields позволяет с помощью встроенного JS 
обрабатывать заголовок в реальном времени, 
конвертирует в т.ч. и кириллицу. 
"""


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Админ-панель модели записей
    """
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'status']

@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    """
    Админ-панель модели категорий
    """
    prepopulated_fields = {'slug': ('title',)}
