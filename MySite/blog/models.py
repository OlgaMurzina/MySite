from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


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
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
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
    # добавляем менеджер тегов
    tags = TaggableManager()

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

    def get_absolute_url(self):
        """
        Метод для формирования кананонического адреса динамически. Функция reverse()
        будет формировать URL-адрес динамически, применяя имя URL-адреса, определенное
        в шаблонах URL-адресов, и добавлять к нем все, что нам нужно для быстрого поиска
        :return:
        """
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

class Comment(models.Model):
    """
    Модель для хранения комментариев к постам
    """
    # поле связи многие к одному комментария и поста в блоге
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # поле управления публикацией комментариев
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'