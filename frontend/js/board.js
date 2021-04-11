class Board {

    constructor() {
        this.spacing = 10
        this.width = 500;

        this.scoreCoords = [300, 60];
        this.scoreHeight = 100;

        this.boardCoords = [300, 370];
        this.boardHeight = 500;

        this.boardColour = color(40);
        this.timerColour = color(255, 0, 0);
        this.textColour = color(0, 100, 200);
    }

    show() {
        fill(this.boardColour);
        for (let x = 0; x < boardSize; x++){
            for (let y = 0; y < boardSize; y++){
                rect(this.boardCoords[0] - 225 + x * 50, this.boardCoords[1] - 225 + y * 50, size, size, radius);
            }
        }
    }
    
    updateHeader(score) {
        fill(0);
        rect(this.scoreCoords[0], this.scoreCoords[1], this.width, this.scoreHeight);
        fill(this.timerColour);
        let timerWidth = map(timeLeft, 0, 60, 0, 500);
        if (timerWidth < 0) {
            timerWidth = 0;
        }
        rect(timerWidth / 2 + 50, 107, timerWidth, 3);
        
        fill(this.textColour);
        textSize(50);
        textAlign(CENTER, CENTER);
        text(score, this.scoreCoords[0], this.scoreCoords[1])
    }
}
