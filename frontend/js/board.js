class Board {

    constructor(elementId) {
        this.element = new Element(document.getElementById(elementId));
        this.isInitialized = false;
        this.height = 0;
        this.width = 0;
        this.n = 0;
        this.cells = [];
    }

    init(height, width) {
        console.log('init board', height, width);
        this.isInitialized = true;
        this.height = height;
        this.width = width;
        this.n = this.height * this.width;
        this.build();
    }

    build() {
        this.element.removeChildElements();

        const grid = this.element.createChildElement();
        grid.addClass('grid');

        for (let i = 0; i < this.height; i++) {

            const row = grid.createChildElement();
            row.addClass('row');

            for (let j = 0; j < this.width; j++) {

                const cell = row.createChildElement();
                cell.addClass('cell');
                this.cells.push(cell);
            }
        }
    }

    getindexFromCoordinates(i, j) {
        return i * this.width + j;
    }

    /**
     * 
     * @param {number[]} snakeCellIndexes 
     * @param {number} fruitIndex
     */
    update(snakeCellIndexes, fruitIndex) {

        if(this.isInitialized) {
            // Stack of cell indexes
        const cellStack = [];
        for (let i = 0, l = this.n; i < l; i++) {
            cellStack.push(0);
        }

        // Update fruit
        this.cells[fruitIndex].addClass('fruit');
        cellStack[fruitIndex] = 1;

        // Update snake
        snakeCellIndexes.forEach(index => {
            if (index >= 0 && index < this.n) {
                this.cells[index].addClass('snake');
                cellStack[index] = 1;
            }
        });

        // Remaining cells
        cellStack.forEach((value, index) => {
            if (index >= 0 && index < this.n) {
                if (value == 0) {
                    this.cells[index].removeClass('fruit').removeClass('snake');
                }
            }
        });
        }
    }
}
