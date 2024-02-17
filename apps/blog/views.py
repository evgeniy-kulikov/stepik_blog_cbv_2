
from django.shortcuts import render

from django.views.generic import ListView, DetailView
from .models import Post, Category


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 1
    queryset = Post.custom.all()  # Переопределение вызова модели

    # get_context_data - может использоваться для передачи содержимого или параметров вне модели в шаблон
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'

        # получить доступ к параметрам on_each_side,  on_ends
        # https://django.fun/docs/django/5.0/ref/paginator/#django.core.paginator.Paginator
        """
        Paginator.get_elided_page_range(number, *, on_each_side=3, on_ends=2)[исходный код]¶
        Возвращает основанный на 1 список номеров страниц, аналогичный Paginator.page_range, 
        но может добавлять многоточие с одной или обеих сторон текущего номера страницы, 
        если Paginator.num_pages имеет большой размер.

        Количество страниц, включаемых с каждой стороны от текущего номера страницы, 
        определяется аргументом on_each_side, который по умолчанию равен 3.

        Количество страниц, включаемых в начало и конец диапазона страниц, 
        определяется аргументом on_ends, который по умолчанию равен 2.

        Например, при значениях по умолчанию для on_each_side и on_ends, 
        если текущая страница - 10, а всего страниц 50, 
        диапазон страниц будет [1, 2, '…', 7, 8, 9, 10, 11, 12, 13, '…', 49, 50]. 
        Это приведет к появлению страниц 7, 8 и 9 слева и 11, 12 и 13 справа от текущей страницы, 
        а также страниц 1 и 2 в начале и 49 и 50 в конце.
        """
        page = context['page_obj']
        context['paginator_range'] = page.paginator.get_elided_page_range(page.number, on_each_side=2, on_ends=2)

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
    paginate_by = 1
    queryset = Post.custom.all()  # Переопределение вызова модели

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

