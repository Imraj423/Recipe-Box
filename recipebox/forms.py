from django import forms
from recipebox.models import Author
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RecipeAddForm(forms.Form):
    title = forms.CharField(max_length=50)
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    description = forms.CharField(widget=forms.Textarea)
    time_required = forms.CharField(max_length=100)
    instructions = forms.CharField(widget=forms.Textarea)

class AuthorAddForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = [
            'name',
            'bio'
        ]

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
        )

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)