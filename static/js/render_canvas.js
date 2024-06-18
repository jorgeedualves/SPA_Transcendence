let ctx, canvas;
const socket = new WebSocket('ws://127.0.0.1:8000/ws/test/');
let height, width, p_width, p_height;
let p1_keyUp, p1_keyDown, p2_keyUp, p2_keyDown;
let ball_x, ball_y;
let p1_points, p2_points;
let p1X, p2X, p1_y, p2_y;
let isPaused, game_started, ev_timer = false, game_ended;
let skin_map = null;
let ai = true;
let start_draw = false;
let menuItems = [];
let gameData = null;
let gameType = '';

socket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    if (data.static_data) {
        const static_data = data.static_data;
        width = static_data.width;
        height = static_data.height;
        p_width = static_data.p_width;
        p_height = static_data.p_height;
        p1X = static_data.p1_x;
        p2X = static_data.p2_x;
    }
    if (data.game_state) {
        const game_state = data.game_state;
        p1_y = game_state.p1_y;
        p2_y = game_state.p2_y;
        ball_x = game_state.ball_x;
        ball_y = game_state.ball_y;
        p1_points = game_state.p1_score;
        p2_points = game_state.p2_score;
        isPaused = game_state.isPaused;
        game_started = game_state.game_started;
        game_ended = game_state.game_ended;
        if (!isPaused && start_draw) {
            draw();
        }
        if (game_ended) {
            createMenu([{
                text: 'Back to Home', action: () => {
                    window.location.href = '/';
                }
            }]);
            drawMenu();
        }
    }
};

function setup() {
	canvas = document.getElementById('canvas');
	ctx = canvas.getContext('2d');
	const singleGameData = sessionStorage.getItem('singleGameData');
    const tournamentData = sessionStorage.getItem('TournamentData');

    if (singleGameData) {
        gameData = JSON.parse(singleGameData);
		console.log(gameData)
        gameType = 'single';
		skin_map = gameData.skin;
    } else if (tournamentData) {
        gameData = JSON.parse(tournamentData);
        gameType = 'tournament';
    }
    if (gameData) {
		socket.send(JSON.stringify({ event: 'guest', name: gameData.playerTwoName }));
        if (gameType === 'single') {
			if (gameData.mode === 'PVP') {
				ai = false
				socket.send(JSON.stringify({ event: 'ai', state: false }));
			} 
		}
    }
	canvas.addEventListener('click', function(event) {
		if (isPaused || game_started == false) {
			const rect = canvas.getBoundingClientRect();
			const mouseX = event.clientX - rect.left;
			const mouseY = event.clientY - rect.top;
	
			menuItems.forEach(item => {
				if (
					mouseX >= item.x &&
					mouseX <= item.x + item.width &&
					mouseY >= item.y &&
					mouseY <= item.y + item.height
				) {
					item.action();
				}
			});
		}
	});
	start_draw = true;
}

function createMenu(items, options = {}) {
    const defaultOptions = {
        itemWidth: 200,
        itemHeight: 50,
        fontSize: "30px",
        fontColor: "#000",
        bgColor: "#f00",
        padding: 20
    };
    const opts = { ...defaultOptions, ...options };

    menuItems = items.map((item, index) => ({
        text: item.text,
        x: (width - opts.itemWidth) / 2,
        y: (height - opts.itemHeight * items.length - opts.padding * (items.length - 1)) / 2 + index * (opts.itemHeight + opts.padding),
        width: opts.itemWidth,
        height: opts.itemHeight,
        action: item.action
    }));
}

function drawMenu() {
    ctx.fillStyle = "rgba(0, 0, 0, 0.8)";
    ctx.fillRect(0, 0, width, height);

    menuItems.forEach(item => {
        ctx.fillStyle = "#fff";
        ctx.fillRect(item.x, item.y, item.width, item.height);
        ctx.fillStyle = "#000";
        ctx.font = "30px monospace";
        ctx.fillText(item.text, item.x + 20, item.y + item.height / 2 + 10);
    });
}

function draw() {
    // fundo
	if (skin_map == 'map2'){
		drawBasketballCourt();
	}
	else if (skin_map == 'map3'){
		drawSoccerField();
	}
	else {
		drawRect(0, 0, width, height, "#000");
		// player 1
	}
	drawRect(p1X, p1_y, p_width, p_height);
	// player 2
	drawRect(p2X, p2_y, p_width, p_height);
	// barra lateral
	drawRect(width / 2 - 5, 0, 5, height);
	// bola
	drawRect(ball_x, ball_y, 10, 10);
	// pontuação
	writePoints();
}

function drawSoccerField() {
    // Cor do fundo do campo
    ctx.fillStyle = "#0b9b3e";
    ctx.fillRect(0, 0, width, height);

    // Desenhar as linhas brancas do campo
    ctx.strokeStyle = "#ffffff";
    ctx.lineWidth = 2;

    // Linhas de fundo
    ctx.strokeRect(0, 0, width, height);

    // Linha central
    ctx.beginPath();
    ctx.moveTo(width / 2, 0);
    ctx.lineTo(width / 2, height);
    ctx.stroke();

    // Círculo central
    ctx.beginPath();
    ctx.arc(width / 2, height / 2, 70, 0, 2 * Math.PI); // raio arbitrário
    ctx.stroke();

    // Ponto central
    ctx.beginPath();
    ctx.arc(width / 2, height / 2, 3, 0, 2 * Math.PI); // raio pequeno para o ponto central
    ctx.fillStyle = "#ffffff";
    ctx.fill();
    ctx.stroke();

    // Área do gol esquerdo
    ctx.strokeRect(0, height / 2 - 100, 100, 200); // valores arbitrários para largura e altura da área do gol

    // Área do gol direito
    ctx.strokeRect(width - 100, height / 2 - 100, 100, 200); // valores arbitrários para largura e altura da área do gol

    // Círculos pequenos nas áreas do gol
    ctx.beginPath();
    ctx.arc(70, height / 2, 3, 0, 2 * Math.PI); // círculo pequeno na área do gol esquerdo
    ctx.fillStyle = "#ffffff";
    ctx.fill();
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(width - 70, height / 2, 3, 0, 2 * Math.PI); // círculo pequeno na área do gol direito
    ctx.fillStyle = "#ffffff";
    ctx.fill();
    ctx.stroke();
}

function drawBasketballCourt() {
    // Cor do fundo do campo
    ctx.fillStyle = "#D2691E"; // cor laranja
    ctx.fillRect(0, 0, width, height);

    // Desenhar as linhas brancas do campo
    ctx.strokeStyle = "#ffffff";
    ctx.lineWidth = 2;

    // Linhas de fundo
    ctx.strokeRect(0, 0, width, height);

    // Linha central
    ctx.beginPath();
    ctx.moveTo(width / 2, 0);
    ctx.lineTo(width / 2, height);
    ctx.stroke();

    // Círculo central
    ctx.beginPath();
    ctx.arc(width / 2, height / 2, 60, 0, 2 * Math.PI); // raio arbitrário
    ctx.stroke();

    // Área do garrafão esquerdo
    ctx.beginPath();
    ctx.rect(0, height / 2 - 140, 190, 280); // valores arbitrários para largura e altura do garrafão
    ctx.stroke();

    // Área do garrafão direito
    ctx.beginPath();
    ctx.rect(width - 190, height / 2 - 140, 190, 280); // valores arbitrários para largura e altura do garrafão
    ctx.stroke();

    // Semicírculo do garrafão esquerdo
    ctx.beginPath();
    ctx.arc(190, height / 2, 60, 1.5 * Math.PI, 0.5 * Math.PI); // semicírculo esquerdo
    ctx.stroke();

    // Semicírculo do garrafão direito
    ctx.beginPath();
    ctx.arc(width - 190, height / 2, 60, 1.5 * Math.PI, 0.5 * Math.PI, true); // semicírculo direito
    ctx.stroke();

    // Círculo do lance livre esquerdo
    ctx.beginPath();
    ctx.arc(130, height / 2, 60, 0, 2 * Math.PI); // círculo esquerdo
    ctx.setLineDash([5, 5]); // linha tracejada
    ctx.stroke();

    // Círculo do lance livre direito
    ctx.beginPath();
    ctx.arc(width - 130, height / 2, 60, 0, 2 * Math.PI); // círculo direito
    ctx.setLineDash([5, 5]); // linha tracejada
    ctx.stroke();

    // Ponto central
    ctx.beginPath();
    ctx.arc(width / 2, height / 2, 3, 0, 2 * Math.PI); // raio pequeno para o ponto central
    ctx.fillStyle = "#ffffff";
    ctx.fill();
    ctx.stroke();

    // Restaurar a linha contínua
    ctx.setLineDash([]);
}

function writePoints() {
	ctx.font = "50px monospace";
	ctx.fillStyle = "#fff";
	// w/4 = 1/4 da tela = metade da tela do player 1
    ctx.fillText(p1_points, width/4, 50);
	// 3*(w/4) = 3/4 da tela = metade da tela do player 2
    ctx.fillText(p2_points, 3*(width/4), 50);
}

function drawRect(x, y, w, h, color = "#fff") {
    ctx.fillStyle = color;
    ctx.fillRect(x, y, w, h);
}

function countdown(seconds, callback) {
	let remaning = seconds
	ev_timer = true
	const intervalId = setInterval(() => {
		if (remaning > 0) {
			draw();
			// Desenhar o fundo do menu
			ctx.fillStyle = "rgba(0, 0, 0, 0.8)";
			ctx.fillRect(0, 0, canvas.width, canvas.height);
			// Desenhar o texto da contagem regressiva
			ctx.fillStyle = "#fff";
			ctx.font = "50px monospace";
			ctx.fillText(remaning, canvas.width / 2, canvas.height / 2);
			remaning--
		}else {
			ev_timer = false
			clearInterval(intervalId);
			callback();
		}
	}, 1000);
}

document.addEventListener('keydown', function(event) {

	if (ai == false){
		if (event.key == 'ArrowUp') {
			socket.send(JSON.stringify({ event: 'p2_up', state: true }));
		} else if (event.key == 'ArrowDown') {
			socket.send(JSON.stringify({ event: 'p2_down', state: true }));
		}
	}
    if (event.key == 'w' || event.key == 'W') {
        socket.send(JSON.stringify({ event: 'p1_up', state: true }));
    } else if (event.key == 's' || event.key == 'S') {
        socket.send(JSON.stringify({ event: 'p1_down', state: true }));
    }

	if (event.key == 'Escape') {
		if (isPaused == false && game_started == true) {
            createMenu([
                { text: 'Continue', action: () => {
					countdown(3, () => {
					socket.send(JSON.stringify({ event: 'isPaused', state: false }));
				});
			}},
                { text: 'Quit', action: () => {
				window.location.href = '/';
			}}
            ]);
			drawMenu();
			socket.send(JSON.stringify({ event: 'isPaused', state: true }));
		}else if (isPaused == true && ev_timer == false) {
			countdown(3, () => {
				socket.send(JSON.stringify({ event: 'isPaused', state: false }));
			});
		}
		
	}
});

document.addEventListener('keyup', function(event) {
    if (event.key == 'w') {
        socket.send(JSON.stringify({ event: 'p1_up', state: false }));
    }
	else if (event.key == 's') {
		socket.send(JSON.stringify({ event: 'p1_down', state: false }));
	}

	if (event.key == 'ArrowUp') {
		socket.send(JSON.stringify({ event: 'p2_up', state: false }));
	}
	else if (event.key == 'ArrowDown') {
		socket.send(JSON.stringify({ event: 'p2_down', state: false }));
	}
});

document.addEventListener("DOMContentLoaded", function() {
    const targetNode = document.getElementById('content');
    if (!targetNode) {
        console.error('Target node #content not found');
        return;
    }

    const observerOptions = {
        childList: true,
        subtree: true
    };

    const observer = new MutationObserver((mutationsList, observer) => {
        mutationsList.forEach(async mutation => {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(async node => {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        if (node.querySelector('#canvas')) {
                            const userId = await fetchUserId();
                            if (userId) {
                                setup();
                                draw();
                                if (game_started == false) {
                                    createMenu([{
                                        text: 'Start Game', action: () => {
                                            countdown(3, () => {
                                                start_draw = true;
                                                socket.send(JSON.stringify({ event: 'game_started', state: true, user_id: userId }));
                                            });
                                        }
                                    }]);
                                    drawMenu();
                                }
                            } else {
                                console.error('User not authenticated');
                            }
                            observer.disconnect();
                        }
                    }
                });
            }
        });
    });

    observer.observe(targetNode, observerOptions);
});

async function fetchUserId() {
    const response = await fetch('/game/get_current_user/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'same-origin'
    });

    if (response.ok) {
        const userInfo = await response.json();
        return userInfo.id; // Return the user ID
    } else {
        console.error('Failed to fetch user info');
        return null;
    }
}