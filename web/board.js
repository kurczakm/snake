var BOARD_WIDTH;
var BOARD_HEIGHT;

var playerName = 'player' + Math.floor(Math.random() * 1000000);
var playerColor = '#'+(0x1000000+Math.random()*0xffffff).toString(16).substr(1,6);

const BOARD_TR_PREFIX = 'board_tr_';
const BOARD_TD_PREFIX = 'board_td_';

const LEFT_DIRECTION = 'left';
const RIGHT_DIRECTION = 'right';
const UP_DIRECTION = 'up';
const DOWN_DIRECTION = 'down';

window.addEventListener('DOMContentLoaded', () => {
    const websocket = new WebSocket('ws://localhost:8001/');
    handleServerData(websocket);
    handleButtons(websocket);
    sendMoves(websocket);
});

function handleButtons(websocket) {
    document.getElementById('start_button').addEventListener('click', () => {
        const startAction = {
            action: 'start',
            player: {
                name: playerName,
                color: playerColor
            }
        }
        websocket.send(JSON.stringify(startAction));
        removePlayButtonsAndFields();
        showStatus();
    });

    document.getElementById('join_button').addEventListener('click', () => {
        const joinKey = document.getElementById('join_input').value;
        const startAction = {
            action: 'join',
            key: joinKey,
            player: {
                name: playerName,
                color: playerColor
            }
        }
        websocket.send(JSON.stringify(startAction));
        removePlayButtonsAndFields();
        showStatus();
    });
}

function removePlayButtonsAndFields() {
    const startButton = document.getElementById('start_button');
    const joinButton = document.getElementById('join_button');
    const joinInput = document.getElementById('join_input');

    startButton.remove();
    joinButton.remove();
    joinInput.remove();
}

function showStatus() {
    document.getElementById('status_container').style.visibility = 'visible';
}

function sendMoves(websocket) {
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
}

function handleServerData(websocket) {
    websocket.addEventListener('message', ({ data }) => {
        handleMessage(data)
    });
}

function handleMessage(data) {
    const parsedData = JSON.parse(data);

    switch (parsedData.type) {
        case 'game_info':
            BOARD_WIDTH = parsedData.width;
            BOARD_HEIGHT = parsedData.height;
            const joinKey = parsedData.key;
            document.getElementById('game_code').innerHTML = joinKey;
            createBoard();
            break;
        case 'status':
            renderPosition(parsedData);
            const state = parsedData.state;
            document.getElementById('state').innerHTML = state
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
            try {
                const cell = getBoardCell(segment[0], segment[1]);
                cell.style.backgroundColor = player.color;
            } catch (error) {
                // the cell is out off the board
            }
        });
    });

    info.food.forEach((food) => {
        const cell = getBoardCell(food[0], food[1]);
        cell.style.backgroundColor = 'red';
    });
}
