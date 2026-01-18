from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, DetailView

from blogs.forms import CustomUserCreationForm, BlogForm
from blogs.models import Blog, Author, BlogImage
from blogs.forms import CommentForm
from blogs.models import Comment


# Create your views here.

# @login_required
def index(request):
    return render(request, 'blogs/index.html')


class BloggerListView(ListView):
    model = Author
    context_object_name = 'bloggers'
    paginate_by = 10
    template_name = 'blogs/blogger_list.html'

    def get_queryset(self):
        return Author.objects.all().order_by('user__username')


class BloggerDetailView(DetailView):
    model = Author
    context_object_name = 'blogger'
    template_name = 'blogs/blogger_detail.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all blogs by this author
        blogs = self.object.blogs.all().order_by('-created_at')

        # Paginate them
        paginator = Paginator(blogs, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['blogs'] = page_obj  # paginated blogs
        context['page_obj'] = page_obj  # for pagination template
        return context

class BlogListView(ListView):
    model = Blog
    context_object_name = 'blogs'
    paginate_by = 10
    template_name = 'blogs/blog_list.html'


    def get_queryset(self):
        queryset = Blog.objects.all()
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(author__user__username__icontains=search_query)
            )
        return queryset.order_by('-created_at')


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context

# class BlogListView(ListView):
#     model = Blog
#     context_object_name = 'blogs'
#     paginate_by = 10
#     template_name = 'blogs/blog_list.html'
#
#     def get_queryset(self):
#         queryset = Blog.objects.all()
#         search_query = self.request.GET.get('q', '')
#
#         if search_query:
#             queryset = queryset.filter(
#                 Q(title__icontains=search_query) |
#                 Q(author__user__username__icontains=search_query)
#             )
#
#         return queryset.order_by('-created_at')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['search_query'] = self.request.GET.get('q', '')
#         return context
#
#     def render_to_response(self, context, **response_kwargs):
#         if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
#             return render(
#                 self.request,
#                 "blogs/fragments/_blog_list_fragment.html",
#                 context
#             )
#         return super().render_to_response(context, **response_kwargs)


class BlogDetailView(DetailView):
    model = Blog
    context_object_name = 'blog'
    template_name = 'blogs/blog_detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

    # def get_object(self):
    #     # Use 'blog_id' from URL instead of default 'pk'
    #     return Blog.objects.get(id=self.kwargs['blog_id'])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.core.paginator import Paginator
        comments = self.object.comments.all().order_by('-created_at')
        paginator = Paginator(comments, 10)  # Show 5 comments per page
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        context['comments'] = page_obj
        context['page_obj'] = page_obj
        context['comment_form'] = CommentForm()

        # Check if it's an AJAX request for pagination
        context['is_ajax'] = self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        return context

    def render_to_response(self, context, **response_kwargs):
        # Check if it's an AJAX request for loading more comments
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Build HTML for all comments on this page
            comments_html = ''
            for comment in context['comments']:
                comments_html += render_to_string('blogs/fragments/comment_item.html', {
                    'comment': comment
                }, request=self.request)

            # Return JSON response
            return JsonResponse({
                'html': comments_html,
                'has_next': context['page_obj'].has_next(),
                'next_page': context['page_obj'].next_page_number() if context['page_obj'].has_next() else None
            })

        # Normal request - return HTML page
        return super().render_to_response(context, **response_kwargs)


class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def get_login_url(self):
        return f"{reverse('login')}?next={self.request.path}"

    def form_valid(self, form):
        blog = Blog.objects.get(pk=self.kwargs['blog_pk'])

        comment = form.save(commit=False)
        comment.blog = blog
        comment.user = self.request.user
        comment.save()

        # Check if it's an AJAX request
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render_to_string('blogs/fragments/comment_item.html', {
                'comment': comment,
                'user': self.request.user
            })

            return JsonResponse({
                'success': True,
                'html': html,
                'comment_count': blog.comments.count()
            })

        return redirect('blog-detail', pk=blog.pk)

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)

        return redirect('blog-detail', pk=self.kwargs['blog_pk'])


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blogs/blog_form.html'
    success_url = reverse_lazy('blog-list')

    def form_valid(self, form):
        # Get the Author profile of the logged-in user
        author = get_object_or_404(Author, user=self.request.user)

        blog = form.save(commit=False)
        blog.author = author  # ← Set author automatically

        blog.save()

        return super().form_valid(form)




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


class UploadImageView(LoginRequiredMixin, View):
    """
    Handle image uploads from Editor.js

    When user clicks "add image" in the editor:
    1. Editor.js sends image file to this view via AJAX
    2. This view saves the image
    3. Returns the image URL to Editor.js
    4. Editor.js inserts the URL into the content JSON
    """

    def post(self, request, *args, **kwargs):
        # Check if image file is in request
        if 'image' not in request.FILES:
            return JsonResponse({
                'success': 0,
                'error': 'No image provided'
            })

        image_file = request.FILES['image']

        # Create BlogImage instance (without blog reference for now)
        # The image URL will be stored in the blog's JSON content
        blog_image = BlogImage.objects.create(image=image_file)

        # Return success response in Editor.js format
        # Editor.js expects this exact JSON structure
        return JsonResponse({
            'success': 1,
            'file': {
                'url': blog_image.image.url,
            }
        })

