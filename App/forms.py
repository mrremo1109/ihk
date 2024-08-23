from django import forms
from django.contrib.auth.models import User
from .models import Job_Seeker, Recruiter

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = Job_Seeker
        fields = ['phone', 'address', 'resume', 'latitude', 'longitude']

class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = Recruiter
        fields = ['phone', 'company', 'address', 'latitude', 'longitude']
