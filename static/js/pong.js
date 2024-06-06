let ctx, p1_y, p2_y, p1_points, p2_points;
let ball_y_orientation, ball_x_orientation, ball_x, ball_y, b_size = 10, b_speed = 9;
let p1_keyUp, p1_keyDown, p2_keyUp, p2_keyDown, p_speed = 10;
let ev_pause, ev_gameStart, ev_Timer;
let current_frame = 0, update_interval = 60;
let ia = true, predict_ball_y = 0, last_predicted_frame = 0;
const h = 800, w = 1300, p_w = 20, p_h = 100, p1_x = 10, p2_x = w - p_w - 10;

// Global variable to store game data
let gameData = null;
let gameType = '';

function setup() {
    const canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');

    // Retrieve stored data from sessionStorage
    const singleGameData = sessionStorage.getItem('singleGameData');
    const tournamentData = sessionStorage.getItem('TournamentData');

    if (singleGameData) {
        gameData = JSON.parse(singleGameData);
        gameType = 'single';
    } else if (tournamentData) {
        gameData = JSON.parse(tournamentData);
        gameType = 'tournament';
    }
	console.log('Game Data:', gameData);
    if (gameData) {
        console.log('Game Data:', gameData);
        if (gameType === 'single') {
			if (gameData.mode === 'PVP') {
				ia = false
			} 
		}
    }

    // Initialize player positions
    p1_y = p2_y = (h / 2) - (p_h / 2);

    // Initialize player points
    p1_points = 0;
    p2_points = 0;

    ev_pause = false;
    ev_gameStart = false;
    ev_Timer = false;
    initBall();
    let cout = 5;
    let timer = setInterval(function () {
        draw();
        ctx.font = "50px monospace";
        ctx.fillStyle = "#fff";
        ctx.fillText(cout, w / 2, h / 2);
        cout--;
        if (cout == 0) {
            clearInterval(timer);
            ev_gameStart = true;
            setInterval(loop, 1000 / 60);
        }
    }, 1000);
    // Define an interval of 60 fps for the loop
}

function loop() {
    if (ev_pause == false) {
        colision()
        keyEv()
        //move a bola no eixo X e Y
        ball_x += b_speed * ball_x_orientation
        ball_y += b_speed * ball_y_orientation
        draw()
    }
}

function predict_ball(ball_x, ball_y, ball_x_orientation, ball_y_orientation, paddle_x, height) {
    let time_to_hit = (paddle_x - ball_x) / ball_x_orientation

    predict_ball_y = ball_y + ball_y_orientation * time_to_hit

    /* while (predict_ball_y < 0 || predict_ball_y > height) {
    if (predict_ball_y < 0)	{
        predict_ball_y = -predict_ball_y
    }
    else if (predict_ball_y > height) {
        predict_ball_y = 2 * height - predict_ball_y
    }
} */

    return predict_ball_y
}


function colision() {
    //Verifica se a bola está colidindo com o barra do player 1
    if (ball_x >= p1_x && ball_x <= p1_x + b_size && ball_y >= p1_y && ball_y <= p1_y + p_h) {
        ball_x_orientation = 1
    }
    //Verifica se a bola está colidindo com o barra do player 2
    if (ball_x >= p2_x && ball_x <= p2_x + b_size && ball_y >= p2_y && ball_y <= p2_y + p_h) {
        ball_x_orientation = -1
    }
    // verifica se a bola bateu no chão ou no teto
    if (ball_y + b_size >= h || ball_y <= 0)
        ball_y_orientation *= -1

    // verifica se player pontuou 
    if (ball_x + b_size > w) {
        p1_points++
        initBall()
    }
    else if (ball_x < 0) {
        p2_points++
        initBall()
    }
}

function keyEv() {
    if (p1_keyUp == true && p1_y > 0) {
        p1_y -= p_speed
    } else if (p1_keyDown == true && p1_y + p_h < h) {
        p1_y += p_speed
    }
    if (ia == false) {
        if (p2_keyUp == true && p2_y > 0) {
            p2_y -= p_speed
        } else if (p2_keyDown == true && p2_y + p_h < h) {
            p2_y += p_speed
        }
    } else {
        p2_y = ia_move(ball_x, ball_y, ball_x_orientation, ball_y_orientation, p2_x, p2_y, p_speed, h, 0, 0.1)
    }
}

function drawRect(x, y, w, h, color = "#fff") {
    ctx.fillStyle = color
    ctx.fillRect(x, y, w, h)
    ctx.fillStyle = "#000"
}

function draw() {
    // fundo
    drawRect(0, 0, w, h, "#000")
    // player 1
    drawRect(p1_x, p1_y, p_w, p_h)
    // player 2
    drawRect(p2_x, p2_y, p_w, p_h)
    // barra lateral
    drawRect(w / 2 - 5, 0, 5, h)
    // bola
    drawRect(ball_x, ball_y, b_size, b_size)
    // pontuação
    writePoints()
}

function writePoints() {
    ctx.font = "50px monospace";
    ctx.fillStyle = "#fff";
    // w/4 = 1/4 da tela = metade da tela do player 1
    ctx.fillText(p1_points, w / 4, 50);
    // 3*(w/4) = 3/4 da tela = metade da tela do player 2
    ctx.fillText(p2_points, 3 * (w / 4), 50);
}

function initBall() {
    ball_y_orientation = Math.pow(2, Math.floor(Math.random() * 2) + 1) - 3
    ball_x_orientation = Math.pow(2, Math.floor(Math.random() * 2) + 1) - 3
    ball_x = w / 2 - 10
    ball_y = h / 2 - 10
}

document.addEventListener("keydown", function (ev) {
    let timero
    // keyCode 87 = w, keycode 83 = s
    if (ev.key == "w") {
        p1_keyUp = true
    } else if (ev.key == "s") {
        p1_keyDown = true
    }
    // keycode 38 = arrowUp, keycode 40 = arrowDown
    if (ev.key == "ArrowUp")
        p2_keyUp = true
    else if (ev.key == "ArrowDown") {
        p2_keyDown = true
    }
    if (ev.key == "Escape" && ev_gameStart == true) {
        if (ev_pause == false) {
            ev_pause = true
            ctx.font = "50px monospace";
            ctx.fillStyle = "#fff";
            ctx.fillText("Game Paused", w / 2 - 140, h / 2);
        }
        else if (ev_pause == true && ev_Timer == false) {
            ev_Timer = true
            let cout = 5
            let timer = setInterval(function () {
                ctx.font = "50px monospace";
                ctx.fillStyle = "#fff";
                draw()
                ctx.fillText(cout, w / 2, h / 2);
                cout--
                if (cout == 0) {
                    clearInterval(timer)
                    ev_Timer = false
                    ev_pause = false
                }
            }, 1000)
        }
    }
})

function ia_move(ball_x, ball_y, ball_x_orientation, ball_y_orientation, paddle_x, paddle_y, paddle_speed, height, error_margin, smoothing) {

    let hafHeight = p_h / 2

	if(ball_x >= w / 2) {
		if (current_frame - last_predicted_frame >= update_interval) {
			predict_ball_y = predict_ball(ball_x, ball_y, ball_x_orientation, ball_y_orientation, paddle_x, height)
	
			let error = (Math.random() * 2 - 1) * error_margin
			predict_ball_y += error
	
			last_predicted_frame = current_frame
		}
	}
	else {
		predict_ball_y = height / 2
	}


    current_frame++

    let target_y = predict_ball_y - hafHeight
    target_y = Math.max(0, Math.min(height - p_h, target_y))

    // smoothing
    let new_y = paddle_y + (target_y - paddle_y) * smoothing

    if (Math.abs(new_y - paddle_y) > paddle_speed) {
        if (new_y > paddle_y && paddle_y > 0) {
            paddle_y += paddle_speed
        }
        else if (new_y < paddle_y && paddle_y + p_h < h) {
            paddle_y -= paddle_speed
        }
    } else {
        paddle_y = new_y
    }

    // limites

    return paddle_y
}

document.addEventListener("keyup", function (ev) {
    // keyCode 87 = w, keycode 83 = s
    if (ev.key == "w") {
        p1_keyUp = false
    } else if (ev.key == "s") {
        p1_keyDown = false
    }
    // keycode 38 = arrowUp, keycode 40 = arrowDown
    if (ev.key == "ArrowUp")
        p2_keyUp = false
    else if (ev.key == "ArrowDown") {
        p2_keyDown = false
    }
})

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
        mutationsList.forEach(mutation => {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        if (node.querySelector('#canvas')) {
                            setup();
                            observer.disconnect();
                        }
                    }
                });
            }
        });
    });

    observer.observe(targetNode, observerOptions);
});
