document.addEventListener('DOMContentLoaded', function() {
    // Event delegation for buttons inside modals
    document.body.addEventListener('click', function(event) {
        if (event.target.id === 'submitSingleGame') {
            handleSingleGameSubmit(event);
        }
    });

    // Event listener for the tournament form submission
    document.body.addEventListener('click', function(event) {
        if (event.target.id === 'submitTournament') {
            handleTournamentSubmit(event);
        }
    });

    // Handle Single Game submit button click
    function handleSingleGameSubmit(event) {
        let playerName = document.getElementById('playerName').value.trim();
        let difficulty = document.getElementById('difficulty').value;

        // Client-side validation
        if (!playerName) {
            alert('Player Name cannot be empty.');
            return;
        }

        // Process form data here
        console.log('Player Name:', playerName);
        console.log('Difficulty:', difficulty);

        // Example: Sending data to your server using fetch
        fetch('/your-endpoint/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')  // Assuming you have a function to get the CSRF token
            },
            body: JSON.stringify({
                playerName: playerName,
                difficulty: difficulty
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    // Handle Tournament form submit button click
    function handleTournamentSubmit(event) {
        let teamName = document.getElementById('teamName').value.trim();
        let numberOfTeams = document.getElementById('numberOfTeams').value.trim();

        // Client-side validation
        if (!teamName) {
            alert('Team Name cannot be empty.');
            return;
        }
        if (!numberOfTeams || isNaN(numberOfTeams) || numberOfTeams <= 0) {
            alert('Number of Teams must be a positive number.');
            return;
        }

        // Process form data here
        console.log('Team Name:', teamName);
        console.log('Number of Teams:', numberOfTeams);

        // Example: Sending data to your server using fetch
        fetch('/your-endpoint/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')  // Assuming you have a function to get the CSRF token
            },
            body: JSON.stringify({
                teamName: teamName,
                numberOfTeams: numberOfTeams
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    // Function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});