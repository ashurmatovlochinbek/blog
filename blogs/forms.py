import json

import bleach
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Blog

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter blog title...'
            }),
            # Content will be populated by Editor.js via JavaScript
            'content': forms.HiddenInput(),
        }

    def clean_content(self):
        """
        Sanitize the Editor.js JSON content to prevent XSS attacks
        This runs when form is submitted
        """
        content = self.cleaned_data.get('content')

        # If content is empty, return empty dict
        if not content:
            return {}

        # If content is a string (from form), parse it as JSON
        if isinstance(content, str):
            try:
                content = json.loads(content)
            except json.JSONDecodeError:
                raise forms.ValidationError("Invalid content format")

        # Sanitize each block in the content
        if 'blocks' in content:
            for block in content['blocks']:

                # Sanitize paragraph text
                if block['type'] == 'paragraph' and 'text' in block.get('data', {}):
                    # Allow only safe HTML tags
                    allowed_tags = ['b', 'i', 'u', 'a', 'strong', 'em', 'code', 'mark']
                    allowed_attrs = {'a': ['href', 'title', 'target']}

                    block['data']['text'] = bleach.clean(
                        block['data']['text'],
                        tags=allowed_tags,
                        attributes=allowed_attrs,
                        strip=True
                    )

                # Sanitize header text (no HTML allowed)
                elif block['type'] == 'header' and 'text' in block.get('data', {}):
                    block['data']['text'] = bleach.clean(
                        block['data']['text'],
                        tags=[],  # No HTML tags allowed in headers
                        strip=True
                    )

                # Sanitize list items
                elif block['type'] == 'list' and 'items' in block.get('data', {}):
                    block['data']['items'] = [
                        bleach.clean(item, tags=['b', 'i', 'code'], strip=True)
                        for item in block['data']['items']
                    ]

                # Sanitize quote text
                elif block['type'] == 'quote':
                    if 'text' in block.get('data', {}):
                        block['data']['text'] = bleach.clean(
                            block['data']['text'],
                            tags=['b', 'i'],
                            strip=True
                        )
                    if 'caption' in block.get('data', {}):
                        block['data']['caption'] = bleach.clean(
                            block['data']['caption'],
                            tags=[],
                            strip=True
                        )

        return content


# blogs/forms.py
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'Write your comment here...',
            })
        }
        labels = {
            'content': 'Your Comment'
        }