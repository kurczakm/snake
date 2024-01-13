var BOARD_WIDTH;
var BOARD_HEIGHT;

var playerName = 'player1';
var playerColor = 'purple';

const BOARD_TR_PREFIX = 'board_tr_';
const BOARD_TD_PREFIX = 'board_td_';

const LEFT_DIRECTION = 'left';
const RIGHT_DIRECTION = 'right';
const UP_DIRECTION = 'up';
const DOWN_DIRECTION = 'down';

window.addEventListener('DOMContentLoaded', () => {
    const websocket = new WebSocket('ws://localhost:8001/');

    websocket.addEventListener('message', ({ data }) => {
        handleMessage(data)
    });

    document.getElementById('start_button').addEventListener('click', () => {
        const startAction = {
            action: 'start',
            player: {
                name: playerName,
                color: playerColor
            }
        }
        websocket.send(JSON.stringify(startAction));
    });

    document.addEventListener('keydown', event => {
        switch (event.key) {
            case 'ArrowLeft':
                move(LEFT_DIRECTION, websocket);
                break;
            case 'ArrowRight':
                move(RIGHT_DIRECTION, websocket);
                break;
            case 'ArrowUp':
                move(UP_DIRECTION, websocket);
                break;
            case 'ArrowDown':
                move(DOWN_DIRECTION, websocket);
                break;
        }
    });
});

function handleMessage(data) {
    const parsedData = JSON.parse(data);

    switch (parsedData.type) {
        case 'game_info':
            BOARD_WIDTH = parsedData.width;
            BOARD_HEIGHT = parsedData.height;
            createBoard();
            break;
        case 'status':
            renderPosition(parsedData);
            break;
    }
}

function move(direction, websocket) {
    const moveAction = {
        action: 'move',
        direction: direction,
        playerName: playerName
    };

    websocket.send(JSON.stringify(moveAction));
}

function createBoard() {
    const body = document.getElementsByTagName('body')[0];
    
    const board = document.createElement('table');
    board.id = 'board';
    for (var i = 0; i < BOARD_HEIGHT; i++) {
        const tr = document.createElement('tr');
        tr.id = `${BOARD_TR_PREFIX}${i}`;
        for (var j = 0; j < BOARD_WIDTH; j++) {
            const td = document.createElement('td');
            td.id = `${BOARD_TD_PREFIX}${i}_${j}`;
            tr.appendChild(td);
        }
        board.appendChild(tr);
    }
    body.appendChild(board);

    clearBoard();
}

function getBoardCell(x, y) {
    if (!Number.isInteger(x)) {
        throw new Error(`Argument x: ${x} is not an integer!`);
    }

    if (!Number.isInteger(y)) {
        throw new Error(`Argument y: ${y} is not an integer!`);
    }

    if (x < 0 || x >= BOARD_WIDTH) {
        throw new Error(`Argument x: ${x} is out of board width!`);
    }

    if (y < 0 || y >= BOARD_HEIGHT) {
        throw new Error(`Argument y: ${y} is out of board height!`);
    }

    return document.getElementById(`${BOARD_TD_PREFIX}${y}_${x}`);
}

function clearBoard() {
    const cells = document.getElementsByTagName('td');
    console.log(cells);
    for (var i = 0; i < cells.length; i++) {
        cells[i].style.backgroundColor = 'gray';
    }
}


function renderPosition(info) {
    console.log(info);
    clearBoard();

    info.players.forEach((player) => {
        player.bodySegments.forEach((segment) => {
            const cell = getBoardCell(segment[0], segment[1]);
            cell.style.backgroundColor = playerColor;
        });
    });

    info.food.forEach((food) => {
        const cell = getBoardCell(food[0], food[1]);
        cell.style.backgroundColor = 'red';
    });
}
