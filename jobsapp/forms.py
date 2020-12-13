from django import forms

from jobsapp.models import Job, Applicant
from django.forms.widgets import DateInput, EmailInput, TextInput


class CreateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ('user', 'created_at', 'filled',)
        labels = {
            "last_date": "Last Date",
            "company_name": "Company Name",
            "company_description": "Company Description"
        }

        widgets = {
            'title': TextInput(attrs={'class': 'input', 'placeholder': 'ex: Softeware Engineer'}),
            'last_date': DateInput(attrs={'class': 'date', 'placeholder': '00/00/00'}),
            'description': TextInput(attrs={'class': 'input', 'placeholder': 'Job Details'}),
            'location': TextInput(attrs={'class': 'input', 'placeholder': 'Dhaka,Bangladesh'}),
            'vacancy': TextInput(attrs={'class': 'input', 'placeholder': '1'}),
            'duration': TextInput(attrs={'class': 'input', 'placeholder': 'In Months'}),
            'last_time': TextInput(attrs={'class': 'input', 'placeholder': 'mm/dd/yyyy'}),
            'salary': TextInput(attrs={'class': 'input', 'placeholder': 'Leave Blank If Negotiable'}),
            'experience': TextInput(attrs={'class': 'input', 'placeholder': 'In Years'}),
        }

    def is_valid(self):
        valid = super(CreateJobForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        job = super(CreateJobForm, self).save(commit=False)
        if commit:
            job.save()
        return job


class ApplyJobForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ('job',)


class JobUpdateForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ('user', 'created_at',)
        widgets = {
            'title': TextInput(attrs={'class': 'input', 'placeholder': 'ex: Softeware Engineer'}),
            'last_date': DateInput(attrs={'class': 'date', 'placeholder': 'mm/dd/yyyy'}),
            'description': TextInput(attrs={'class': 'input', 'placeholder': 'Job Details'}),
        }
