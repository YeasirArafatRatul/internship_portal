
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from jobsapp.decorators import user_is_employer
from jobsapp.forms import CreateJobForm, JobUpdateForm
from jobsapp.models import Job, Applicant, JobCategory
from SiteSettings.models import Setting

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from jobsapp.decorators import user_is_employer
from jobsapp.tasks import time_to_live


class DashboardView(ListView):
    model = Job
    template_name = 'jobs/employer/dashboard.html'
    context_object_name = 'jobs'
    paginate_by = 3

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all().order_by('-id')[:8]
        context['settings'] = Setting.objects.filter(status=True).first()
        return context


class JobCreateView(LoginRequiredMixin, CreateView):
    template_name = 'jobs/jobcreate.html'
    form_class = CreateJobForm
    success_url = reverse_lazy('jobs:employer-dashboard')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('accounts:login')
        if self.request.user.is_authenticated and self.request.user.role != 'employer':
            return reverse_lazy('accounts:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        request = self.request
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all().order_by('-id')[:8]
        context['settings'] = Setting.objects.filter(status=True).first()
        return context


class JobUpdateView(LoginRequiredMixin, UpdateView):
    model = Job
    form_class = JobUpdateForm
    template_name = 'jobs/job_edit.html'
    pk_url_kwarg = 'job_id'

    def form_valid(self, form):
        request = self.request
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def test_func(self):
        job = self.get_object()
        if self.request.user == job.user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all().order_by('-id')[:8]
        context['settings'] = Setting.objects.filter(status=True).first()
        return context


@login_required(login_url='/login')
def job_update(request, job_id):
    if request.method == "POST":
        job_form = JobUpdateForm(
            request.POST, instance=request.user, id=job_id)
        if job_form.is_valid():
            job_form.save()

            messages.success(
                request, "Your Job is updated successfully")
            return redirect('jobs:employer-dashboard')
    else:
        category = JobCategory.objects.all().order_by('-id')[:8]
        job_form = CreateJobForm(instance=request.user)
        setting = Setting.objects.filter(status=True).first()
    context = {
        'categories': category,
        'job_form': job_form,

        'settings': setting,

    }

    return render(request, 'jobs/job_edit.html', context)


@login_required(login_url=reverse_lazy('accounts:login'))
def delete(request, job_id=None):
    try:
        job = Job.objects.get(user_id=request.user.id, id=job_id)
        job.delete()
    except IntegrityError as e:
        print(e.message)
        return HttpResponseRedirect(reverse_lazy('jobs:employer-dashboard'))
    return HttpResponseRedirect(reverse_lazy('jobs:employer-dashboard'))


class ApplicantPerJobView(ListView):
    model = Applicant
    template_name = 'jobs/employer/applicants.html'
    context_object_name = 'applicants'
    paginate_by = 1

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return Applicant.objects.filter(job_id=self.kwargs['job_id']).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = Job.objects.get(id=self.kwargs['job_id'])
        context['categories'] = JobCategory.objects.all().order_by('-id')[:8]
        context['settings'] = Setting.objects.filter(status=True).first()
        return context


class ApplicantsListView(ListView):
    model = Applicant
    template_name = 'jobs/employer/all-applicants.html'
    context_object_name = 'applicants'
    paginate_by = 8

    def get_queryset(self):
        # jobs = Job.objects.filter(user_id=self.request.user.id)
        return self.model.objects.filter(job__user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all().order_by('-id')[:8]
        context['settings'] = Setting.objects.filter(status=True).first()
        return context


@login_required(login_url=reverse_lazy('accounts:login'))
def filled(request, job_id=None):
    try:
        job = Job.objects.get(user_id=request.user.id, id=job_id)
        job.filled = True
        job.save()
    except IntegrityError as e:
        print(e.message)
        return HttpResponseRedirect(reverse_lazy('jobs:employer-dashboard'))
    return HttpResponseRedirect(reverse_lazy('jobs:employer-dashboard'))


@login_required(login_url=reverse_lazy('accounts:login'))
def select(request, applicant_id=None):
    url = request.META.get("HTTP_REFERER")  # get last url
    try:
        applicant = Applicant.objects.get(id=applicant_id)
        applicant.status = 1
        applicant.save()
    except IntegrityError as e:
        print(e.message)
        return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)


@login_required(login_url=reverse_lazy('accounts:login'))
def reject(request, applicant_id=None):
    url = request.META.get("HTTP_REFERER")  # get last url
    try:
        applicant = Applicant.objects.get(id=applicant_id)
        applicant.status = 2
        applicant.save()
        time_to_live(applicant_id)
        print(
            '****************************background-schedule created for id:', applicant_id)
    except IntegrityError as e:
        print(e.message)
        return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)


def create_job(request):
    if request.method == 'POST':
        form = CreateJobForm(request.POST)

        if form.is_valid():
            form.instance.user = request.user
