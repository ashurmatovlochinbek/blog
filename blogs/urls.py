

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blogs/', views.BlogListView.as_view(), name='blog-list'),
    path('<int:pk>/', views.BlogDetailView.as_view(), name='blog-detail'),
    path('create/', views.BlogCreateView.as_view(), name='blog-create'),
    path('<int:blog_pk>/comment/', views.AddCommentView.as_view(), name='add-comment'),
]
