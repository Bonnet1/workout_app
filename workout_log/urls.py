from django.urls import path
from . import views

urlpatterns = [
    # Add basic functions
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # Add interactive functionality
    path("exercises", views.exercises, name="exercises"),
    path("add_exercise", views.add_exercise, name="add_exercise"),
    path("add", views.add, name="add"),
    path("update/<int:workout_id>", views.update, name="update")
]