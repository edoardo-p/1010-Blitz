class Grid {

    constructor(topX, topY, tiles=undefined) {
        this.topX = topX;
        this.topY = topY;
        this.tiles = tiles;

        if (tiles === undefined) {
            this.tiles = [];

            for (let x = 0; x < boardSize; x++) {
                let temp = [];
                for (let y = 0; y < boardSize; y++) {
                    temp.push(new Tile()); 
                }
                this.tiles.push(temp);
            }
        }
    }

    show() {
        for (let row = 0; row < this.tiles.length; row++) {
            for (let col = 0; col < this.tiles.length; col++) {
                let tile = this.tiles[row][col];
                if (!tile.empty) {
                    fill(tile.colour);
                    rect(this.topX + col * 50, this.topY + row * 50, size, size, radius);
                }
            }
        }
    }
    
    update(x, y, piece) {
        if (this.checkValid(x, y, piece)) {
            piece.tiles.forEach(coords => {
                let actualRow = coords[1] + y;
                let actualCol = coords[0] + x;
                this.tiles[actualRow][actualCol].update(piece.colour);
            });
            this.checkLines();
            return true;
        }
        return false;
    }

    checkValid(x, y, piece) {
        for (let i = 0; i < piece.tiles.length; i++) {
            let actualCol = piece.tiles[i][0] + x;
            let actualRow = piece.tiles[i][1] + y;
            if (actualRow < 0 || actualRow >= this.tiles.length || actualCol < 0 || actualCol >= this.tiles.length || !this.tiles[actualRow][actualCol].empty) {
                return false;
            }
        }
        return true;
    }

    checkLines() {
        let fullRows = [];
        let fullCols = [];
        for (var row = 0; row < this.tiles.length; row++) {
            for (var col = 0; col < this.tiles.length; col++) {
                if (this.tiles[row][col].empty) {
                    break;
                }
            }
            if (col === 10) {
                fullRows.push(row);
            }
        }

        for (var col = 0; col < this.tiles.length; col++) {
            for (var row = 0; row < this.tiles.length; row++) {
                if (this.tiles[row][col].empty) {
                    break;
                }
            }
            if (row === 10) {
                fullCols.push(col);
            }
        }

        this.clearLines(fullRows, fullCols);
    }

    clearLines(fullRows, fullCols) {
        fullRows.forEach(row => {
            for (let i = 0; i < boardSize; i++) {
                this.tiles[row][i].update(0);
            }
        });

        fullCols.forEach(col => {
            for (let i = 0; i < boardSize; i++) {
                this.tiles[i][col].update(0);
            }
        });

        score += 5 * (fullRows.length + fullCols.length) * (fullRows.length + fullCols.length + 1);
    }

    hasLost(pieces) {
        for (let i = 0; i < pieces.length; i++) {
            for (let row = 0; row < boardSize; row++) {
                for (let col = 0; col < boardSize; col++) {
                    if (this.checkValid(row, col, pieces[i])) {
                        return false;
                    }
                }
            }
        }
        return true;
    }
}
