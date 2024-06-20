import { loadContent } from './spa-utils.js';
import {initAll} from './render_canvas.js';

document.addEventListener('DOMContentLoaded', function() {
    document.body.addEventListener('click', function(event) {
        if (event.target.id === 'submitSingleGame') {
            handleSingleGameSubmit(event);
        } else if (event.target.id === 'submitTournament') {
            handleTournamentSubmit(event);
        }
    });
    // Function to attach event listeners to radio buttons
    function attachEventListeners() {
        const pvpRadio = document.getElementById('pvp');
        const pveRadio = document.getElementById('pve');

        if (pvpRadio && pveRadio) {
            pvpRadio.addEventListener('change', function() {
                togglePlayerTwoInput();
            });

            pveRadio.addEventListener('change', function() {
                togglePlayerTwoInput();
            });
        }
    }

    // Function to toggle the display of player two input field
    function togglePlayerTwoInput() {
        const pvpSelected = document.getElementById('pvp').checked;
        const playerTwoContainer = document.getElementById('playerTwoNameContainer');
        if (pvpSelected) {
            playerTwoContainer.style.display = 'block';
        } else {
            playerTwoContainer.style.display = 'none';
        }
    }

    function handleSingleGameSubmit(event) {
        event.preventDefault();

        let playerOneName = document.getElementById('playerOneName').value.trim();
        let playerTwoName = document.getElementById('playerTwoName').value.trim();
        let skin = document.getElementById('skin').value;
        const gameMode = document.querySelector('input[name="gameMode"]:checked').value;

        if (!playerOneName || (gameMode === 'PVP' && !playerTwoName)) {
            alert('Player Name cannot be empty.');
            return;
        }

        // Clear previous data
        sessionStorage.removeItem('singleGameData');
        sessionStorage.removeItem('TournamentData');

        let data = {
            playerOneName: playerOneName,
            playerTwoName: gameMode === 'PVP' ? playerTwoName : null,
            skin: skin,
            mode: gameMode
        };
        sessionStorage.setItem('singleGameData', JSON.stringify(data)); // Store data with a unique key
        const eventPlayer = new CustomEvent('playerDataReady', { detail: 'singleGameData' });
        document.dispatchEvent(eventPlayer);
        loadContent('/game/pong/', data, false, initAll);
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

        // Clear previous data
        sessionStorage.removeItem('singleGameData');
        sessionStorage.removeItem('TournamentData');

        let data = {
            teamName: teamName,
            numberOfTeams: numberOfTeams
        };

        sessionStorage.setItem('TournamentData', JSON.stringify(data));
        const eventPlayer = new CustomEvent('playerDataReady', { detail: 'TournamentData' });
        document.dispatchEvent(eventPlayer);
        loadContent('/game/tournament/', data, false, initAll);
    }

    // MutationObserver to detect when the modal is added to the DOM
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.addedNodes.length) {
                const singleGameModal = document.getElementById('singleGameModal');
                if (singleGameModal) {
                    attachEventListeners();
                    togglePlayerTwoInput();
                }
            }
        });
    });

    // Configure the observer
    const config = { childList: true, subtree: true };
    observer.observe(document.body, config);
});

