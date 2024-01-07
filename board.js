var BOARD_WIDTH;
var BOARD_HEIGTH;

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
            action: 'start'
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
            BOARD_HEIGTH = parsedData.height;
            createBoard();
            break;
        case 'positions':
            renderPosition(parsedData);
            break;
    }
}

function move(direction, websocket) {
    const moveAction = {
        action: 'move',
        direction: direction
    };

    websocket.send(JSON.stringify(moveAction));
}

function createBoard() {
    const body = document.getElementsByTagName('body')[0];
    
    const board = document.createElement('table');
    board.id = 'board';
    for (var i = 0; i < BOARD_HEIGTH; i++) {
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

    if (y < 0 || y >= BOARD_HEIGTH) {
        throw new Error(`Argument y: ${y} is out of board height!`);
    }

    return document.getElementById(`${BOARD_TD_PREFIX}${y}_${x}`);
}

function renderPosition(info) {
    console.log(info.players);
    info.players.forEach((player) => {
        const headCell = getBoardCell(player.head[0], player.head[1]);
        headCell.style.backgroundColor = 'red';
    });
}
