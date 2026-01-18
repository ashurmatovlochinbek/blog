from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags


# Create your models here.

class Author(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='author')
    bio = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('blogger-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['user__username']


class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.JSONField(default=dict, blank=True)
    author = models.ForeignKey(Author, on_delete=models.RESTRICT, null=True, related_name='blogs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.id)])

    def get_preview_text(self, max_words=30):
        """Extract plain text from Editor.js blocks for previews"""
        text_parts = []
        if 'blocks' in self.content:
            for block in self.content['blocks']:
                if block['type'] == 'paragraph' and 'text' in block.get('data', {}):
                    # Remove HTML tags if any
                    clean_text = strip_tags(block['data']['text'])
                    text_parts.append(clean_text)
                elif block['type'] == 'header' and 'text' in block.get('data', {}):
                    text_parts.append(strip_tags(block['data']['text']))
                elif block['type'] == 'list' and 'items' in block.get('data', {}):
                    for item in block['data']['items']:
                        text_parts.append(strip_tags(item))
        full_text = ' '.join(text_parts)
        words = full_text.split()
        return ' '.join(words[:max_words]) + ('...' if len(words) > max_words else '')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class BlogImage(models.Model):
    """
    NEW MODEL: Store uploaded images for blog posts
    Images are uploaded here and their URLs are stored in the JSON content
    """
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    image = models.ImageField(upload_to='blog_images/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image uploaded at {self.uploaded_at}"


User = get_user_model()

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.blog.title}'

    class Meta:
        ordering = ['-created_at']