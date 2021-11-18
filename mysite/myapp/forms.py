from django import forms
from django.core import validators
from django.core.validators import validate_unicode_slug
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as auth_user

from . import models
def must_be_unique(value):
    user_objects = auth_user.objects.filter(email=value)
    if len(user_objects) > 0:
        raise forms.ValidationError("Email already exist")
            #always return the cleaned data
    return value

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True,
        validators=[must_be_unique]
    )

    class Meta:
        model = auth_user
        fields = (
            "username",
            "email",
            "password1",
            "password2"
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class MoviesForm(forms.Form):
    movie_field = forms.CharField(label='movies', max_length=240)

    def save(self,request):
        movie_instance = models.MovieModel()
        movie_instance.movie = self.cleaned_data["movie_field"]
        movie_instance.author = request.user
        movie_instance.save()
        return movie_instance
