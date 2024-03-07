# Workout Log App

#### Video Demo: https://youtu.be/WoC_u0hG0sw

#### Description:

This project helps users plan and track their workouts over time

It can be hard to track workouts using various spreadsheets, pen/paper, and rnadom apps, so I decided to make a simple workout log for my final project.

This app allows a user to do the following:
1. Create an account and login
2. Build a database of exercises to be shared with other users
3. Create a new workout based on a saved exercise and set, rep, and weight variables
4. Start and track progress through a workout
5. Complete a workout
6. View their workout history

Most of the app is only accessible to logged in users, but logged out users are able to view the exercise list (but cannot add new exercises). There are authentication rules on the client and server side.

#### Distinctiveness and Complexity:

 This project combines many of the lessons taught during CS50w, including:

 * Four additional models with complex linkages
 * A customized Django admin panel
 * Authentication on server and client side
 * Dynamic interaction using JavaScript
 * Asynchronous updates to improve UX
 * Git tracking throughout
 * Setting up a project from scratch

 I purposefulyl chose an application that would differ significantly from the other projects completed in this course, while also selecting something that I would use personally. The goal was to gain experience working with Python/Django, JavaScript, and Jinja to create the workflows and UX I wanted.

 This project is also a great jumping off point to adding other modules to cover AI/ML and social networking in the future.

#### How to Run:

```pip install -r requirements.txt```

```python makemigrations```

```python migrate```

```python manage.py runserver```

#### Technologies used in developing this application include:

#### Front End:
* HTML/CSS
* JavaScript / AJAX
* Jinja

**Static Files**:
* app.js: Functions to allow a user to create a dynamic workout list without calling the server. Creates a list object named exerciseList and updates as the user interacts with their planned workout on the page. The add_workout() function checks to ensure that all fields have been completed and alerts the user if they have missed anything. The list is then sent to the /add route using a POST method after converting the exerciseList object to a JSON.

* index.js: Allows for dynamic interaction with each workout on the index page, including adjusting the button color depending on the status of the workout. The toggleStatus() function takes a workout id and it's current status and changes to the next status on the server before reloading the page to show the changes.

* styles.css: Additional styling to navbar and number input fields to improve UX.

* NOTE: Bootstrap is used for additional UI styling.

**Template Files**:
* exercises.html: shows all current exercises and a form to add a new exercise for logged in users
* index.html: renders the available workouts as individual cards for the current user if logged in
* layout.html: common styling for html pages, including navbar that dynamically adjust login / log out based on user status
* login.html: allows the user to login to the app or click to register a new account
* register.html: allows a new user to create an account
* workout.html: allows the user to create a new workout using a form and dynamically generated lists if logged in

#### Back End:
* Python / Django
* Sqlite3

**views.py**:

* /: Main index page shows a list of all workouts matched to the loged in user. From this page the user can start a workout, check off exercises as they are completed, and complete a workout.

* /login_view: Uses Django auth framework to login a registered user.

* /logout_view: Uses Django auth framework to log out the current user.

* /register: Uses Django auth framework to register a new account.

* /add_exercises: Receives a POST command to create a new exercise in the database.

* /exercises: Renders a HTML page containing all current exercises available in the database.

* /add: Returns a form to dynamically create a new workout from the database of available exercises when it receives a GET command. Creates a new workout based on the completed form when it receives a POST command.

* /update: Used to change the status of a workout between Template, Started, and Finished.

**models.py**:

The Django sqlite database handles the following models:

* User: Stores the name and email address of every registered user with unique id and creation date.

* Workout: Creates a unique workout and logs creator, created and modified timestamps, and current status

* Exercise: Creates a new exercise with a body part, equipment needed, name, and url of a video walkthrough

* WorkoutExercise: Creates a unique instance of an exercise to be performed in a workout by joining those models together.

* WorkoutExerciseDetail: Records the planned reps, sets, adn weight for a unique exercise in a unique workout.


Models and DB structure inspired by https://github.com/vladislavalerievich/gym-log