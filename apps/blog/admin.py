from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin  # улучшить визуальный вид раздела категорий в админ панели
# from mptt.admin import DraggableMPTTAdmin
from .models import Post, Category

# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    """
    Админ-панель модели категорий
    """
    prepopulated_fields = {'slug': ('title',)}
