from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_list(request):
    """
    Представление листа постов в блоге.
    Извлекаются все посты со статусом PUBLISHED, используя менеджер published из нашей модели.
    :param request: запрос с фронта для обработки
    :return: сгенерированная веб-страница с результатами обработки запроса
    """
    post_list = Post.published.all()
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
                  {'posts': posts})

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
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})