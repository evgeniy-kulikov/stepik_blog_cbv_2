
from django.shortcuts import render

from django.views.generic import ListView, DetailView
from .models import Post, Category


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 2


# get_context_data - может использоваться для передачи содержимого или параметров вне модели в шаблон
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context


class PostDetailView(DetailView):
    model = Post
    # По умолчанию DetailView ищет шаблон с префиксом имени модели и суффиксом _detail.html
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'  # переопределим имя Queryset по умолчанию

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title  # Переопределяем get_context_data для добавления в него ключа 'title'
        return context


class PostFromCategory(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    category = None

    def get_queryset(self):

        # Так тоже можно
        # self.category = Category.objects.get(slug=self.kwargs['slug'])
        # queryset = super().get_queryset().filter(status='published')
        # queryset = queryset.filter(category__slug=self.category.slug)

        self.category = Category.objects.get(slug=self.kwargs['slug'])
        queryset = Post.objects.filter(category__slug=self.category.slug)

        if not queryset:
            sub_cat = Category.objects.filter(parent=self.category)
            queryset = Post.objects.filter(category__in=sub_cat)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Записи из категории: {self.category.title}'
        return context

