from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    # частота изменения страниц постов
    changefreq = 'weekly'
    # релевантность (макс = 1)
    priority = 0.9

    def items(self):
        # возвращает набор запросов QuerySet объектов,
        # подлежащих включению в эту карту сайта
        return Post.published.all()

    def lastmod(self, obj):
        # получает каждый возвращаемый методом items() объект и
        # возвращает время последнего изменения объекта
        return obj.updated