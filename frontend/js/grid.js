class Grid {

    constructor(topX, topY, width=10, height=10) {
        this.size = 48;
        this.radius = 5;
        this.topX = topX;
        this.topY = topY;
        this.width = width;
        this.height = height;
        this.tiles = [];

        for (let x = 0; x < width; x++) {
            let temp = [];
            for (let y = 0; y < height; y++) {
                temp.push(new Tile()); 
            }
            this.tiles.push(temp);
        }
    }

    show() {
        for (let row = 0; row < this.tiles.length; row++) {
            for (let col = 0; col < this.tiles.length; col++) {
                let tile = this.tiles[row][col];
                if (!tile.empty) {
                    fill(tile.colour);
                    rect(this.topX + col * 50, this.topY + row * 50, this.size, this.size, this.radius);
                }
            }
        }
    }
    
    update(x, y, piece) {
        if (this.checkValid(x, y, piece)) {
            let row = Math.floor((x - 50) / 50);
            let col = Math.floor((y - 120) / 50);
        
            piece.tiles.forEach(coords => {
                let actualRow = coords[0] + row;
                let actualCol = coords[1] + col;
                if (actualRow >= 0 && actualRow < boardSize && actualCol >= 0 && actualCol < boardSize) {
                    this.tiles[coords[1] + col][coords[0] + row].update(piece.colour);
                }
            });
            this.checkLines();
        }
    }

    checkValid(x, y, piece) {
        if (x < 50 || x > 550 || y < 120 || y > 620) {
            return false;
        }
        for (let i = 0; i < piece.tiles.length; i++) {
            let actualRow = piece.tiles[i][0] + Math.floor((x - 50) / 50);
            let actualCol = piece.tiles[i][1] + Math.floor((y - 120) / 50);
            if (actualRow < 0 || actualRow >= this.tiles.length || actualCol < 0 || actualCol >= this.tiles.length) {
                return false;
            }
        }
        return true;
    }

    checkLines() {
        
    }
}
