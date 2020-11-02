from django import forms

from jobsapp.models import Job, Applicant


class CreateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ('user', 'created_at', 'filled')
        labels = {
            "last_date": "Last Date",
            "company_name": "Company Name",
            "company_description": "Company Description"
        }
        widget = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'descriptsion': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_date': forms.SelectDateWidget(attrs={'class': 'form-control'}),
            'salary': forms.TextInput(attrs={'class': 'form-control'}),
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
