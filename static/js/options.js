import { loadContent } from './spa-utils.js';

document.addEventListener('DOMContentLoaded', function() {
    document.body.addEventListener('click', function(event) {
        if (event.target.id === 'submitSingleGame') {
            handleSingleGameSubmit(event);
        } else if (event.target.id === 'submitTournament') {
            handleTournamentSubmit(event);
        }
    });

    function handleSingleGameSubmit(event) {
        event.preventDefault();

        let playerOneName = document.getElementById('playerOneName').value.trim();
        let playerTwoName = document.getElementById('playerTwoName').value.trim();
        let skin = document.getElementById('skin').value;

        if (!playerOneName || !playerTwoName) {
            alert('Player Name cannot be empty.');
            return;
        }

        let data = {
            playerOneName: playerOneName,
            playerTwoName: playerTwoName,
            skin: skin
        };

        loadContent('/game/pong/', data);
    }

    function handleTournamentSubmit(event) {
        event.preventDefault();

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

        let data = {
            teamName: teamName,
            numberOfTeams: numberOfTeams
        };

        loadContent('/tournament/', data);
    }
});