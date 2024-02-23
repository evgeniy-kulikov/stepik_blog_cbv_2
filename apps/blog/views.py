from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View

from django.views.generic import ListView, DetailView, CreateView, UpdateView

from taggit.models import Tag

from .forms import PostCreateForm, PostUpdateForm, CommentCreateForm
from .models import Post, Category, Comment, Rating
from ..services.mixins import AuthorRequiredMixin


class PostByTagListView(ListView):
    """
    Фильтрация по тегу
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    tag = None

    def get_queryset(self):
        self.tag = Tag.objects.get(slug=self.kwargs['tag'])
        queryset = Post.objects.filter(tags__slug=self.tag.slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Статьи по тегу: {self.tag.name}'
        return context


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 3
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
        # page = context['page_obj']
        # context['paginator_range'] = page.paginator.get_elided_page_range(page.number, on_each_side=2, on_ends=2)

        return context


class PostDetailView(DetailView):
    model = Post
    # По умолчанию DetailView ищет шаблон с префиксом имени модели и суффиксом _detail.html
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'  # переопределим имя Queryset по умолчанию

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title  # Переопределяем get_context_data для добавления в него ключа 'title'
        context['form'] = CommentCreateForm  # вывод нашей формы в шаблон, используя переменную {{ form }}
        return context


class PostFromCategory(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    category = None
    paginate_by = 2
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


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Представление: создание материалов (статьи) на сайте
    """
    model = Post
    template_name = 'blog/post_create.html'
    form_class = PostCreateForm

    # Пока нет авторизации, будем перенаправлять пользователя на главную страницу сайта.
    # Работает LoginRequiredMixin
    login_url = 'home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # передаем заголовок для <title> нашего шаблона
        context['title'] = 'Добавление статьи на сайт'
        return context

    def form_valid(self, form):
        """
        Проверяем нашу форму, а также сохраняем автором текущего пользователя на странице
        """
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


# class PostUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
# Убрали LoginRequiredMixin, так как данная логика уже добавлена в кастомный миксин AuthorRequiredMixin
class PostUpdateView(AuthorRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление: обновления материала (статьи) на сайте
    """
    model = Post
    template_name = 'blog/post_update.html'
    context_object_name = 'post'
    form_class = PostUpdateForm
    login_url = 'home'
    success_message = 'Запись была успешно обновлена!'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Обновление статьи: {self.object.title}'
        return context

    def form_valid(self, form):
        # Временно разрешим всем редактировать свои и чужие статьи
        # form.instance.updater = self.request.user
        form.save()
        return super().form_valid(form)


class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для добавления комментария через JS
    """
    model = Comment
    form_class = CommentCreateForm

    def is_ajax(self):
        """
        Возвращает True, если запрос был сделан через AJAX
        """
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def form_invalid(self, form):
        """
        Метод вызывается, когда форма создания комментария не проходит валидацию
        """
        if self.is_ajax():
            return JsonResponse({'error': form.errors}, status=400)
        return super().form_invalid(form)

    def form_valid(self, form):
        """
        Метод вызывается, когда форма создания комментария прошла валидацию
        В нем сохраняется новый комментарий, и возвращается успешный ответ
        с атрибутами в виде json с помощью JsonResponse,
        в случае, если это был не AJAX запрос, то делаем редирект пользователя на статью.
        """
        comment = form.save(commit=False)
        comment.post_id = self.kwargs.get('pk')
        comment.author = self.request.user
        comment.parent_id = form.cleaned_data.get('parent')
        comment.save()

        if self.is_ajax():
            return JsonResponse({
                'is_child': comment.is_child_node(),
                'id': comment.id,
                'author': comment.author.username,
                'parent_id': comment.parent_id,
                'time_create': comment.time_create.strftime('%Y-%b-%d %H:%M:%S'),
                'avatar': comment.author.profile.avatar.url,
                'content': comment.content,
                'get_absolute_url': comment.author.profile.get_absolute_url()
            }, status=200)

        return redirect(comment.post.get_absolute_url())

    def handle_no_permission(self):
        return JsonResponse({'error': 'Необходимо авторизоваться для добавления комментариев'}, status=400)


class RatingCreateView(View):
    model = Rating

    def post(self, request, *args, **kwargs):
        post_id = request.POST.get('post_id')
        value = int(request.POST.get('value'))
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
        ip_address = ip
        user = request.user if request.user.is_authenticated else None

        rating, created = self.model.objects.get_or_create(
           post_id=post_id,
            ip_address=ip_address,
            defaults={'value': value, 'user': user},
        )

        if not created:
            if rating.value == value:
                rating.delete()
                return JsonResponse({'status': 'deleted', 'rating_sum': rating.post.get_sum_rating()})
            else:
                rating.value = value
                rating.user = user
                rating.save()
                return JsonResponse({'status': 'updated', 'rating_sum': rating.post.get_sum_rating()})
        return JsonResponse({'status': 'created', 'rating_sum': rating.post.get_sum_rating()})