// Function to handle adding a new event
async function addEvent() {}
// Input fields //
const firstname= document.getElementById('firstname').ariaValueMax;
const secondName = document.getElementById('secondName').value;
const eventType = document.getElementById('eventType').value;
const email = document.getElementById('email').value;
// Create an object with the event details
const eventDetails = {
    first_name: firstname,
    second_name: secondName,
    event_type: eventType,
    email: email,
};
// Send a POST request to the server with the event details
const response = await fetch('/events', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(eventDetails)
});

  // Handle the response from the server
  if (response.ok) {
    alert('Event added successfully!');
} else {
    alert('Failed to add event.');
}

