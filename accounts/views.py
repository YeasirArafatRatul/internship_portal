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
from django.views.generic import CreateView, FormView, RedirectView, TemplateView, DetailView, UpdateView
from django.views.generic.edit import DeleteView
from accounts.forms import *
from accounts.models import User, CV, UserProfile, Education, Service
from jobsapp.models import JobCategory
from SiteSettings.models import Setting
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import ProfileUpdateForm, EmployeeProfileUpdateForm, EmployerProfileUpdateForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.db import IntegrityError


@login_required(login_url='/login')
def profile(request):
    setting = Setting.objects.filter(status=True).first()
    categories = JobCategory.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    print(profile.user.id)

    degrees = Education.objects.filter(user_id=current_user.id)
    skills = Service.objects.filter(user_id=current_user.id)
    experiences = Experience.objects.filter(user_id=current_user.id)

    context = {'categories': categories,
               'settings': setting,
               'profile': profile,
               'degrees': degrees,
               'skills': skills,
               'experiences': experiences,
               }
    return render(request, 'accounts/demo_profile.html', context)


@login_required(login_url='/login')
def user_update(request):
    if request.method == "POST":
        if request.user.role == 'employer':
            user_form = EmployerProfileUpdateForm(
                request.POST, instance=request.user)
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
        category = JobCategory.objects.all()
        # EMPLOYER UPDATE
        if request.user.role == 'employer':
            user_form = EmployerProfileUpdateForm(instance=request.user)
        # EMPLYEE UPDATE
        else:
            user_form = EmployeeProfileUpdateForm(instance=request.user)

        profile_form = ProfileUpdateForm(
            instance=request.user.userprofile)
        setting = Setting.objects.filter(status=True).first()
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
        context = super().get_context_data(**kwargs)
        context['settings'] = Setting.objects.get(status=True)
        context['categories'] = JobCategory.objects.all()
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
        context['categories'] = JobCategory.objects.all()
        context['settings'] = Setting.objects.filter(status=True).first()
        return context


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
        context['categories'] = JobCategory.objects.all()
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
        context['categories'] = JobCategory.objects.all()
        context['settings'] = Setting.objects.filter(status=True).first()
        return context


def render_pdf_view(request):
    template_path = 'resume/resume.html'
    resume = CV.objects.get(id=1)
    context = {
        'resume': resume,
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


def resume_show_view(request, *args, **kwargs):
    resume = CV.objects.get(id=1)
    context = {
        'resume': resume,
    }
    return render(request, 'resume/resume.html', context)


def jsresume(request):
    resume = CV.objects.get(id=1)
    context = {
        'resume': resume,
    }
    return render(request, 'resume/resume.html', context)
