from django.urls import path
from . import views

urlpatterns = [
    # Add basic functions
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # Add interactive functionality
    path("workout", views.workout, name="workout"),
    path("add_exercise", views.add_exercise, name="add_exercise")
]