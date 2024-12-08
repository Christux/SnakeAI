window.addEventListener('load', () => {

    const socket = io();
    const board = new Board('board')
    
    socket.on('connect', () => {
        //socket.emit('my event', { data: 'I\'m connected!' });
    });

    socket.on('init_board', (data) => {
        shape = JSON.parse(data);
        board.init(shape.height, shape.width);
        socket.emit('start');
    });


    socket.on('error_message', console.error);

    window.addEventListener('keydown', (event) => {
        
        let key = 0;

        switch (event.key) {

            case 'ArrowRight':
                key = 1;
                break;

            case 'ArrowUp':
                key = 2;
                break;

            case 'ArrowLeft':
                key = 3;
                break;

            case 'ArrowDown':
                key = 4;
                break;
        }

        if(key > 0) {
            socket.emit('direction', JSON.stringify({direction: key}));
        }

        if (event.code == 'Space') {
            socket.emit('pause');
        }
    });

    socket.on('update', function (data) {
        data = JSON.parse(data)
        board.update(data.snakeIndexes, data.fruitIndex);
    });
});
