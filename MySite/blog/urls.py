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
    # соотносится с представлением post_detail и принимает аргумент id,
    # который является целым числом, заданным конвертором путей int
    path('<int:id>/', views.post_detail, name='post_detail'),
]
