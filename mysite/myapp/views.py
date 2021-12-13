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
            return redirect("/login/")
    else:
        form = forms.RegistrationForm()
    context = {
        "title": "Registration Page",
        "form": form
    }
    return render(request,"registration/register.html",context=context)
@login_required
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
            for j in range(len(new_l)):
                if new_l[i]["user"] == new_l[j]["user"]:
                    max += new_l[i]["priority"] + new_l[j]["priority"]
                # else:
                #     max = new_l[j]["priority"]
                    # break
            pair = (max,new_l[i]["user"])
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
def delete_view(request):
    if request.method =="POST":
        form = forms.DeleteForm(request.POST)
        if form.is_valid():
            form.delete_movie(request)
        return redirect("/delete/")
    else:
        form = forms.DeleteForm()
    movie_objects = models.MovieModel.objects.all()
    cur_user = request.user
    user_movie_list = []
    for i in movie_objects:
        if i.author == cur_user:
            user_movie_list.append(i.movie)
    context = {
    "list":user_movie_list,
    "form": form,
    }
    return render(request,"delete.html",context=context)

def createProfile_view(request):
    if request.method =="POST":
        form = forms.ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request)
            return redirect("/createProfile/")
    else:
        form = forms.ProfileForm()
    context = {
    "form": form,
    }
    return render(request,"createProfile.html",context = context)


def profile_view(request):
    cur_user = request.user
    movie_objects = models.MovieModel.objects.all()
    profile_objects = models.ProfileModel.objects.all()
    movie_list=[]
    profile_list=[]
    for i in movie_objects:
        if i.author == cur_user:
            movie_list.append(i.movie)
    for i in profile_objects:
        if i.author == cur_user:
            pair = (i.thumbnail.url,i.about)
            profile_list.append(pair)
        break
    if request.method =="POST":
        form = forms.ProfileForm(request.POST)
    else:
        form = forms.ProfileForm()
    context = {
    "list1" :movie_list,
    "list2":profile_list,
    "form": form,
    }
    return render(request,"profile.html",context=context)


def chat_view(request):
    return render(request, 'chat/chat.html')

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })
