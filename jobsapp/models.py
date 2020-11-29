from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from accounts.models import User
from django.urls import reverse


class JobCategory(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(blank=True, null=True,
                             default='default_cat.png', upload_to='cat_pics')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Job Categories"


JOB_TYPE = (
    ('paid', "Paid"),
    ('unpaid', "Unpaid"),
    # ('3', "Internship"),
)


GENDER = (
    ('n/a', "N/A"),
    ('male', "Male"),
    ('female', "Female"),
    ('others', "Others"),
)


class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    description = RichTextField(
        blank=True, null=True, default="Write Your Content Here")
    location = models.CharField(max_length=150)
    type = models.CharField(choices=JOB_TYPE, max_length=10)
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE)
    vacancy = models.PositiveSmallIntegerField(default=1)
    duration = models.PositiveSmallIntegerField(null=True, blank=True)
    last_date = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    filled = models.BooleanField(default=False)
    salary = models.IntegerField(default=0, blank=True)
    gender = models.CharField(choices=GENDER, max_length=6, default='n/a')
    experience = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("jobs:jobs-detail", kwargs={"id": self.id})


class Applicant(models.Model):
    APPLICANT_STATUS = (

        ('0', 'Undefined'),
        ('1', "Selected"),
        ('2', "Rejected"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE,
                            related_name='applicants')
    status = models.CharField(
        max_length=30, choices=APPLICANT_STATUS, default=0)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['user', 'job']

    def __str__(self):
        return self.user.get_full_name()
