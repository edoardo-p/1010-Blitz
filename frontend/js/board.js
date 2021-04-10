class Board {

    constructor() {
        this.spacing = 10
        this.width = 500;

        this.scoreCoords = [300, 60];
        this.scoreHeight = 100;

        this.boardCoords = [300, 370];
        this.boardHeight = 500;

        this.piecesCoords = [300, 705];
        this.pieceHeight = 150;

        this.colour = color(255);
        this.grid = [10, 10];

        this.tileSize = 48;
        this.radius = 5;
    }

    show() {
        fill(this.colour);
        rect(this.scoreCoords[0], this.scoreCoords[1], this.width, this.scoreHeight);
        rect(this.boardCoords[0], this.boardCoords[1], this.width, this.boardHeight);
        rect(this.piecesCoords[0], this.piecesCoords[1], this.width, this.pieceHeight);
        fill(128);
        for (let x = 0; x < this.grid[0]; x++){
            for (let y = 0; y < this.grid[1]; y++){
                rect(this.boardCoords[0] - 225 + x * 50, this.boardCoords[1] - 225 + y * 50, this.tileSize, this.tileSize, this.radius);
            }
        }
    }

    updateScore(score) {
        textSize(50);
        textAlign(CENTER, CENTER);
        fill(0);
        text(score, this.scoreCoords[0], this.scoreCoords[1])

    }
}
