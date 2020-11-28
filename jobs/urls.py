from django.contrib import admin
from django.urls import path, include
from background_task.models import Task
from jobsapp.tasks import time_to_live

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('jobsapp.urls')),
    path('', include('accounts.urls')),
    path('blog/', include('blog.urls')),
    path('site-info/', include('SiteSettings.urls')),
]

# time_to_live(repeat=60)
