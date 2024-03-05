import json
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse

from .models import User, Workout, Exercise, WorkoutExercise, WorkoutExerciseDetail

class NewExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        widgets = {'user': forms.HiddenInput()}
        fields = ["name", "body_part", "equipment", "video_url"]

class NewWorkoutExerciseForm(forms.ModelForm):
    class Meta:
        model = WorkoutExerciseDetail
        fields = ["reps", "sets", "weight"]

# Create your views here.

def index(request):

    # Authenticated users view their dashboard
    if request.user.is_authenticated:

        # Display historic workouts
        workouts = Workout.objects.filter(user=request.user)
        return render(request, "workout_log/index.html", {
            "workouts": workouts
        })

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))
    
# Add functionality to create and log a workout
    
def add_exercise(request):
    
    # Check if method is POST
    if request.method == "POST":

        # Capture new exercise data from form
        form = NewExerciseForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():
            new_exercise = form.save(commit=False)
            new_exercise.user = request.user
            new_exercise.save()
            return HttpResponseRedirect(reverse("workout"))
        return HttpResponseRedirect(reverse("workout"), {
            "message": "Invalid Form"
        })

def workout(request):

    ## TODO: Explore using formset factory to alllow dynamic exercises to be added

    # Check if method is POST
    if request.method == "POST":

        # Capture new workout data from form
        form = (request.POST)

        # Create a new workout
        new_workout = Workout(
            user = request.user
        )
        new_workout.save()
        
        # Create all relevant exercises TODO - add multi exercise functionality
        new_workout_exercise = WorkoutExercise(
            exercise = Exercise.objects.get(pk=form['exercise']),
            workout = Workout.objects.get(pk=new_workout.id)
        )
        new_workout_exercise.save()

        # Create relevanet exercise details TODO -- add multi log functionality
        exercise_detail_form = NewWorkoutExerciseForm(request.POST)
        if exercise_detail_form.is_valid():
            new_exercise_detail = exercise_detail_form.save(commit=False)
            new_exercise_detail.workout_exercise = WorkoutExercise.objects.get(pk=new_workout_exercise.id)
            new_exercise_detail.save()

        return HttpResponseRedirect(reverse("workout"))
       
    available_exercises = Exercise.objects.all().order_by('name')

    return render(request, "workout_log/workout.html", {
        "exercises": available_exercises,
        "exercise_form": NewExerciseForm(),
        "exercise_detail_form": NewWorkoutExerciseForm()
    })






# Add user login, logout, and registration functionality

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "workout_log/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "workout_log/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "workout_log/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "workout_log/register.html", {
                "message": "Email address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "workout_log/register.html")