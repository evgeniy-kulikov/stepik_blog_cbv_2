from uuid import uuid4
from pytils.translit import slugify

"""
pip install pytils
Pytils это инструменты для работы с русскими строками 
(транслитерация, числительные словами, русские даты и т.д.) 
"""
def unique_slugify(instance, slug):
    """
    Генератор уникальных SLUG для моделей, в случае существования такого SLUG.
    """
    model = instance.__class__
    unique_slug = slugify(slug)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{unique_slug}-{uuid4().hex[:8]}'
    return unique_slug
