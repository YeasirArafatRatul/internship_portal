from django.contrib import admin
from .models import *
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email']


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
admin.site.register(CV)
admin.site.register(Education)
admin.site.register(ComapanyImage)
admin.site.register(InterviewProcess)
