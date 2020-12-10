from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.forms import TextInput, EmailInput, Select, FileInput
from accounts.models import User, UserProfile
from accounts.models import ComapanyImage, Education, Experience, InterviewProcess, Service, Projects, Benefits, Course
from django.forms.widgets import DateInput

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'))


class EmployeeRegistrationForm(UserCreationForm):
    # gender = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=GENDER_CHOICES)

    def __init__(self, *args, **kwargs):
        super(EmployeeRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['gender'].required = True
        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = "Last Name"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"

        # self.fields['gender'].widget = forms.CheckboxInput()

        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Enter First Name',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Last Name',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Enter Email',
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': 'Enter Password',
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': 'Confirm Password',
            }
        )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',
                  'password1', 'password2', 'gender']
        error_messages = {
            'first_name': {
                'required': 'First name is required',
                'max_length': 'Name is too long'
            },
            'last_name': {
                'required': 'Last name is required',
                'max_length': 'Last Name is too long'
            },
            'gender': {
                'required': 'Gender is required'
            }
        }

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if not gender:
            raise forms.ValidationError("Gender is required")
        return gender

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.role = "employee"
        if commit:
            user.save()
        return user


class EmployerRegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(EmployerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "Company Name"
        # self.fields['address'].label = "Company Address"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"

        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Company Name',
            }
        )
        # self.fields['address'].widget.attrs.update(
        #     {
        #         'placeholder': 'Enter Company Address',
        #     }
        # )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Enter Email',
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': 'Enter Password',
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': 'Confirm Password',
            }
        )

    class Meta:
        model = User
        fields = ['first_name',  'email', 'password1', 'password2']
        error_messages = {
            'first_name': {
                'required': 'First name is required',
                'max_length': 'Name is too long'
            },
            # 'address': {
            #     'required': 'address is required',
            #     'max_length': 'address is too long'
            # }
        }

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.role = "employer"
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields['email'].widget.attrs.update(
            {'placeholder': 'Enter Email'})
        self.fields['password'].widget.attrs.update(
            {'placeholder': 'Enter Password'})

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)

            if self.user is None:
                raise forms.ValidationError("User Does Not Exist.")
            if not self.user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")
            if not self.user.is_active:
                raise forms.ValidationError("User is not Active.")

        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user


class EmployeeProfileUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', "gender")
        widgets = {
            'first_name': TextInput(attrs={'class': 'input', 'placeholder': 'first name'}),
            'last_name': TextInput(attrs={'class': 'input', 'placeholder': 'last name'}),
            'email': EmailInput(attrs={'class': 'input', 'placeholder': 'email'}),

        }

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        del self.fields['password']
        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Enter First Name',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Last Name',
            }
        )


class EmployerProfileUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'email')
        widgets = {
            'first_name': TextInput(attrs={'class': 'input', 'placeholder': 'Company name'}),
            'email': EmailInput(attrs={'class': 'input', 'placeholder': 'email'}),

        }

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        del self.fields['password']
        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Company Name',
            }
        )


# class UserUpdateForm(UserChangeForm):

#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email', "gender")
#         widgets = {
#             'first_name': TextInput(attrs={'class': 'input', 'placeholder': 'first name'}),
#             'last_name': TextInput(attrs={'class': 'input', 'placeholder': 'last name'}),
#             'email': EmailInput(attrs={'class': 'input', 'placeholder': 'email'}),

#         }

#     def __init__(self, *args, **kwargs):
#         super(UserChangeForm, self).__init__(*args, **kwargs)
#         del self.fields['password']

class CompanyImageForm(forms.ModelForm):
    class Meta:
        model = ComapanyImage
        exclude = ('user',)
        widgets = {
            'company_image': FileInput(attrs={'class': 'input', 'placeholder': 'Company Image', }),

        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('about', 'address', 'image',
                  'cover_img', 'website',)
        widgets = {
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'profile picture', }),
            'cover_img': FileInput(attrs={'class': 'input', 'placeholder': 'cover photo', }),
            'about': TextInput(attrs={'class': 'input', 'placeholder': 'Say Something About You...'}),
            'address': TextInput(attrs={'class': 'input', 'placeholder': 'Enter Address'}),
            'website': TextInput(attrs={'class': 'input', 'placeholder': 'https://www.example.com'})
        }


class ProfileUpdateFormEmployer(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('about', 'address', 'image',
                  'cover_img', 'website', 'industry_type', 'employee_no')
        widgets = {
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'profile picture', }),
            'cover_img': FileInput(attrs={'class': 'input', 'placeholder': 'cover photo', }),
            'about': TextInput(attrs={'class': 'input', 'placeholder': 'Say Something About You...'}),
            'address': TextInput(attrs={'class': 'input', 'placeholder': 'Enter Address'}),
            'website': TextInput(attrs={'class': 'input', 'placeholder': 'https://www.example.com'})
        }


class AddEducationForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ('user',)
        widgets = {
            'institute_name': TextInput(attrs={'class': 'input', 'placeholder': 'Institute Name', }),
            'subject': TextInput(attrs={'class': 'input', 'placeholder': 'Discipline', }),
            'passing_year': DateInput(attrs={'class': 'input', 'placeholder': '00/00/00'}),
            'cgpa': TextInput(attrs={'class': 'input', 'placeholder': '4.00'}),
        }


class EducationUpdateForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ('user',)
        widgets = {
            'institute_name': TextInput(attrs={'class': 'input', 'placeholder': 'Institute Name', }),
            'subject': TextInput(attrs={'class': 'input', 'placeholder': 'Discipline', }),
            'passing_year': DateInput(attrs={'class': 'input', 'placeholder': '00/00/00'}),
            'cgpa': TextInput(attrs={'class': 'input', 'placeholder': '4.00'}),
        }


class AddServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        exclude = ('user',)
        widgets = {
            'name': TextInput(attrs={'class': 'input', 'placeholder': ' Skill Name', }),
            'details': TextInput(attrs={'class': 'textarea', 'placeholder': 'Description', }),
        }


class AddExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        exclude = ('user',)
        widgets = {
            'company_name': TextInput(attrs={'class': 'input', 'placeholder': 'Company Name', }),
            'position': TextInput(attrs={'class': 'textarea', 'placeholder': 'What was your position?', }),
            'from_date': DateInput(attrs={'class': 'input', 'placeholder': '00/00/00', }),
            'to_date': DateInput(attrs={'class': 'input', 'placeholder': '00/00/00', }),
        }


class AddInterviewProcessForm(forms.ModelForm):
    class Meta:
        model = InterviewProcess
        exclude = ('user',)
        widgets = {

            'details': TextInput(attrs={'class': 'input', 'placeholder': 'Write Your Content Here', }),
        }


class AddBenefitsForm(forms.ModelForm):
    class Meta:
        model = Benefits
        exclude = ('user',)
        widgets = {
            'details': TextInput(attrs={'class': 'input', 'placeholder': 'Write Your Content Here', }),
        }


class AddProjectForm(forms.ModelForm):
    class Meta:
        model = Projects
        exclude = ('user',)
        widgets = {
            'proj_name': TextInput(attrs={'class': 'input', 'placeholder': 'Your Project Name', }),
            'details': TextInput(attrs={'class': 'input', 'placeholder': 'Write Your Content Here', }),
        }


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ('user',)
        widgets = {
            'course_name': TextInput(attrs={'class': 'input', 'placeholder': 'Your Course Name', }),
            'institute_name': TextInput(attrs={'class': 'input', 'placeholder': 'From Where You Completed This Course?'}),
            'duration': TextInput(attrs={'class': 'input', 'placeholder': 'duration in month', }),
            'details': TextInput(attrs={'class': 'input', 'placeholder': 'Write Your Content Here', }),
        }
