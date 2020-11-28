from django.shortcuts import render
from django.views.generic import ListView, DetailView
from SiteSettings.models import Setting
from jobsapp.models import JobCategory
from .models import Post
# Create your views here.


class PostListView(ListView):
    model = Post
    template_name = 'blogs/blog.html'
    context_object_name = 'blogs'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(featured=False).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all().order_by('-id')[:8]
        context['featured'] = Post.objects.filter(
            featured=True).order_by('-id')[:6]
        context['settings'] = Setting.objects.filter(status=True).first()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blogs/blog-details.html'
    context_object_name = 'blog'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all().order_by('-id')[:8]
        context['featured'] = Post.objects.filter(
            featured=True).order_by('?')[:6]
        context['settings'] = Setting.objects.filter(status=True).first()
        return context
