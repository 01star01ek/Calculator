from django import forms
from .models import Lesson, Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name','major','ad_year']

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['classname','classkind','classcredits']

