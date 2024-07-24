"""
URL configuration for MySite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap

# определен словарь sitemaps
sitemaps = {'posts': PostSitemap, }

urlpatterns = [
    path('admin/', admin.site.urls),
    # новый шаблон URL-адреса, определенный с помощью функции include,
    # ссылается на шаблоны URL-адресов, определенные в приложении blog,
    # что-бы они были включены в рамки пути blog/
    path('blog/', include('blog.urls', namespace='blog')),
    # определим шаблон URL-адреса, который совпадает с шаблоном sitemap.xml и
    # в котором используется встроенное в Django представление sitemap.
    # Словарь sitemaps передается в представление sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap')
]

# Указанные шаблоны вставляются в рамки именного пространства blog.
# Именные пространства должны быть уникальными для всего проекта.
# Позже можно будет легко ссылаться на URL-запросы блога, используя именное пространство,
# за которым следует двоеточие, и имя URL-запроса, например blog:post_list и blog:post_detail.
