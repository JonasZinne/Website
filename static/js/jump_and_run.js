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
    speed: 5,
    gravity: 0.5,
    jumpStrength: -10,
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
        // const randomTime = Math.random() * (3000 - 1500) + 1500; // 1500-3000 ms
        const randomTime = Math.random() * 3000; // 0-3000 ms
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

function movePlayer() {
    player.x += player.dx;

    if (player.x < 0) player.x = 0;
    if (player.x + player.width > canvas.width) player.x = canvas.width - player.width;
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
    obstacles.forEach((obstacle) => {
        obstacle.x -= 3;

        if (obstacle.x + obstacle.width < 0) {
            obstacles.shift();
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
    player.dx = 0;
    player.dy = 0;
    obstacles = [];
    gameRunning = false;
    gameOver = false;
}

function drawStartButton() {
    ctx.fillStyle = "blue";
    ctx.fillRect(canvas.width / 2 - 50, canvas.height / 2 - 25, 100, 50);

    ctx.fillStyle = "white";
    ctx.font = "20px Arial";
    ctx.fillText("Start", canvas.width / 2 - 25, canvas.height / 2 + 10);
}

function drawGameOver() {
    ctx.fillStyle = "red";
    ctx.font = "30px Arial";
    ctx.fillText("Game Over!", canvas.width / 2 - 100, canvas.height / 2);

    ctx.fillStyle = "white";
    ctx.font = "20px Arial";
    ctx.fillText("Click to Restart", canvas.width / 2 - 80, canvas.height / 2 + 50);
}

function gameLoop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (gameRunning) {
        applyGravity();
        movePlayer();
        moveObstacles();
        checkCollision();

        drawFloor();
        drawPlayer();
        drawObstacles();
    } else if (gameOver) {
        drawGameOver();
    } else {
        drawStartButton();
    }

    requestAnimationFrame(gameLoop);
}

document.addEventListener("keydown", (e) => {
    if (e.code === "Space") {
        jump();
    }
    if ((e.code === "ArrowRight" || e.code === "KeyD") && gameRunning) {
        player.dx = player.speed;
    }
    if ((e.code === "ArrowLeft" || e.code === "KeyA") && gameRunning) {
        player.dx = -player.speed;
    }
});

document.addEventListener("keyup", (e) => {
    if (e.code === "ArrowRight" || e.code === "KeyD" || e.code === "ArrowLeft" || e.code === "KeyA") {
        player.dx = 0;
    }
});

canvas.addEventListener("click", (e) => {
    const canvasRect = canvas.getBoundingClientRect();
    const clickX = e.clientX - canvasRect.left;
    const clickY = e.clientY - canvasRect.top;

    if (!gameRunning && !gameOver && 
        clickX > canvas.width / 2 - 50 && clickX < canvas.width / 2 + 50 &&
        clickY > canvas.height / 2 - 25 && clickY < canvas.height / 2 + 25) {
        resetGame();
        gameRunning = true;
        startObstacleGeneration();
    }

    if (gameOver) {
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