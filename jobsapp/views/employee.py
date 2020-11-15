from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from accounts.forms import EmployeeProfileUpdateForm
from accounts.models import User
from jobsapp.decorators import user_is_employee
from jobsapp.models import Job, JobCategory, Applicant
from SiteSettings.models import Setting
from django.views.generic import CreateView, FormView, RedirectView, TemplateView, DetailView, ListView


class AppliedJobsView(ListView):
    model = Applicant
    template_name = 'jobs/employee/applied-jobs.html'
    context_object_name = 'applied_jobs'
    paginate_by = 8

    def get_queryset(self):
        # jobs = Job.objects.filter(user_id=self.request.user.id)
        return self.model.objects.filter(user=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['applied_jobs'] = Applicant.objects.filter(user=self.user)
        context['categories'] = JobCategory.objects.all()
        context['settings'] = Setting.objects.filter(status=True).first()
        return context


class EditProfileView(UpdateView):
    model = User
    form_class = EmployeeProfileUpdateForm
    context_object_name = 'employee'
    template_name = 'jobs/employee/edit-profile.html'
    success_url = reverse_lazy('accounts:employer-profile-update')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employee)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            raise Http404("User doesn't exists")
        # context = self.get_context_data(object=self.object)
        return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None):
        obj = self.request.user
        print(obj)
        if obj is None:
            raise Http404("Job doesn't exists")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all()
        context['settings'] = Setting.objects.filter(status=True).first()
        return context
