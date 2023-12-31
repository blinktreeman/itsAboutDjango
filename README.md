# Совсем небольшой Django-blog

## Создан проект, настроен репозиторий

```shell
Windows PowerShell
(C) Корпорация Майкрософт (Microsoft Corporation). Все права защищены.

Установите последнюю версию PowerShell для новых функций и улучшения! https://aka.ms/PSWindows

(venv) PS C:\Users\eugen\PycharmProjects\itsAboutDjango> git remote add origin git@github.com:blinktreeman/itsAboutDjango.git
(venv) PS C:\Users\eugen\PycharmProjects\itsAboutDjango> git push -u origin master
Enumerating objects: 9, done.
Counting objects: 100% (9/9), done.
Delta compression using up to 12 threads
Compressing objects: 100% (8/8), done.
Writing objects: 100% (9/9), 2.74 KiB | 2.74 MiB/s, done.
Total 9 (delta 1), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (1/1), done.
To github.com:blinktreeman/itsAboutDjango.git
 * [new branch]      master -> master
branch 'master' set up to track 'origin/master'.
(venv) PS C:\Users\eugen\PycharmProjects\itsAboutDjango> git checkout -b dev-iad
Switched to a new branch 'dev-iad'
(venv) PS C:\Users\eugen\PycharmProjects\itsAboutDjango>
```
## Отделение конфигурации от кода
[Store config in the environment](https://12factor.net/config)

Установим python-dotenv
[https://pypi.org/project/python-dotenv/](https://pypi.org/project/python-dotenv/)
```shell
(venv) PS C:\Users\eugen\PycharmProjects\itsAboutDjango> pip install python-dotenv
Collecting python-dotenv
  Downloading python_dotenv-1.0.0-py3-none-any.whl (19 kB)
Installing collected packages: python-dotenv
Successfully installed python-dotenv-1.0.0
```
Добавим файл .env для хранения настроек среды  
В файле settings.py добавим:
```python
from dotenv import dotenv_values

# take environment variables from .env
# https://pypi.org/project/python-dotenv/#getting-started
ENV_PATH = Path('.') / '.env'
CONFIG_VALUES = dotenv_values(ENV_PATH)
```

# Создание суперпользователя, административный сайт
[Introducing the Django Admin](https://docs.djangoproject.com/en/4.1/intro/tutorial02/#introducing-the-django-admin)  
```shell
(venv) PS C:\Users\eugen\PycharmProjects\itsAboutDjango> python manage.py makemigrations 
No changes detected
(venv) PS C:\Users\eugen\PycharmProjects\itsAboutDjango> python manage.py migrate       
Operations to perform:
  Apply all migrations: auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0001_initial... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
(venv) PS C:\Users\eugen\PycharmProjects\itsAboutDjango> python manage.py createsuperuser
Username (leave blank to use 'eugen'): 
Email address: blinktreeman@gmail.com
Password:
Password (again):
Superuser created successfully.
(venv) PS C:\Users\eugen\PycharmProjects\itsAboutDjango> 
```
# Добавляем приложение "Блог"
```shell
(venv) PS C:\Users\eugen\PycharmProjects\itsAboutDjango> python manage.py startapp blog
(venv) PS C:\Users\eugen\PycharmProjects\itsAboutDjango> 
```
Добавим в apps.py удобное имя для приложения
```python
verbose_name = 'Блог'
```
blog/apps.py:
```python
from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    verbose_name = 'Блог'
```
И добавим приложение в файл конфигурации указав ссылку на 
класс конфигурацию нашего приложения  
[https://docs.djangoproject.com/en/4.1/ref/applications/#configuring-applications](https://docs.djangoproject.com/en/4.1/ref/applications/#configuring-applications)  
settings.py:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # blog application
    'blog.apps.BlogConfig',
]
```
## Приложение accounts

Прежде чем перейти к созданию моделей приложения blog определимся каким образом 
приложение будет работать с пользователями. Здесь вариант, который рекомендует к использованию документация Django, 
использование пользовательской модели

[Using a custom user model when starting a project](https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project)

> If you’re starting a new project, it’s highly recommended to set up a 
> custom user model, even if the default User model is sufficient for you.

> Если вы начинаете новый проект, настоятельно рекомендуется настроить 
пользовательскую модель, даже если стандартная модель User вас полностью 
устраивает.  

И здесь также возможны несколько вариантов действия - использование классов 
AbstractUser либо AbstractBaseUser (работа с AbstractBaseUser влечет сильно много 
лишних действий, воспользуемся AbstractUser)

### AbstractUser

Если заглянем в модуль django.contrib.auth.models:
```python
class User(AbstractUser):
    """
    Users within the Django authentication system are represented by this
    model.

    Username and password are required. Other fields are optional.
    """

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
```
Можем видеть, что класс User наследуется от AbstractUser. Это позволит нам 
при создании пользовательской модели наследованной от AbstractUser использовать 
те же поля и методы если бы мы пользовались напрямую моделью User.  
Однако в дальнейшем, если возникнет необходимость, мы сможем расширить свою 
пользовательскую модель.

Для начала документация рекомендует задать пользовательскую модель в виде:
```python
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
```
Также необходимо переопределить пользовательскую модель по умолчанию, 
указав значение для параметра AUTH_USER_MODEL в settings.py:
```python
AUTH_USER_MODEL = 'accounts.User'
```
## Создаем приложение accounts
```shell
(venv) PS C:\Users\eugen\PycharmProjects\itsAboutDjango> python manage.py startapp accounts
(venv) PS C:\Users\eugen\PycharmProjects\itsAboutDjango> 
```
в settings.py:
```python
# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # blog application
    'blog.apps.BlogConfig',
    # accounts application
    'accounts.apps.AccountsConfig',
]
```
Задаем пользовательскую модель
```python
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass
```
В settings.py переопределяем модель по умолчанию:
```python
AUTH_USER_MODEL = 'accounts.User'
```
Регистрируем модель пользователя в админке Django. В accounts/admin.py:
```python
from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
```
## Модели приложения blog
В файле моделей blog/models.py

```python
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
```

Также создадим менеджер моделей blog/managers.py:
```python
from django.db import models


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self)\
            .get_queryset()\
            .filter(status='published')
```

И добавим его к модели blog/models.py:
```python
from .managers import PublishedManager
...

# Default manager
objects = models.Manager()
# Published posts manager
published_posts = PublishedManager()
```

## Create _base.html and home.html
```shell
(venv) PS C:\Users\eugen\PycharmProjects\itsAboutDjango> cd .\blog\
(venv) PS C:\Users\eugen\PycharmProjects\itsAboutDjango\blog> mkdir templates
(venv) PS C:\Users\eugen\PycharmProjects\itsAboutDjango\blog> cd .\templates\
(venv) PS C:\Users\eugen\PycharmProjects\itsAboutDjango\blog\templates>
(venv) PS C:\Users\eugen\PycharmProjects\itsAboutDjango\blog\templates> notepad _base.html
(venv) PS C:\Users\eugen\PycharmProjects\itsAboutDjango\blog\templates> notepad home.html
```
Добавляем маршруты к блогу - itsAboutDjango/urls.py:
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')), # <- add
]
```
Для blog/views.py:
```python
from django.shortcuts import render, get_object_or_404

from .models import Post


# https://docs.djangoproject.com/en/4.2/intro/tutorial03/#a-shortcut-render
def post_list(request):
    posts = Post.published_posts.all()
    return render(request,
                  'home.html',
                  {'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             published__year=year,
                             published__month=month,
                             published__day=day)
    comments = post.comments.filter(active=True)
    return render(request,
                  'detail.html',
                  {'post': post,
                   'comments': comments})
```
Для blog/urls.py:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    # post views
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail'),
]
```

Также страница поста с комментариями blog/templates/detail.html:
```html
{% extends "_base.html" %}
{% block title %}{{ post.title }}{% endblock %}
{% load static %}
{% load markdown_extras %}

{% block content %}
<div class="container">
    <div class="blog-post">
        <h2 class="blog-post-title mb-1"> {{ post.title }} </h2>
        <p class="blog-post-meta">Published {{ post.published }} by {{ post.author }}</p>
        {{ post.body| markdown | safe }}
    </div>
</div>
<div class="container pb-5">
    <div class="blog-comments">
        <div class="row">
            <div class="col">
                {% with comments.count as total_comments %}
                <h2>
                    {{ total_comments }} comment{{ total_comments|pluralize }}
                </h2>
                {% endwith %}
            </div>
        </div>

        {% for comment in comments %}
        <div class="blog-comment-header bg-secondary bg-gradient text-white rounded mt-3">
            <div class="row">
                <div class="col">
                    <div class="vstack">
                        <div class="hstack gap-3">
                            <div class="text-white"> {{ comment.author }} </div>
                        </div>
                        <div class="blog-comment-meta text-white-50"> Comment {{ comment.created }} </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="blog-comment-body mt-3">
            {{ comment.body|linebreaks }}
        </div>
        {% empty %}
        <p>There are no comments yet.</p>
        {% endfor %}
    </div>
</div>

{% endblock %}
```
