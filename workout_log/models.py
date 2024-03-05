from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
    pass

class Workout(models.Model):
    STATUSES = (
        ('Started', 'Started'),
        ('Finished', 'Finished'),
        ('Template', 'Template'),
    )

    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="workouts")
    created_at = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField()
    status = models.CharField(default=STATUSES[0][0], max_length=16, choices=STATUSES)

    def __str__(self):
        return f"{self.user}: {self.status} at {self.modified_at}"

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified_at = timezone.now()
        return super(User, self).save(*args, **kwargs)
    
class Exercise(models.Model):
    BODY_PARTS = (
        ('Forearms', 'Forearms'),
        ('Triceps', 'Triceps'),
        ('Biceps', 'Biceps'),
        ('Neck', 'Neck'),
        ('Shoulders', 'Shoulders'),
        ('Chest', 'Chest'),
        ('Back', 'Back'),
        ('Core', 'Core'),
        ('Upper Legs', 'Upper Legs'),
        ('Glutes', 'Glutes'),
        ('Calves', 'Calves'),
        ('Full Body', 'Full Body'),
        ('Other', 'Other'),
    )
    EQUIPMENT = (
        ('Barbell', 'Barbell'),
        ('Dumbbell', 'Dumbbell'),
        ('Machine', 'Machine'),
        ('Bodyweight', 'Bodyweight'),
        ('Bands', 'Bands'),
        ('Cardio', 'Cardio'),
        ('Other', 'Other'),
    )

    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="exercises")
    body_part = models.CharField(max_length=16, choices=BODY_PARTS)
    video_url = models.CharField(max_length=256, blank=True, null=True)
    equipment = models.CharField(max_length=16, choices=EQUIPMENT)
    name = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.name}"

class WorkoutExercise(models.Model):
    exercise= models.ForeignKey("Exercise", on_delete=models.CASCADE, related_name="workoutexercise")
    workout = models.ForeignKey("Workout", on_delete=models.CASCADE, related_name="workout_exercises")

    def __str__(self):
        return f"{self.workout} - {self.exercise}"

class WorkoutExerciseDetail(models.Model):
    workout_exercise = models.ForeignKey("WorkoutExercise", on_delete=models.CASCADE, related_name="workout_exercise_details")
    reps = models.PositiveIntegerField()
    sets = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.workout_exercise}: {self.sets} sets at {self.reps} at {self.weight} lbs."