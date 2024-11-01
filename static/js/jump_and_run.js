const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

let gameRunning = false;
let gameOver = false;

let player = {
    x: 50,
    y: 0,
    width: 50,
    height: 50,
    color: "black",
    dy: 0,
    dx: 0,
    gravity: 0.5,
    jumpStrength: -14,
    grounded: false
};

const floor = {
    x: 0,
    y: 350,
    width: canvas.width,
    height: 50,
    color: "green"
};

let obstacles = [];
let score = 0;

function createObstacle() {
    const obstacle = {
        x: canvas.width,
        y: floor.y - 30,
        width: 30,
        height: 30,
        color: "red"
    };
    obstacles.push(obstacle);
}

function startObstacleGeneration() {
    if (gameRunning) {
        createObstacle();

        const minTimeout = 500;
        const randomTime = Math.random() * 2000 + minTimeout; // 500-2500 ms
        setTimeout(startObstacleGeneration, randomTime);
    }
}

function drawPlayer() {
    ctx.fillStyle = player.color;
    ctx.fillRect(player.x, player.y, player.width, player.height);
}

function drawFloor() {
    ctx.fillStyle = floor.color;
    ctx.fillRect(floor.x, floor.y, floor.width, floor.height);
}

function drawObstacles() {
    obstacles.forEach((obstacle) => {
        ctx.fillStyle = obstacle.color;
        ctx.fillRect(obstacle.x, obstacle.y, obstacle.width, obstacle.height);
    });
}

function applyGravity() {
    if (!player.grounded) {
        player.dy += player.gravity;
        player.y += player.dy;
    }

    if (player.y + player.height >= floor.y) {
        player.y = floor.y - player.height;
        player.grounded = true;
        player.dy = 0;
    }
}

function jump() {
    if (player.grounded && gameRunning) {
        player.dy = player.jumpStrength;
        player.grounded = false;
    }
}

function moveObstacles() {
    obstacles.forEach((obstacle, index) => {
        obstacle.x -= 3;

        if (obstacle.x + obstacle.width < 0) {
            obstacles.splice(index, 1);
        }

        if (!obstacle.passed && obstacle.x + obstacle.width < player.x) {
            score++;
            obstacle.passed = true;
        }
    });
}

function checkCollision() {
    obstacles.forEach((obstacle) => {
        if (
            player.x < obstacle.x + obstacle.width &&
            player.x + player.width > obstacle.x &&
            player.y < obstacle.y + obstacle.height &&
            player.y + player.height > obstacle.y
        ) {
            gameRunning = false;
            gameOver = true;
        }
    });
}

function resetGame() {
    player.x = 50;
    player.y = floor.y - player.height;
    player.dy = 0;
    obstacles = [];
    score = 0;
    gameRunning = false;
    gameOver = false;
}

function drawStartButton() {
    const buttonWidth = 120;
    const buttonHeight = 50;
    const buttonX = canvas.width / 2 - buttonWidth / 2;
    const buttonY = canvas.height / 2 - buttonHeight / 2;

    ctx.fillStyle = "white";
    ctx.fillRect(buttonX, buttonY, buttonWidth, buttonHeight);
    ctx.strokeStyle = "black";
    ctx.strokeRect(buttonX, buttonY, buttonWidth, buttonHeight);

    ctx.fillStyle = "black";
    ctx.font = "24px Arial";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText("Starten", canvas.width / 2, canvas.height / 2);
}

function drawScore() {
    ctx.fillStyle = "black";
    ctx.font = "24px Arial";
    ctx.textAlign = "center";
    ctx.textBaseline = "top";
    ctx.fillText("Score: " + score, canvas.width / 2, 30);
}

function drawGameOver() {
    ctx.fillStyle = "red";
    ctx.font = "40px Arial";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText("Game Over!", canvas.width / 2, canvas.height / 4);

    ctx.fillStyle = "black";
    ctx.font = "24px Arial";
    ctx.fillText("Score: " + score, canvas.width / 2, canvas.height / 2 - canvas.height / 8);

    const buttonWidth = 220;
    const buttonHeight = 50;
    const buttonX = canvas.width / 2 - buttonWidth / 2;
    const buttonY = canvas.height / 2;

    ctx.fillStyle = "white";
    ctx.fillRect(buttonX, buttonY, buttonWidth, buttonHeight);
    ctx.strokeStyle = "black";
    ctx.strokeRect(buttonX, buttonY, buttonWidth, buttonHeight);

    ctx.fillStyle = "black";
    ctx.font = "24px Arial";
    ctx.fillText("Nochmal Spielen", canvas.width / 2, buttonY + buttonHeight / 2);
}

function gameLoop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (gameRunning) {
        applyGravity();
        moveObstacles();
        checkCollision();

        drawFloor();
        drawPlayer();
        drawObstacles();
        drawScore();
    } else if (gameOver) {
        drawGameOver();
    } else {
        drawStartButton();
    }

    requestAnimationFrame(gameLoop);
}

// Event Listener für Tastatur
document.addEventListener("keydown", (e) => {
    if (e.code === "Space") {
        e.preventDefault();
        jump();
    }
});

// Event Listener für Touch-Events
document.addEventListener("touchstart", (e) => {
    e.preventDefault();
    jump();
});

canvas.addEventListener("click", (e) => {
    const canvasRect = canvas.getBoundingClientRect();
    const clickX = e.clientX - canvasRect.left;
    const clickY = e.clientY - canvasRect.top;

    const startButtonWidth = 120;
    const startButtonHeight = 50;
    const startButtonX = canvas.width / 2 - startButtonWidth / 2;
    const startButtonY = canvas.height / 2 - startButtonHeight / 2;

    if (!gameRunning && !gameOver && 
        clickX > startButtonX && clickX < startButtonX + startButtonWidth &&
        clickY > startButtonY && clickY < startButtonY + startButtonHeight) {
        resetGame();
        gameRunning = true;
        startObstacleGeneration();
    }

    const restartButtonWidth = 220;
    const restartButtonHeight = 50;
    const restartButtonX = canvas.width / 2 - restartButtonWidth / 2;
    const restartButtonY = canvas.height / 2;

    if (gameOver &&
        clickX > restartButtonX && clickX < restartButtonX + restartButtonWidth &&
        clickY > restartButtonY && clickY < restartButtonY + restartButtonHeight) {
        resetGame();
        gameRunning = true;
        startObstacleGeneration();
    }
});

function resizeCanvas() {
    const containerWidth = canvas.clientWidth;
    const aspectRatio = 2;

    canvas.width = containerWidth;
    canvas.height = Math.min(containerWidth / aspectRatio, 400);

    floor.width = canvas.width;
    floor.y = canvas.height - 50;
    player.y = floor.y - player.height;
}

window.addEventListener("resize", resizeCanvas);
window.addEventListener("load", () => {
    resizeCanvas();
    resetGame();
    gameLoop();
});