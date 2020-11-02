from django.contrib import admin
from .models import Job, Applicant, JobCategory
# Register your models here.


admin.site.register(Job)
admin.site.register(JobCategory)
admin.site.register(Applicant)
