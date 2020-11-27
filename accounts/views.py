from django.contrib.staticfiles import finders
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
import os
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages, auth
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, FormView, RedirectView, TemplateView, DetailView, UpdateView, ListView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.db import IntegrityError
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# forms
from accounts.forms import *
from accounts.models import User, CV, UserProfile, Education, Service
from jobsapp.models import JobCategory
from SiteSettings.models import Setting
from jobsapp.forms import CreateJobForm


@login_required(login_url='/login')
def profile(request):
    setting = Setting.objects.filter(status=True).first()
    categories = JobCategory.objects.all().order_by('-id')[:8]
    current_user = request.user

    profile = UserProfile.objects.get(user_id=current_user.id)
    degrees = Education.objects.filter(user_id=current_user.id)
    skills = Service.objects.filter(user_id=current_user.id)
    experiences = Experience.objects.filter(user_id=current_user.id)
    interview_process = InterviewProcess.objects.filter(
        user_id=current_user.id)

    benefits = Benefits.objects.filter(user_id=current_user.id)
    projects = Projects.objects.filter(user_id=current_user.id)
    courses = Course.objects.filter(user_id=current_user.id)

    if request.method == 'POST':
        form = CompanyImageForm(
            request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            messages.success(
                request, "Image is uploaded successfully")
            return redirect('accounts:my-profile')

    else:
        form = CompanyImageForm(request.POST)

    context = {'categories': categories,
               'settings': setting,
               'profile': profile,
               'degrees': degrees,
               'skills': skills,
               'experiences': experiences,
               'process': interview_process,
               'form': form,
               'courses': courses,
               'benefits': benefits,
               'projects': projects,

               }
    return render(request, 'accounts/demo_profile.html', context)


@login_required(login_url='/login')
def user_update(request):
    if request.method == "POST":
        if request.user.role == 'employer':
            user_form = EmployerProfileUpdateForm(
                request.POST, instance=request.user)

            profile_form = ProfileUpdateFormEmployer(
                request.POST, request.FILES, instance=request.user.userprofile)
        else:
            user_form = EmployeeProfileUpdateForm(
                request.POST, instance=request.user)
            profile_form = ProfileUpdateForm(
                request.POST, request.FILES, instance=request.user.userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request, "Your Profile is updated successfully")
            return redirect('accounts:my-profile')
    else:
        # EMPLOYER UPDATE
        if request.user.role == 'employer':
            user_form = EmployerProfileUpdateForm(instance=request.user)
            profile_form = ProfileUpdateFormEmployer(
                instance=request.user.userprofile)
        # EMPLYEE UPDATE
        else:
            user_form = EmployeeProfileUpdateForm(instance=request.user)
            profile_form = ProfileUpdateForm(instance=request.user.userprofile)

        setting = Setting.objects.filter(status=True).first()
        category = JobCategory.objects.all()
    context = {
        'categories': category,
        'user_form': user_form,
        'profile_form': profile_form,
        'settings': setting,

    }

    return render(request, 'accounts/user_update.html', context)


@login_required(login_url='/login')  # Check login
def password_change(request):
    url = request.META.get("HTTP_REFERER")
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('accounts:my-profile')
        else:
            return render(request, 'accounts/password_change.html', {'form': form})
            # messages.error(
            #     request, 'Error' + str(form.errors))
            # return HttpResponseRedirect(url)
    else:
        category = JobCategory.objects.all()
        setting = Setting.objects.filter(status=True).first()
        form = PasswordChangeForm(request.user)
        return render(request, 'accounts/password_change.html', {'form': form, 'categories': category, 'settings': setting,
                                                                 })


# ------------------------------------------------------------
#                      EDUCATION
# -------------------------------------------------------------

class AddEducationView(LoginRequiredMixin, CreateView):
    form_class = AddEducationForm
    template_name = 'accounts/add_education.html'
    success_url = reverse_lazy('accounts:my-profile')

    def form_valid(self, form):
        request = self.request
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all()
        context['settings'] = Setting.objects.filter(status=True).first()
        return context


class EducationUpdateView(LoginRequiredMixin, UpdateView):
    model = Education
    form_class = EducationUpdateForm
    template_name = 'accounts/update_edu.html'
    success_url = reverse_lazy('accounts:my-profile')
    pk_url_kwarg = 'edu_id'

    def form_valid(self, form):
        request = self.request
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def test_func(self):
        edu = self.get_object()
        if self.request.user == edu.user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all()
        context['settings'] = Setting.objects.filter(status=True).first()
        return context


@login_required(login_url=reverse_lazy('accounts:login'))
def edu_delete(request, edu_id=None):
    try:
        edu = Education.objects.get(user_id=request.user.id, id=edu_id)
        edu.delete()

    except IntegrityError as e:
        print(e.message)
        return HttpResponseRedirect(reverse_lazy('accounts:my-profile'))
    return HttpResponseRedirect(reverse_lazy('accounts:my-profile'))


# ------------------------------------------------------------
#                      SKILL
# ------------------------------------------------------------
class AddSkillView(LoginRequiredMixin, CreateView):
    form_class = AddServiceForm
    template_name = 'accounts/skill_or_service.html'
    success_url = reverse_lazy('accounts:my-profile')

    def form_valid(self, form):
        request = self.request
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all()
        context['settings'] = Setting.objects.filter(status=True).first()
        return context


class SkillUpdateView(LoginRequiredMixin, UpdateView):
    model = Service
    form_class = AddServiceForm
    template_name = 'accounts/update_edu.html'
    success_url = reverse_lazy('accounts:my-profile')
    pk_url_kwarg = 'skill_id'

    def form_valid(self, form):
        request = self.request
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def test_func(self):
        skill = self.get_object()
        if self.request.user == skill.user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all()
        context['settings'] = Setting.objects.filter(status=True).first()
        return context


@login_required(login_url=reverse_lazy('accounts:login'))
def skill_delete(request, skill_id=None):
    try:
        skill = Service.objects.get(user_id=request.user.id, id=skill_id)
        skill.delete()

    except IntegrityError as e:
        print(e.message)
        return HttpResponseRedirect(reverse_lazy('accounts:my-profile'))
    return HttpResponseRedirect(reverse_lazy('accounts:my-profile'))


# ------------------------------------------------------------
#                      EXPERIENCE
# ------------------------------------------------------------

class AddExperienceView(LoginRequiredMixin, CreateView):
    form_class = AddExperienceForm
    template_name = 'accounts/skill_or_service.html'
    success_url = reverse_lazy('accounts:my-profile')

    def form_valid(self, form):
        request = self.request
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all()
        context['settings'] = Setting.objects.filter(status=True).first()
        return context


class ExperienceUpdateView(LoginRequiredMixin, UpdateView):
    model = Experience
    form_class = AddExperienceForm
    template_name = 'accounts/update_edu.html'
    success_url = reverse_lazy('accounts:my-profile')
    pk_url_kwarg = 'exp_id'

    def form_valid(self, form):
        request = self.request
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def test_func(self):
        skill = self.get_object()
        if self.request.user == skill.user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all()
        context['settings'] = Setting.objects.filter(status=True).first()
        return context


@login_required(login_url=reverse_lazy('accounts:login'))
def exp_delete(request, exp_id=None):
    try:
        edu = Experience.objects.get(user_id=request.user.id, id=exp_id)
        edu.delete()

    except IntegrityError as e:
        print(e.message)
        return HttpResponseRedirect(reverse_lazy('accounts:my-profile'))
    return HttpResponseRedirect(reverse_lazy('accounts:my-profile'))


# ------------------------------------------------------------
#                      PROJECTS
# ------------------------------------------------------------

class AddProjectView(LoginRequiredMixin, CreateView):
    form_class = AddProjectForm
    template_name = 'accounts/skill_or_service.html'
    success_url = reverse_lazy('accounts:my-profile')

    def form_valid(self, form):
        request = self.request
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all()
        context['settings'] = Setting.objects.filter(status=True).first()
        return context


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Projects
    form_class = AddProjectForm
    template_name = 'accounts/update_edu.html'
    success_url = reverse_lazy('accounts:my-profile')
    pk_url_kwarg = 'pro_id'

    def form_valid(self, form):
        request = self.request
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def test_func(self):
        skill = self.get_object()
        if self.request.user == skill.user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all()
        context['settings'] = Setting.objects.filter(status=True).first()
        return context


@login_required(login_url=reverse_lazy('accounts:login'))
def pro_delete(request, pro_id=None):
    try:
        edu = Projects.objects.get(user_id=request.user.id, id=pro_id)
        edu.delete()

    except IntegrityError as e:
        print(e.message)
        return HttpResponseRedirect(reverse_lazy('accounts:my-profile'))
    return HttpResponseRedirect(reverse_lazy('accounts:my-profile'))

# ------------------------------------------------------------
#                      COURSE
# ------------------------------------------------------------


class AddCourseyView(LoginRequiredMixin, CreateView):
    form_class = AddCourseForm
    template_name = 'accounts/skill_or_service.html'
    success_url = reverse_lazy('accounts:my-profile')

    def form_valid(self, form):
        request = self.request
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all()[:8]
        context['settings'] = Setting.objects.filter(status=True).first()
        return context


class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = AddCourseForm
    template_name = 'accounts/update_edu.html'
    success_url = reverse_lazy('accounts:my-profile')
    pk_url_kwarg = 'pro_id'

    def form_valid(self, form):
        request = self.request
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def test_func(self):
        skill = self.get_object()
        if self.request.user == skill.user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all()
        context['settings'] = Setting.objects.filter(status=True).first()
        return context


@login_required(login_url=reverse_lazy('accounts:login'))
def cor_delete(request, cor_id=None):
    try:
        edu = Course.objects.get(user_id=request.user.id, id=cor_id)
        edu.delete()

    except IntegrityError as e:
        print(e.message)
        return HttpResponseRedirect(reverse_lazy('accounts:my-profile'))
    return HttpResponseRedirect(reverse_lazy('accounts:my-profile'))

# ------------------------------------------------------------
#                      BENEFITS
# ------------------------------------------------------------


class AddBenefitsView(LoginRequiredMixin, CreateView):
    form_class = AddBenefitsForm
    template_name = 'accounts/skill_or_service.html'
    success_url = reverse_lazy('accounts:my-profile')

    def form_valid(self, form):
        request = self.request
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all()[:8]
        context['settings'] = Setting.objects.filter(status=True).first()
        return context


class BenefitsUpdateView(LoginRequiredMixin, UpdateView):
    model = Benefits
    form_class = AddBenefitsForm
    template_name = 'accounts/update_edu.html'
    success_url = reverse_lazy('accounts:my-profile')
    pk_url_kwarg = 'ben_id'

    def form_valid(self, form):
        request = self.request
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def test_func(self):
        skill = self.get_object()
        if self.request.user == skill.user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all()[:8]
        context['settings'] = Setting.objects.filter(status=True).first()
        return context


@login_required(login_url=reverse_lazy('accounts:login'))
def ben_delete(request, ben_id=None):
    try:
        edu = Benefits.objects.get(user_id=request.user.id, id=ben_id)
        edu.delete()

    except IntegrityError as e:
        print(e.message)
        return HttpResponseRedirect(reverse_lazy('accounts:my-profile'))
    return HttpResponseRedirect(reverse_lazy('accounts:my-profile'))

# ------------------------------------------------------------
#                      INTERVIEW PROCESS
# ------------------------------------------------------------


class InterviewProcessView(LoginRequiredMixin, CreateView):
    template_name = 'accounts/skill_or_service.html'
    form_class = AddInterviewProcessForm
    success_url = reverse_lazy('accounts:my-profile')

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


class InterviewProcessUpdateView(LoginRequiredMixin, UpdateView):
    model = InterviewProcess
    form_class = AddInterviewProcessForm
    template_name = 'accounts/update_edu.html'
    success_url = reverse_lazy('accounts:my-profile')
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        request = self.request
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def test_func(self):
        skill = self.get_object()
        if self.request.user == skill.user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all()[:8]
        context['settings'] = Setting.objects.filter(status=True).first()
        return context


@login_required(login_url=reverse_lazy('accounts:login'))
def interview_delete(request, id=None):
    try:
        edu = InterviewProcess.objects.get(user_id=request.user.id, id=id)
        edu.delete()

    except IntegrityError as e:
        print(e.message)
        return HttpResponseRedirect(reverse_lazy('accounts:my-profile'))
    return HttpResponseRedirect(reverse_lazy('accounts:my-profile'))

# --------------------------------------------------------
#                   USER DETAIL
# --------------------------------------------------------


class UserDetailView(DetailView):
    model = User
    template_name = 'accounts/user_profile.html'
    context_object_name = 'user'

   # this function serves the product id
    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(User, id=id_)

    # this will server siteSettings data to this view
    def get_context_data(self, **kwargs):
        id_ = self.kwargs.get("id")
        context = super().get_context_data(**kwargs)
        context['degrees'] = Education.objects.filter(user_id=id_)
        context['skills'] = Service.objects.filter(user_id=id_)
        context['experiences'] = Experience.objects.filter(user_id=id_)
        context['settings'] = Setting.objects.get(status=True)
        context['categories'] = JobCategory.objects.all().order_by('-id')[:8]
        context['process'] = InterviewProcess.objects.filter(user_id=id_)

        context['benefits'] = Benefits.objects.filter(user_id=id_)
        context['projects'] = Projects.objects.filter(user_id=id_)
        context['courses'] = Course.objects.filter(user_id=id_)
        return context


class CompanyImagesView(ListView):
    model = ComapanyImage
    template_name = 'accounts/company_images.html'
    context_object_name = 'images'

    def get_queryset(self):
        self.id = get_object_or_404(User, id=self.kwargs['user_id'])
        return self.model.objects.filter(user=self.id).order_by('-id')

    # this will server siteSettings data to this view

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = Setting.objects.get(status=True)
        context['categories'] = JobCategory.objects.all().order_by('-id')[:8]
        return context


class RegisterEmployeeView(CreateView):
    model = User
    form_class = EmployeeRegistrationForm
    template_name = 'accounts/employee/register.html'
    success_url = '/'

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect('accounts:login')
        else:
            return render(request, 'accounts/employee/register.html', {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all()
        context['settings'] = Setting.objects.filter(status=True).first()
        return context


class RegisterEmployerView(CreateView):
    model = User
    form_class = EmployerRegistrationForm
    template_name = 'accounts/employer/register.html'
    success_url = '/'

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect('accounts:login')
        else:
            return render(request, 'accounts/employer/register.html', {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all().order_by('-id')[:8]
        context['settings'] = Setting.objects.filter(status=True).first()
        return context

# ---------------------------------------------------------------
#  LOGIN - LOGOUT
# ---------------------------------------------------------------


class LoginView(FormView):
    """
        Provides the ability to login as a user with an email and password
    """
    success_url = '/'
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    extra_context = {
        'title': 'Login'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        if 'next' in self.request.GET and self.request.GET['next'] != '':
            return self.request.GET['next']
        else:
            return self.success_url

    def get_form_class(self):
        return self.form_class

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all().order_by('?')[:8]
        context['settings'] = Setting.objects.filter(status=True).first()
        return context


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/login'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return super(LogoutView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all().order_by('?')[:8]
        context['settings'] = Setting.objects.filter(status=True).first()
        return context


def render_pdf_view(request, id):
    template_path = 'resume/jsresume.html'

    user = User.objects.get(id=id)
    userprofile = UserProfile.objects.filter(user_id=id)
    degrees = Education.objects.filter(user_id=id)
    skills = Service.objects.filter(user_id=id)
    experiences = Experience.objects.filter(user_id=id)
    edu_set = Education.objects.filter(user_id=id)
    experience_set = Experience.objects.filter(user_id=id)
    skills_set = Service.objects.filter(user_id=id)
    courses_set = Course.objects.filter(user_id=id)
    projects_set = Projects.objects.filter(user_id=id)

    if len(skills_set) > 3 or len(edu_set) > 3 or len(experience_set) > 3 or courses_set > 3 or projects_set > 3:
        degrees = Education.objects.filter(user_id=id)[:3]
        degrees_two = Education.objects.filter(user_id=id)[3:6]
        skills = Service.objects.filter(user_id=id)[:3]
        skills_two = Service.objects.filter(user_id=id)[3:6]
        experiences = Experience.objects.filter(user_id=id)[:3]
        experiences_two = Experience.objects.filter(user_id=id)[
            3:6]

        courses = Course.objects.filter(user_id=id)[:3]
        courses_two = Course.objects.filter(user_id=id)[
            3:6]
        projects = Projects.objects.filter(user_id=id)[:3]
        projects_two = Projects.objects.filter(user_id=id)[
            3:6]
        context = {
            'user': user,
            'degrees': degrees,
            'degrees_two': degrees_two,
            'skills': skills,
            'skills_two': skills_two,
            'experiences': experiences,
            'experiences_two': experiences_two,
            'courses': courses,
            'courses_two': courses_two,
            'projects': projects,
            'projects_two': projects_two,

        }

    else:
        degrees = Education.objects.filter(user_id=id)[:3]
        skills = Service.objects.filter(user_id=id)[:3]
        experiences = Experience.objects.filter(user_id=id)[:3]

        context = {
            'user': user,
            'degrees': degrees,
            'skills': skills,
            'experiences': experiences,
        }

    response = HttpResponse(content_type='application/pdf')
    # if we want to download
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
    # if we want to display it
    response['Content-Disposition'] = 'filename="resume.pdf"'
    # find the template and render it
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
        return HttpResponse("We had Some errors <pre>" + html + "</pre")
    return response


class ResumeShowView(DetailView):
    model = User
    template_name = 'resume/resume.html'
    context_object_name = 'user'

    # this function serves the product id

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(User, id=id_)

    # this will server siteSettings data to this view
    def get_context_data(self, **kwargs):
        id_ = self.kwargs.get("id")

        context = super().get_context_data(**kwargs)
        edu_set = Education.objects.filter(user_id=id_)
        experience_set = Experience.objects.filter(user_id=id_)
        skills_set = Service.objects.filter(user_id=id_)
        courses_set = Course.objects.filter(user_id=id_)
        projects_set = Projects.objects.filter(user_id=id_)

        context['userprofile'] = UserProfile.objects.filter(user_id=id_)

        if len(skills_set) > 3:
            context['skills'] = Service.objects.filter(user_id=id_)[:3]
            context['skills_two'] = Service.objects.filter(user_id=id_)[3:6]
        else:
            context['skills'] = Service.objects.filter(user_id=id_)[:3]

        if len(experience_set) > 3:
            context['experiences'] = Experience.objects.filter(user_id=id_)[:3]
            context['experiences_two'] = Experience.objects.filter(user_id=id_)[
                3:6]
        else:
            context['experiences'] = Experience.objects.filter(user_id=id_)[:3]

        if len(edu_set) > 3:
            context['degrees'] = Education.objects.filter(user_id=id_)[:3]
            context['degrees_two'] = Education.objects.filter(user_id=id_)[3:6]
        else:
            context['degrees'] = Education.objects.filter(user_id=id_)[:3]

        if len(courses_set) > 3:
            context['courses'] = Course.objects.filter(user_id=id_)[:3]
            context['courses_two'] = Course.objects.filter(user_id=id_)[3:6]
        else:
            context['courses'] = Course.objects.filter(user_id=id_)[:3]

        if len(projects_set) > 3:
            context['projects'] = Projects.objects.filter(user_id=id_)[:3]
            context['projects_two'] = Projects.objects.filter(user_id=id_)[
                3:6]
        else:
            context['projects'] = Projects.objects.filter(user_id=id_)[:3]

        # context['settings'] = Setting.objects.get(status=True)
        # context['categories'] = JobCategory.objects.all()
        # context['process'] = InterviewProcess.objects.filter(user_id=id_)
        return context


# def resume_show_view(request, *args, **kwargs):
#     resume = CV.objects.get(id=1)

#     context = {
#         'resume': resume,
#     }
#     return render(request, 'resume/jsresume.html', context)


# def jsresume(request):
#     resume = CV.objects.get(id=1)
#     context = {
#         'resume': resume,
#     }
#     return render(request, 'resume/jsresume.html', context)
