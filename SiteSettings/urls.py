from django.urls import path
from .views import ContactData, About

app_name = "SiteSettings"

urlpatterns = [
    path('contact', ContactData.as_view(), name='contact'),
    path('about', About.as_view(), name='about'),

]
