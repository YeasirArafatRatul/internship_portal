
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .models import Setting
from django.views.generic.base import TemplateView
# Create your views here.


class ContactData(TemplateView):
    template_name = 'contactus.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['setting'] = Setting.objects.get(status=True)
        return context


class About(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['setting'] = Setting.objects.get(status=True)
        return context
