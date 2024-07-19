from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    """
    Собственный менеджер - конкретно-прикладной менеджер для обслуживания QuerySet только по полю published
    """

    def get_queryset(self):
        return super().get_queryset() \
            .filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    """
    Модель Post для хранения постов блога в базе данных
    """

    class Status(models.TextChoices):
        """
        Определим поле статуса, которое позволит управлять статусом постов блога.
        В постах будут использоваться статусы Draft(Черновик) и Published(Опубликован).
        """
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    # поле заголовка поста
    title = models.CharField(max_length=250)
    # поле для формирования красивых и дружественных для поисковой оптимизации URL-адресов постов блога
    slug = models.SlugField(max_length=250, unique=True)
    # поле автора - связано с моделью данных User - связь один ко многим
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    # поле для хранения тела поста
    body = models.TextField()
    # поле дата публикации
    publish = models.DateTimeField(default=timezone.now)
    # поле дата создания
    created = models.DateTimeField(auto_now_add=True)
    # поле дата изменения
    updated = models.DateTimeField(auto_now=True)
    # поле статуса поста
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    '''
    Если в своей модели вы объявляете какие-либо менеджеры, но также хотите сохранить менеджер 
    objects, то вы должны добавить его в свою модель явным образом!
    '''
    # менеджер, применяемый по умолчанию
    objects = models.Manager()
    # конкретно-прикладной менеджер - собственный менеджер
    published = PublishedManager()

    class Meta:
        """
        Сортировка: посты блога отображаются на странице в обратном хронологическом порядке
        (от самых новых к самым старым) - сортировка идет по полю publish.
        Индексация: добавим индексацию для ускорения поиска по полю publish.
        """
        ordering = ['-publish']
        #
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title
