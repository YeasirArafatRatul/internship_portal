from django.contrib import admin
from .models import User, CV, UserProfile, Education, Service, ComapanyImage
# Register your models here.

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(CV)
admin.site.register(Education)
admin.site.register(ComapanyImage)
