

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blogs/', views.BlogListView.as_view(), name='blog-list'),
    path('<int:pk>/', views.BlogDetailView.as_view(), name='blog-detail'),
]
