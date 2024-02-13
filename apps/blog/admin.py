from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Post, Category

admin.site.register(Post)

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    """
    Админ-панель модели категорий
    """
    prepopulated_fields = {'slug': ('title',)}
