from django import forms
from django.core import validators
from django.core.validators import validate_unicode_slug
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as auth_user
from django.contrib.sessions.models import Session

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


def same(value):
    user_objects = models.MovieModel.objects.filter(movie=value)
    # field_name = 'author'
    # obj = models.MovieModel.objects.first()
    # field_value = getattr(obj,field_name)
    # a = field_value
    # my_field =models.MovieModel._meta.get_fields()
    # print(a)
    if len(user_objects) > 0:
        raise forms.ValidationError("Movie already exist")
    return value

class MoviesForm(forms.Form):
    movie_field = forms.CharField(label='movies',
     max_length=240,

     # validators=[clean_test],
 )
    def test(self,request,form_class=None):
        form = super().test(form_class)
        movie_name = self.cleaned_data['movie_field']
        cleaned_data = super().clean()
        cc_movie = cleaned_data.get("movie")
        user = request.user
        for instance in models.MovieModel.objects.all():
            if instance.author == user and instance.movie == movie_name:
                raise forms.ValidationError("Movie already exist")
        return movie_name





    def save(self,request):
        movie_instance = models.MovieModel()
        movie_instance.movie = self.cleaned_data["movie_field"]
        movie_instance.author = request.user
        movie_instance.save()
        return movie_instance
