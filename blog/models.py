from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

CustomUser = get_user_model()


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250,
                             verbose_name='Заголовок поста')
    author = models.ForeignKey(CustomUser,
                               verbose_name='Автор',
                               related_name='posts',
                               on_delete=models.CASCADE)
    body = models.TextField(verbose_name='Текст поста')
    created = models.DateTimeField(verbose_name='Дата создания',
                                   auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата последнего обновления',
                                   auto_now=True)
    published = models.DateTimeField(verbose_name='Дата публикации',
                                     default=timezone.now)
    status = models.CharField(verbose_name='Статус статьи',
                              max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    slug = models.SlugField(max_length=250,
                            verbose_name='slug',
                            unique_for_date='published')

    class Meta:
        ordering = ('-published',)
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             verbose_name='Статья',
                             related_name='comments',
                             on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser,
                               verbose_name='Автор комментария',
                               related_name='comments',
                               on_delete=models.CASCADE)
    body = models.TextField(verbose_name='Текст комментария')
    created = models.DateTimeField(verbose_name='Дата создания',
                                   auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата последнего обновления',
                                   auto_now=True)
    active = models.BooleanField(default=True,
                                 verbose_name='Комментарий активен')

    class Meta:
        ordering = ('created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.body[:40]
