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
        piece.tiles.forEach(coords => {
            console.log(coords);
            this.tiles[coords[1] + x][coords[0] + y].update(piece.colour);
        });
        this.checkLines();
    }

    checkLines() {
        
    }
}
