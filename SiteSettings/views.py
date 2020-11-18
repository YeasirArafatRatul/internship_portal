
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .models import Setting
from django.views.generic import TemplateView
from jobsapp.models import JobCategory
# Create your views here.


class ContactData(TemplateView):
    template_name = 'contactus.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = Setting.objects.filter(status=True).first()
        context['categories'] = JobCategory.objects.all()
        return context


class About(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = Setting.objects.filter(status=True).first()
        context['categories'] = JobCategory.objects.all()
        return context
