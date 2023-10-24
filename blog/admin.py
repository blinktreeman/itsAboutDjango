from django.contrib import admin
from .models import Post, Comment


class CommentInLine(admin.StackedInline):
    model = Comment
    extra = 0


@admin.register(Post)
class ArticleAdmin(admin.ModelAdmin):
    model = Post

    list_display = (
        'title',
        'author',
        'body',
        'created',
        'updated',
        'published',
        'status',
        'slug',
    )
    list_filter = (
        'status',
    )
    search_fields = (
        'title',
        'author',
        'published',
    )
    prepopulated_fields = {
        'slug': (
            'title',
        )
    }
    inlines = [
        CommentInLine
    ]
    date_hierarchy = 'created'
    save_on_top = True


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = (
        'post',
        'author',
        'body',
        'created',
        'updated',
        'active',
    )
    search_fields = (
        'post',
        'author',
        'created',
    )
