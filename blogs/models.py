from django.contrib.auth import get_user_model
from django.db import models



# Create your models here.

class Author(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='author')
    bio = models.TextField(blank=True)

    def get_absolute_url(self):
        pass

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['user__username']


class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.RESTRICT, null=True, related_name='blogs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        pass

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


User = get_user_model()

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.blog.title}'

    class Meta:
        ordering = ['created_at']