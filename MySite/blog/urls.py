from django.urls import path
from . import views

# определяется именное пространство приложения
app_name = 'blog'
# необходимо вставить шаблоны URL-адресов приложения blog
# в главные шаблоны URL-адресов проекта (в urls.py проекта)

urlpatterns = [
    # представления поста

    # не принимает никаких аргументов и соотносится с представлением post_list
    path('', views.post_list, name='post_list'),
    # не принимает никаких аргументов и соотносится с представлением post_list,
    # выполненным в виде класса

    # path('',
    # views.PostListView.as_view(),
    # name = 'post_list'),

    # соотносится с представлением post_detail и принимает аргумент id,
    # который является целым числом, заданным конвертором путей int,
    # обслуживает отдельные посты
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail'),
    # соотносится с представлением post_share и принимает аргумент post_id,
    # который задается целым числом через ковертор путей int, обслуживает рекомендации
    path('<int:post_id>/share/',
         views.post_share,
         name='post_share'),
    # соотносится с представлением post_comment и принимает аргумент post_id,
    # который задается целым числом через ковертор путей int, обслуживает комментарии
    path('<int:post_id>/comment/',
         views.post_comment,
         name='post_comment'),
    # соотносится с представлением post_list и принимает аргумент tag_slug,
    # который задается slug-строкой, обслуживает посты, отфильтрованные по тегу
    path('tag/<slug:tag_slug>/',
         views.post_list, name='post_list_by_tag'),
    # соотносится с представлением поиска
    path('search/', views.post_search, name='post_search'),

]
