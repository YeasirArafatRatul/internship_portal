from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from jobsapp.views import EditProfileView
from .views import RegisterEmployeeView, RegisterEmployerView, LoginView, LogoutView, UserDetailView

from .views import render_pdf_view, profile, user_update, password_change
from accounts.views import AddEducationView, AddExperienceView, AddSkillView, CompanyImagesView, EducationUpdateView, ExperienceUpdateView, InterviewProcessView, ResumeShowView, SkillUpdateView, edu_delete, exp_delete, skill_delete
from accounts.views import *

app_name = "accounts"

urlpatterns = [
    path('employee/register', RegisterEmployeeView.as_view(),
         name='employee-register'),
    path('employer/register', RegisterEmployerView.as_view(),
         name='employer-register'),

    # -------------PROFILE-----------------
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


    # -------------EDUCATION---------------
    path('employee/add-education/',
         AddEducationView.as_view(), name='add-education'),
    path('employee/update-education/<int:edu_id>',
         EducationUpdateView.as_view(), name='update-education'),
    path('employee/delete-education/<int:edu_id>',
         edu_delete, name='delete-education'),


    # ---------------SKILL------------------
    path('employee/add-skill/',
         AddSkillView.as_view(), name='add-skill'),
    path('employee/update-skill/<int:skill_id>',
         SkillUpdateView.as_view(), name='update-skill'),
    path('employee/delete-skill/<int:skill_id>',
         skill_delete, name='delete-skill'),



    # -------------EXPERIENCE---------------
    path('employee/add-experience/',
         AddExperienceView.as_view(), name='add-experience'),
    path('employee/update-experience/<int:exp_id>',
         ExperienceUpdateView.as_view(), name='update-experience'),
    path('employee/delete-exp/<int:exp_id>',
         exp_delete, name='delete-experience'),


    # -------------PROJECTS---------------
    path('employee/add-projects/',
         AddProjectView.as_view(), name='add-projects'),
    path('employee/update-projects/<int:pro_id>',
         ProjectUpdateView.as_view(), name='update-projects'),
    path('employee/delete-projects/<int:pro_id>',
         pro_delete, name='delete-projects'),


    # -------------COURSE---------------
    path('employee/add-course/',
         AddCourseyView.as_view(), name='add-courses'),
    path('employee/update-course/<int:cor_id>',
         CourseUpdateView.as_view(), name='update-courses'),
    path('employee/delete-course/<int:cor_id>',
         cor_delete, name='delete-courses'),


    # -------------BENEFITS---------------
    path('employer/add-benefits/',
         AddBenefitsView.as_view(), name='add-benefits'),
    path('employer/update-benefits/<int:ben_id>',
         BenefitsUpdateView.as_view(), name='update-benefits'),
    path('employee/delete-benefits/<int:ben_id>',
         ben_delete, name='delete-benefits'),

    # --------------INTERVIEW PROCESS-----------
    path('employer/add-interview-process/',
         InterviewProcessView.as_view(), name='add-interview-process'),
    path('employer/update-interview-process/<int:id>',
         InterviewProcessUpdateView.as_view(), name='update-interview-process'),
    path('employee/delete-interview-process/<int:id>',
         interview_delete, name='delete-interview-process'),


    # ----------------RESUME-----------------

    path('employee/resume/<int:id>',
         ResumeShowView.as_view(), name='employee-resume'),
    path('employee/resume-download/<int:id>', render_pdf_view,
         name='resumedownload'),
    #     path('employee/resume', resume_show_view,
    #          name='resume-show'),
    #     path('employee/jsresume', jsresume,
    #          name='jsresume'),


    path('all-images-by-company/<int:user_id>',
         CompanyImagesView.as_view(), name='company-images'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
