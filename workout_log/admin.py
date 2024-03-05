from django.contrib import admin

from .models import User, Workout, Exercise, WorkoutExercise, WorkoutExerciseDetail

# Register your models here.

admin.site.register(User)
admin.site.register(Workout)
admin.site.register(Exercise)
admin.site.register(WorkoutExercise)
admin.site.register(WorkoutExerciseDetail)