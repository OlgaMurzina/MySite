from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.conf import settings
from .forms import EmailPostForm, CommentForm
from django.views.decorators.http import require_POST
from taggit.models import Tag




def post_list(request, tag_slug=None):
    """
    Представление листа постов в блоге.
    Извлекаются все посты со статусом PUBLISHED, используя менеджер published из нашей модели.
    :param request: запрос с фронта для обработки
    :return: сгенерированная веб-страница с результатами обработки запроса
    """
    post_list = Post.published.all()
    # вставка возможности отображать посты, помеченные определенным тегом
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    # постраничная разбивка с 3 постами на страницу
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        # если page_number находится вне диапазона, то выдать последнюю страницу
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        # если page_number не целое число, то выдать первую страницу
        posts = paginator.page(1)
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts,
                   'tag': tag})

def post_detail(request, year, month, day, post):
    """
    Представление для отображения одиночного поста по его id.
    :param request: запрос с фронта для обработки
    :param id: id нужного поста
    :return: сгенерированная веб-страница с результатом - постом под id = присланному id
    """
    # функция сокращенного доступа для вызова метода get() в заданном модельном менеджере
    # и вызова исключения Http404 вместо исключения DoesNotExist, когда объект не найден
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # список активных комментариев к этому посту
    comments = post.comments.filter(active=True)
    # форма для комментирования пользователями
    form = CommentForm()
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form})

from .forms import EmailPostForm


def post_share(request, post_id):
    # извлечь пост по идентификатору id
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    # статус отправки письма по емейл
    sent = False
    if request.method == 'POST':
        # форма с данными была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # поля формы успешно прошли валидацию и переданы в виде словаря в cd
            cd = form.cleaned_data
            # отправить электронное письмо
            # получение абсолютного адреса поста
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            # формирование темы письма
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            # формирование сообщения
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s ({cd['email']}) comments: {cd['comments']}"
            # отправка письма
            send_mail(subject, message, settings.EMAIL_HOST_USER,
                      [cd['to']])
            # изменение статуса отправки
            sent = True
    else:
        # первый запрос на форму GET - идет пустая форма для сбора данных
        form = EmailPostForm()
    return render(request,
                  'blog/post/share.html',
                  {'post': post, 'form': form, 'sent': sent})


class PostListView(ListView):
    """
    Альтернативное представление списка постов
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    comment = None
    # Комментарий был отправлен
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Создать объект класса Comment, не сохраняя его в базе данных
        comment = form.save(commit=False)
        # Назначить пост комментарию
        comment.post = post
        # Сохранить комментарий в базе данных
        comment.save()
    return render(request, 'blog/post/comment.html',
                  {'post': post,
                   'form': form,
                   'comment': comment})