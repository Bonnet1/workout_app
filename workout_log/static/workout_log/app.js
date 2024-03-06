let exerciseOrder = 0;
let exerciseList = [];

document.addEventListener('DOMContentLoaded', function() {

    //ADD EXERCISE TO WORKOUT
    const addExerciseInput = document.querySelector('.addExerciseInput');
    const addExerciseButton = document.querySelector('button.addExerciseButton');

    //ADD FUNCTIONALITY TO SUBMIT
    document.querySelector('#add_workout').addEventListener('click', () => add_workout());

    addExerciseButton.addEventListener('click', () => {
        let exerciseDetail = {
            order: exerciseOrder,
            exercise: '',
            reps: '',
            sets: '',
            weight: ''
        };
        let list = document.querySelector('#selected_exercises');
        let exercise = document.createElement('div');

        let selectedExercise = document.createElement('INPUT');
        selectedExercise.setAttribute("type", "text")
        selectedExercise.value = addExerciseInput.value;
        selectedExercise.disabled=true;
        exerciseDetail.exercise = addExerciseInput.value;
        exercise.append(selectedExercise)

        let reps = document.createElement("INPUT")
        reps.setAttribute("type", "number")
        reps.placeholder = "Reps"
        reps.onkeyup = () => {
            exerciseDetail.reps = reps.value;
        }
        exercise.append(reps)

        let sets = document.createElement("INPUT")
        sets.setAttribute("type", "number")
        sets.placeholder = "Sets"
        sets.onkeyup = () => {
            exerciseDetail.sets = sets.value;
        }
        exercise.append(sets)

        let weight = document.createElement("INPUT")
        weight.setAttribute("type", "number")
        weight.placeholder = "Weight (lb)"
        weight.onkeyup = () => {
            exerciseDetail.weight = weight.value;
        }
        exercise.append(weight)

        let removeExerciseButton = document.createElement('button')
        removeExerciseButton.innerText = "Remove";
        let order = exerciseOrder;
        removeExerciseButton.addEventListener('click', () => {
            exercise.remove()
            exerciseList = exerciseList.filter(exercise => exercise.order !== order);
        })

        exercise.append(removeExerciseButton)
        exerciseOrder++;
        list.append(exercise);
        exerciseList.push(exerciseDetail);
    });

})

function add_workout() {
    // TODO -- Add check to ensure that all execises include reps, sets, and weight
    
    fetch('/add', {
        method: 'POST',
        body: JSON.stringify(exerciseList)
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => {
        console.log('Error', error);
    });
}