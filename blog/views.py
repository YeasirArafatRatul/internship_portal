from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView, DetailView
from SiteSettings.models import Setting
from jobsapp.models import JobCategory
from .models import Post
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
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


class BlogSearchView(ListView):
    model = Post
    template_name = 'blogs/blog-search.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        return self.model.objects.filter(Q(title__icontains=self.request.GET.get('blog'))).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all().order_by('-id')[:8]
        context['settings'] = Setting.objects.filter(status=True).first()
        context['featured'] = Post.objects.filter(
            featured=True).order_by('?')[:6]
        return context


def search(request):

    try:
        query = request.GET.get('blog')
        blogs = Post.objects.filter(Q(title__icontains=query))
        paginator = Paginator(blogs, 4)  # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(1)

        categories = JobCategory.objects.all().order_by('-id')[:8]
        settings = Setting.objects.filter(status=True).first()
        featured = Post.objects.filter(
            featured=True).order_by('?')[:6]
        context = {
            'blogs': posts,
            'categories': categories,
            'settings': settings,
            'featured': featured,
        }
        return render(request, 'blogs/blog-search.html', context)

    except Exception as e:
        print('error is ', e)
        return HttpResponse(str(e))
