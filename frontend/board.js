class Board {

    constructor() {
        this.spacing = 10
        this.scoreLC = createVector(50,10)
        this.scoreWidth = 500;
        this.scoreHeight = 100;
        this.boardLC = createVector(50,this.scoreLC.y + this.scoreHeight + this.spacing);
        this.boardWidth = this.scoreWidth;
        this.boardHeight = this.boardWidth;
        this.pieceLC = createVector(50,this.boardLC.y + this.boardHeight + this.spacing)
        this.pieceWidth = this.boardWidth;
        this.pieceHeight = 150;
        this.colour = color(255);
    }

    show() {
        noStroke();
        fill(this.colour);
        rect(this.scoreLC.x, this.scoreLC.y, this.scoreWidth, this.scoreHeight);
        rect(this.boardLC.x, this.boardLC.y, this.boardWidth, this.boardHeight);
        rect(this.pieceLC.x, this.pieceLC.y, this.pieceWidth, this.pieceHeight);  
    }

    updateScore(score) {
        textSize(50);
        text(score, this.scoreLC.x + 100, this.scoreLC.y + 70)

    }
}