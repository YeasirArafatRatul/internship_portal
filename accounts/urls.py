from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from jobsapp.views import EditProfileView
from .views import RegisterEmployeeView, RegisterEmployerView, LoginView, LogoutView, UserDetailView

from .views import render_pdf_view, resume_show_view, jsresume, profile, user_update, password_change

app_name = "accounts"

urlpatterns = [
    path('employee/register', RegisterEmployeeView.as_view(),
         name='employee-register'),
    path('employer/register', RegisterEmployerView.as_view(),
         name='employer-register'),
    path('my/profile/', profile,
         name='my-profile'),
    path('user/profile/<int:id>', UserDetailView.as_view(),
         name='user-detail'),

    path('employee/profile/update', EditProfileView.as_view(),
         name='employer-profile-update'),
    path('employee/profile-update', user_update,
         name='profile-update'),
    path('user/profile/password-change', password_change,
         name='password-change'),


    path('logout', LogoutView.as_view(), name='logout'),
    path('login', LoginView.as_view(), name='login'),


    path('employee/resume-download', render_pdf_view,
         name='resumedownload'),
    path('employee/resume', resume_show_view,
         name='resume-show'),
    path('employee/jsresume', jsresume,
         name='jsresume'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
