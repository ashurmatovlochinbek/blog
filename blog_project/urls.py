"""
URL configuration for blog_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from blogs.views import RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', RegisterView.as_view(), name='register'),
    path('blog/', include('blogs.urls')),
    path('', RedirectView.as_view(pattern_name='index', permanent=True)),
]

# Default Authentication URLs
# Django's django.contrib.auth.urls provides these standard URL patterns:
# Login/Logout:
#
# /accounts/login/ - Login page
# /accounts/logout/ - Logout handler
#
# Password Change:
#
# /accounts/password_change/ - Form to change password (requires login)
# /accounts/password_change/done/ - Success page after password change
#
# Password Reset:
#
# /accounts/password_reset/ - Form to request password reset via email
# /accounts/password_reset/done/ - Confirmation that reset email was sent
# /accounts/reset/<uidb64>/<token>/ - Link from email to actually reset password
# /accounts/password_reset_complete/ - Success page after reset

# What You Need to Provide
# Django handles the logic, but you need to create templates. The default template names are:
#
# registration/login.html
# registration/logged_out.html
# registration/password_change_form.html
# registration/password_change_done.html
# registration/password_reset_form.html
# registration/password_reset_done.html
# registration/password_reset_confirm.html
# registration/password_reset_complete.html