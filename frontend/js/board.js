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

        this.colour = color(0);
    }

    show() {
        fill(this.colour);
        rect(this.boardCoords[0], this.boardCoords[1], this.width, this.boardHeight);
        rect(this.piecesCoords[0], this.piecesCoords[1], this.width, this.pieceHeight);
        fill(40);
        for (let x = 0; x < boardSize; x++){
            for (let y = 0; y < boardSize; y++){
                rect(this.boardCoords[0] - 225 + x * 50, this.boardCoords[1] - 225 + y * 50, size, size, radius);
            }
        }
    }
    
    updateScore(score) {
        fill(this.colour);
        rect(this.scoreCoords[0], this.scoreCoords[1], this.width, this.scoreHeight);
        textSize(50);
        textAlign(CENTER, CENTER);
        fill(0, 100, 200);
        text(score, this.scoreCoords[0], this.scoreCoords[1])
    }
}
