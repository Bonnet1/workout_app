document.addEventListener('DOMContentLoaded', function() {

    // Select all buttons
    document.querySelectorAll('button').forEach(button => {

        button.style.fontWeight = "bold";

        if (button.dataset.status == "Started") {
            button.style.color = "red";
        } else if (button.dataset.status == "Template") {
            button.style.color = "green";
        } else {
            button.style.color = "blue";
        }
        
        // When a button is clicked, change the state of that workout
        button.onclick = function() {
            toggleStatus(this.dataset.workout, this.dataset.status)
            button.style.color = toggleColor(this.dataset.status)
        }
    })
});

function toggleStatus(workout_id, currentStatus) {
    let newStatus;
    
    if (currentStatus == "Template") {
        // START
        newStatus = "Started";
    } else if (currentStatus == "Started") {
        // END
        newStatus = "Finished";
    } else {
        // Set to template
        newStatus = "Template";
    }
    
    fetch('/update/' + parseInt(workout_id), {
        method: 'PUT',
        body: JSON.stringify({
            status: newStatus
        })
    })
    .then(location.reload());
}

// function toggleColor(status) {
//     let color;
//     if (status == "Template") {
//         color = "green"
//     } else if (status == "Started") {
//         color = "red"
//     } else {
//         color = "blue"
//     }
//     return color;
// }