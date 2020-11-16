from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView

from ..documents import JobDocument
from ..forms import ApplyJobForm
from ..models import Job, Applicant, JobCategory, User
from SiteSettings.models import Setting
from django.shortcuts import get_object_or_404


# class BaseView(CreateView):
#     model = Setting
#     template_name = 'base.html'
#     context_object_name = 'settings'

#     def get_queryset(self):
#         return self.model.objects.filter(status=True).first()


class HomeView(ListView):
    model = Job
    template_name = 'home.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return self.model.objects.filter(filled=False).order_by('-created_at')[:8]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employers'] = User.objects.filter(
            role='employer').order_by('?')[:8]
        context['trendings'] = self.model.objects.filter(filled=False,
                                                         created_at__month=timezone.now().month).order_by('-created_at')[:5]
        context['settings'] = Setting.objects.filter(status=True).first()
        context['categories'] = JobCategory.objects.all().order_by('-id')[:8]
        return context


class SearchView(ListView):
    model = Job
    template_name = 'jobs/search.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return self.model.objects.filter(location__contains=self.request.GET['location'],
                                         title__contains=self.request.GET['position'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all()

        context['settings'] = Setting.objects.filter(status=True).first()
        return context


class JobListView(ListView):
    model = Job
    template_name = 'jobs/jobs.html'
    context_object_name = 'jobs'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all()
        context['settings'] = Setting.objects.filter(status=True).first()
        return context


class IndividualCompanyJobListView(ListView):
    model = Job
    template_name = 'jobs/jobs.html'
    context_object_name = 'jobs'
    paginate_by = 8

    def get_queryset(self):
        # jobs = Job.objects.filter(user_id=self.request.user.id)
        self.id = get_object_or_404(User, id=self.kwargs['user_id'])
        return self.model.objects.filter(user=self.id, filled=False).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all()
        context['settings'] = Setting.objects.filter(status=True).first()
        return context


class CatJobListView(ListView):
    model = Job
    template_name = 'jobs/jobs.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        self.id = get_object_or_404(JobCategory, id=self.kwargs['cat_id'])
        return Job.objects.filter(category=self.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all()

        context['settings'] = Setting.objects.filter(status=True).first()
        return context


class Companies(ListView):
    model = User
    template_name = 'jobs/companies.html'
    context_object_name = 'companies'
    paginate_by = 16

    def get_queryset(self):
        return self.model.objects.filter(role='employer').order_by('?')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all()

        context['settings'] = Setting.objects.filter(status=True).first()
        return context


class JobDetailsView(DetailView):
    model = Job
    template_name = 'jobs/details.html'
    context_object_name = 'job'
    pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        obj = super(JobDetailsView, self).get_object(queryset=queryset)
        if obj is None:
            raise Http404("Job doesn't exists")
        return obj

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            # raise error
            raise Http404("Job doesn't exists")
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all()

        context['settings'] = Setting.objects.filter(status=True).first()
        return context


class ApplyJobView(CreateView):
    model = Applicant
    form_class = ApplyJobForm
    slug_field = 'job_id'
    slug_url_kwarg = 'job_id'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.info(self.request, 'Successfully applied for the job!')
            return self.form_valid(form)
        else:
            return HttpResponseRedirect(reverse_lazy('jobs:home'))

    def get_success_url(self):
        return reverse_lazy('jobs:jobs-detail', kwargs={'id': self.kwargs['job_id']})

    # def get_form_kwargs(self):
    #     kwargs = super(ApplyJobView, self).get_form_kwargs()
    #     print(kwargs)
    #     kwargs['job'] = 1
    #     return kwargs

    def form_valid(self, form):
        # check if user already applied
        applicant = Applicant.objects.filter(
            user_id=self.request.user.id, job_id=self.kwargs['job_id'])
        if applicant:
            messages.info(self.request, 'You already applied for this job')
            return HttpResponseRedirect(self.get_success_url())
        # save applicant
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all()

        context['settings'] = Setting.objects.filter(status=True).first()
        return context
