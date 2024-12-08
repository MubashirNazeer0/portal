from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.validators import RegexValidator
from .models import Profile,Employer,Student,Alumni
import datetime
from dash.models import Advertisement,Posters


def year_choices():
    return [(r, r) for r in range(1984, datetime.date.today().year + 4)]


def current_year():
    return datetime.date.today().year


MM = 'Management and Marketing'
MIS = 'Management and Information System'
FFI = 'Finance and Financial Institutions'
GA = 'General Administration'
AC = 'Accounting'
OM = 'Operations Management'
NONE = ''

DEPT_CHOICES = (
    ('NONE', ''),
    ('MM', 'MANAGEMENT AND MARKETING'),
    ('MIS', 'MANAGEMENT AND INFORMATION SYSTEM'),
    ('FFI', 'FINANCE AND FINANCIAL INSTITUTIONS'),
    ('GA', 'GENERAL ADMINISTRATION'),
    ('AC', 'ACCOUNTING'),
    ('OM', 'OPERATIONS MANAGEMENT'),
)

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

ROLE_CHOICES = [
    ('employer', 'Employer'),
    ('student', 'Student'),
    ('alumni', 'Alumni'),
]
# class ProfileRegisterForm(forms.ModelForm):
#     registration_number = forms.CharField(max_length=12)
#     job_role = forms.CharField(max_length=100, required=False)
#     work_location = forms.CharField(max_length=100, required=False)
#     company = forms.CharField(max_length=200, required=False)
#     passout_year = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year)

#     class Meta:
#         model = Profile
#         fields = ['dept', 'registration_number', 'job_role', 'work_location', 'company']



# class EmployerForm(forms.ModelForm):
#     """
#     Form for Employer-specific data.
#     """
#     class Meta:
#         model = Employer
#         fields = ['company_name', 'work_location', 'job_role']


# class StudentForm(forms.ModelForm):
#     """
#     Form for Student-specific data.
#     """
#     class Meta:
#         model = Student
#         fields = ['dept', 'registration_number', 'passout_year']

# Profile registration form
class ProfileRegisterForm(forms.ModelForm):
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Role")

    class Meta:
        model = Profile
        fields = ['role']

# Employer-specific form
class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['company_name', 'work_location', 'job_role']

# Student-specific form
# class StudentForm(forms.ModelForm):
#     dept = forms.ChoiceField(choices=Profile.DEPT_CHOICES, label="Department")
#     passout_year = forms.TypedChoiceField(
#         coerce=int, choices=year_choices, initial=current_year, label="Passout Year"
#     )

#     class Meta:
#         model = Student
#         fields = ['dept', 'registration_number','cgpa' ,'passout_year']


# class AlumniForm(forms.ModelForm):
#     class Meta:
#         model = Alumni
#         fields = ['dept', 'registration_number','cgpa', 'passout_year','current_job', 'current_company']

class StudentForm(forms.ModelForm):
    dept = forms.ChoiceField(choices=Profile.DEPT_CHOICES, label="Department")
    passout_year = forms.TypedChoiceField(
        coerce=int, choices=year_choices, initial=current_year, label="Graduation Year"  # Changed label here
    )

    class Meta:
        model = Student
        fields = ['dept', 'registration_number', 'cgpa', 'passout_year','cv']


class AlumniForm(forms.ModelForm):
    passout_year = forms.TypedChoiceField(
        coerce=int, choices=year_choices, initial=current_year, label="Graduation Year"  # Changed label here
    )

    class Meta:
        model = Alumni
        fields = ['dept', 'registration_number', 'cgpa', 'passout_year', 'current_job', 'current_company','cv']





class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        return self.cleaned_data['email'].lower()





class ProfileUpdateForm(forms.ModelForm):
    registration_number = forms.CharField(max_length=12, required=False)
    job_role = forms.CharField(max_length=100, required=False)
    work_location = forms.CharField(max_length=100, required=False)
    company = forms.CharField(max_length=200, required=False)

    class Meta:
        model = Profile
        fields = ['dept', 'registration_number', 'job_role', 'work_location', 'company', 'image']

    def clean_registration_number(self):
        return self.cleaned_data['registration_number'].upper()



class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['image']

class PostersForm(forms.ModelForm):
    class Meta:
        model = Posters
        fields = ['image']
        
        
        
        
        
class EmployerSearchForm(forms.Form):
    # title=forms.CharField(max_length=100, required=False, label='Title')
    cgpa = forms.FloatField(required=False, label='CGPA')
    # dept = forms.ChoiceField(choices=Profile.DEPT_CHOICES, required=False, label='Department')
    dept = forms.MultipleChoiceField(
        choices=Profile.DEPT_CHOICES,
        required=False,
        label='Department',
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )    
    
    current_job = forms.CharField(max_length=100, required=False, label='Current Job')
    current_company = forms.CharField(max_length=200, required=False, label='Current Company')
    roll_no = forms.CharField(max_length=12, required=False, label='Roll Number')


class StudentAlumniSearchForm(forms.Form):
    event_subject = forms.CharField(max_length=40, required=False, label='Event Subject')
    # event_date = forms.DateField(required=False, widget=forms.SelectDateWidget(years=range(1984, datetime.date.today().year + 1)), label='Event Date')
    venue = forms.CharField(max_length=200, required=False, label='Event Venue')
    semester= forms.IntegerField(required=False, label='Semester')
    
    
from django.contrib.auth.forms import AuthenticationForm

    
class CustomAuthenticationForm(AuthenticationForm):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('alumni', 'Alumni'),
        ('employer', 'Employer'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label="Role")