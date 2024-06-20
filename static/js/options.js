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

        let playerOneName = document.getElementById('playerOneNamePvp').value.trim();
        let playerTwoName = document.getElementById('playerTwoNamePvp').value.trim();
        let skin = document.getElementById('skinPvp').value;
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

        let playerOneName = document.getElementById('playerOneNameTour').value;
		let playerTwoName = document.getElementById('playerTwoNameTour').value;
		let playerThreeName = document.getElementById('playerThreeNameTour').value.trim();
		let playerFourName = document.getElementById('playerFourNameTour').value.trim();
		let skin = document.getElementById('skinTour').value;

		console.log(playerOneName, playerTwoName, playerThreeName, playerFourName);
        if (!playerOneName || !playerTwoName || !playerThreeName || !playerFourName) {
			alert('Players Name cannot be empty.');
            return;
        }

        // Clear previous data
        sessionStorage.removeItem('singleGameData');
        sessionStorage.removeItem('TournamentData');

        let TourData = {
            playerOneName: playerOneName,
			playerTwoName: playerTwoName,
			playerThreeName: playerThreeName,
			playerFourName: playerFourName,
			skin: skin
        };

        sessionStorage.setItem('TournamentData', JSON.stringify(TourData));
        const eventPlayer = new CustomEvent('playerDataReady', { detail: 'TournamentData' });
        document.dispatchEvent(eventPlayer);
        loadContent('/game/tournament/', TourData, false, initAll);
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

