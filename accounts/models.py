from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    pass


# ## Complete Flow Diagrams
#
# ### **Password Change Flow (For Logged-In Users):**
# ```
# User clicks "Change Password"
#     → /accounts/password_change/
#     → Enters old & new passwords
#     → /accounts/password_change/done/
#     → Success!
# ```
#
# ### **Password Reset Flow (For Users Who Forgot Password):**
# ```
# User clicks "Forgot Password"
#     → /accounts/password_reset/
#     → Enters email
#     → /accounts/password_reset/done/ ("Check your email")
#     → User checks email
#     → Clicks link in email
#     → /accounts/reset/<uidb64>/<token>/
#     → Enters new password
#     → /accounts/password_reset_complete/
#     → User can now login!