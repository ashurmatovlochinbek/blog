from django.contrib.auth import login
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from blogs.forms import CustomUserCreationForm
from blogs.models import Blog


# Create your views here.

# @login_required
def index(request):
    return render(request, 'blogs/index.html')

class BlogListView(ListView):
    model = Blog
    context_object_name = 'blogs'
    paginate_by = 1
    template_name = 'blogs/blog_list.html'


    def get_queryset(self):
        return Blog.objects.all()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        return context

class BlogDetailView(DetailView):
    model = Blog
    context_object_name = 'blog'
    template_name = 'blogs/blog_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    # def get_object(self):
    #     # Use 'blog_id' from URL instead of default 'pk'
    #     return Blog.objects.get(id=self.kwargs['blog_id'])



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