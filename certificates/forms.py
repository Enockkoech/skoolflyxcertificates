from django import forms
from .models import School, Student

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'motto', 'vision_statement', 'logo']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'second_name', 'profile_picture', 'school']
