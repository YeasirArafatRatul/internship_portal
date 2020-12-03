from django.urls import path, include

from .views import *

app_name = "jobs"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search', SearchView.as_view(), name='search'),
    path('company-search', CompanySearchView.as_view(), name='company-search'),
    path('all-companies', Companies.as_view(), name='companies'),
    path('employer/dashboard/', include([
        path('', DashboardView.as_view(), name='employer-dashboard'),
        path('all-applicants', ApplicantsListView.as_view(),
             name='employer-all-applicants'),

        path('applicants/<int:job_id>', ApplicantPerJobView.as_view(),
             name='employer-dashboard-applicants'),
        path('employer/jobs/create', JobCreateView.as_view(),
             name='employer-jobs-create'),
        path('job-update/<int:job_id>',
             JobUpdateView.as_view(), name='job-update'),
        path('mark-filled/<int:job_id>',
             filled, name='job-mark-filled'),

        path('delete-job/<int:job_id>',
             delete, name='delete-job'),

        path('select-employee/<int:applicant_id>',
             select, name='select'),
        path('reject-employee/<int:applicant_id>',
             reject, name='reject'),

    ])),
    path("all-categories/", AllCategories.as_view(), name='all-categories'),
    path('all-jobs-by-company/<int:user_id>',
         IndividualCompanyJobListView.as_view(), name='company-jobs'),
    path('apply-job/<int:job_id>', ApplyJobView.as_view(), name='apply-job'),
    path('applied-jobs/', AppliedJobsView.as_view(), name='applied-jobs'),
    path('jobs', JobListView.as_view(), name='jobs'),
    path('filter-jobs/<int:cat_id>', CatJobListView.as_view(), name='filter-jobs'),
    path('jobs/<int:id>', JobDetailsView.as_view(), name='jobs-detail'),

]
