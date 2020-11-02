from django.contrib import admin
from .models import Setting


class AdminContact(admin.ModelAdmin):
    list_display = ['id', 'sitePhone', 'siteEmail', 'siteAddress']


# class AdminSlider(admin.ModelAdmin):
#     list_display = ['title', 'image_tag', 'status']


# Register your models here.
admin.site.register(Setting, AdminContact)
# admin.site.register(Slider, AdminSlider)
