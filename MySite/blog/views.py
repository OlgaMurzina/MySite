from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):
    """
    Представление листа постов в блоге.
    Извлекаются все посты со статусом PUBLISHED, используя менеджер published из нашей модели.
    :param request: запрос с фронта для обработки
    :return: сгенерированная веб-страница с результатами обработки запроса
    """
    posts = Post.published.all()
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})


def post_detail(request, id):
    """
    Представление для отображения одиночного поста по его id.
    :param request: запрос с фронта для обработки
    :param id: id нужного поста
    :return: сгенерированная веб-страница с результатом - постом под id = присланному id
    """
    # функция сокращенного доступа для вызова метода get() в заданном модельном менеджере
    # и вызова исключения Http404 вместо исключения DoesNotExist, когда объект не найден
    post = get_object_or_404(Post,
                             id=id, status=Post.Status.PUBLISHED)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})
