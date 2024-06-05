import { loadContent } from './spa.js';

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
		let playerOneName = document.getElementById('playerOneName').value.trim();
		let playerTwoName = document.getElementById('playerTwoName').value.trim();
		let skin = document.getElementById('skin').value;
	
		if (!playerOneName || !playerTwoName) {
			alert('Player Name cannot be empty.');
			return;
		}
	
		fetch('/singleGame/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': getCookie('csrftoken')
			},
			body: JSON.stringify({
				playerOneName: playerOneName,
				playerTwoName: playerTwoName,
				skin: skin
			})
		})
		.then(response => response.json())
		.then(data => {
			console.log('Success:', data);
			localStorage.setItem('singleGameData', JSON.stringify(data)); // Store data with a unique key
			const event = new CustomEvent('playerDataReady', { detail: 'singleGameData' });
			document.dispatchEvent(event);
			loadContent('pong.html');
		})
		.catch((error) => {
			console.error('Error:', error);
		});
	}
	
	function handleTournamentSubmit(event) {
		let teamName = document.getElementById('teamName').value.trim();
		let numberOfTeams = document.getElementById('numberOfTeams').value.trim();
	
		if (!teamName) {
			alert('Team Name cannot be empty.');
			return;
		}
		if (!numberOfTeams || isNaN(numberOfTeams) || numberOfTeams <= 0) {
			alert('Number of Teams must be a positive number.');
			return;
		}
	
		fetch('/tournament/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': getCookie('csrftoken')
			},
			body: JSON.stringify({
				teamName: teamName,
				numberOfTeams: numberOfTeams
			})
		})
		.then(response => response.json())
		.then(data => {
			console.log('Success:', data);
			localStorage.setItem('tournamentData', JSON.stringify(data)); // Store data with a unique key
			const event = new CustomEvent('playerDataReady', { detail: 'tournamentData' });
			document.dispatchEvent(event);
			loadContent('pong.html');
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