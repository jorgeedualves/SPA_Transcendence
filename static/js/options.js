document.addEventListener('DOMContentLoaded', function() {
    // Event delegation for buttons inside modals
    document.body.addEventListener('click', function(event) {
        if (event.target.id === 'submitSingleGame') {
            handleSingleGameSubmit();
        } else if (event.target.closest('#tournamentModal form')) {
            event.preventDefault(); // Prevent the default form submission
            handleTournamentSubmit();
        }
    });

    // Handle Single Game submit button click
    function handleSingleGameSubmit() {
        let playerName = document.getElementById('playerName').value;
        let difficulty = document.getElementById('difficulty').value;

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
    function handleTournamentSubmit() {
        let teamName = document.getElementById('teamName').value;
        let numberOfTeams = document.getElementById('numberOfTeams').value;

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