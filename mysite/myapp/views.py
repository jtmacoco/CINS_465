from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from . import models
from . import forms
# Create your views here.
def index(request):
    return redirect("/login/")

def logout_view(request):
    logout(request)
    return redirect("/login/")

def register_view(request):
    if request.method =="POST":
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            form.save(request)
            #form = forms.SuggestionForm()
            return redirect("/movies/")
    else:
        form = forms.RegistrationForm()
    context = {
        "title": "Registration Page",
        "form": form
    }
    return render(request,"registration/register.html",context=context)

def movies_view(request):
    if request.method == "POST":
        form = forms.MoviesForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            form.save(request)
            form = forms.MoviesForm
    else:
        form = forms.MoviesForm
    context = {
        "title": "add movies",
        "form": form
    }
    return render(request,"movies.html",context=context)
