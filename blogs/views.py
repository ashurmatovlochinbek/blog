from django.contrib.auth import login
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from blogs.forms import CustomUserCreationForm


# Create your views here.

# @login_required
def index(request):
    return render(request, 'blogs/index.html')


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Additional logic can be added here if needed
        login(self.request, self.object)
        from .models import Author
        Author.objects.create(user=self.object)
        return response