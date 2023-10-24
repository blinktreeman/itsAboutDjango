from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    # post views
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail'),
]
