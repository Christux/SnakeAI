class Pad {

    constructor() {

    }

    onKeyPressed(key, action) {
        document.addEventListener('keydown', (event) => {
            if (event.key === key) {
                action();
            }
        });
    }

    onKeyReleased(key, action) {
        document.addEventListener('keyup', (event) => {
            if (event.key === key) {
                action();
            }
        });
    }
}
