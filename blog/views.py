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
