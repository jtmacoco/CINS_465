from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from datetime import datetime,timezone
from operator import itemgetter
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
            form.test(request)
            form.save(request)
            return redirect("/movies/")
    else:
        form = forms.MoviesForm()
    context = {
        "title": "add movies",
        "form": form

    }
    return render(request,"movies.html",context=context)
def match_view(request):
    movie_objects = models.MovieModel.objects.all()
    Movie_list = []
    l = []
    User = get_user_model()
    users = User.objects.all()
    cur_user = request.user
    for m in movie_objects:
        temp = {}
        if cur_user != m.author:
            temp["movie"]=m.movie
            Movie_list += [temp]
    for match in movie_objects:
        t = {"priority":0}
        for j in range(len(Movie_list)):
            if match.movie == Movie_list[j]["movie"] and match.author != cur_user:
                t["priority"] += 1
                t["user"] = match.author
                l += [t]
    seen = set()
    new_l = []
    for d in l:
         t = tuple(d.items())
         if t not in seen:
             seen.add(t)
             new_l.append(d)
    lol = []
    see = set()
    for i in range(len(new_l)):
        max = 0
        if new_l[i]["user"] not in seen:
            for j in range(len(new_l)-1):
                if new_l[i]["user"] == new_l[j]["user"]:
                    max = new_l[i]["priority"] + new_l[j]["priority"]
                else:
                    max = new_l[i]["priority"]
                    break
            pair = (max,new_l[i]["user"])
            max = 0
            seen.add(new_l[i]["user"])
            lol.append(pair)
    sortes = sorted(lol,key=itemgetter(0),reverse = True)
    sort = sorted(new_l, key = lambda i: i["priority"],reverse = True)
    a_key = "priority"
    values_of_key = [a_dict[a_key] for a_dict in sort]
    context = {
        "list":sortes,
    }
    return render(request,"match.html",context=context)
