from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from accounts.models import User


class JobCategory(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Job Categories"


JOB_TYPE = (
    ('1', "Paid"),
    ('2', "Unpaid"),
    # ('3', "Internship"),
)


class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    description = RichTextField(
        blank=True, null=True, default="Write Your Content Here")
    location = models.CharField(max_length=150)
    type = models.CharField(choices=JOB_TYPE, max_length=10)
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE)
    last_date = models.DateTimeField()
    company_name = models.CharField(max_length=100)
    company_description = models.CharField(max_length=300)
    website = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(default=timezone.now)
    filled = models.BooleanField(default=False)
    salary = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.title


class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE,
                            related_name='applicants')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['user', 'job']

    def __str__(self):
        return self.user.get_full_name()
