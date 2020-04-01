from django import forms
from recipebox.models import Author
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Recipe


class RecipeAddForm(forms.Form):    
    title = forms.CharField(max_length=50)
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    description = forms.CharField(widget=forms.Textarea)
    time_required = forms.CharField(max_length=100)
    instructions = forms.CharField(widget=forms.Textarea)

    def __init__(self, user, *args, **kwargs):
        super(RecipeAddForm, self).__init__(*args, **kwargs)
        if user and not user.is_superuser:
            self.fields['author'].queryset = Author.objects.filter(user=user)


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
            'username',
            'password'
        )


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class EditRecipe(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = '__all__'
