from django import forms
from .models import Student

class StudentSignupForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'name', 'email', 'password', 'phone', 'address']
        widgets = {
            'password': forms.PasswordInput(),
        }
