import json
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

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

        # TODO - Create JSON object containing all exercises and exercise details for every workout

        # TODO - Change status of workout from index page

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
            return HttpResponseRedirect(reverse("exercises"))
        return HttpResponseRedirect(reverse("exercises"), {
            "message": "Invalid Form"
        })

def exercises(request):
      
    available_exercises = Exercise.objects.all().order_by('name')

    return render(request, "workout_log/exercises.html", {
        "exercises": available_exercises,
        "exercise_form": NewExerciseForm(),
    })

@csrf_exempt
def add(request):

    # Check if method is POST
    if request.method == "POST":
        data = json.loads(request.body)
        if len(data) > 0:

            # TODO - check to make sure all exercises have reps, sets, and weights added
            # TODO - add persistance to this page so workout is not lost when adding more exercises

            # Create a new workout
            new_workout = Workout(
                user = request.user,
                status = "Started",

            )
            new_workout.save()

            # Add all relevant exercises to the workout
            for exercise in data:
                new_workout_exercise = WorkoutExercise(
                    exercise = Exercise.objects.get(name=exercise['exercise']),
                    workout = Workout.objects.get(pk=new_workout.id)
                    )
                new_workout_exercise.save()

                new_exercise_detail = WorkoutExerciseDetail(
                    workout_exercise = WorkoutExercise.objects.get(pk=new_workout_exercise.id),
                    reps = exercise['reps'],
                    sets = exercise['sets'],
                    weight = exercise['weight']
                )
                new_exercise_detail.save()
                return JsonResponse(data, safe=False)
        else:
            return JsonResponse({
            "error": "No exercises submitted."
        }, status=400)
        
    
    if request.method == "GET":
        available_exercises = Exercise.objects.all().order_by('name')

        return render(request, "workout_log/workout.html", {
            "exercises": available_exercises
        })


# Add user login, logout, and registration functionality

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "workout_log/login.html", {
                "message": "Invalid username and/or password."
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