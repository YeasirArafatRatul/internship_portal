from django.shortcuts import render
from django.views.generic import ListView
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
        return Post.objects.filter().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all().order_by('-id')[:8]
        context['featured'] = Post.objects.filter(
            featured=True).order_by('-id')[:6]
        context['settings'] = Setting.objects.filter(status=True).first()
        return context
