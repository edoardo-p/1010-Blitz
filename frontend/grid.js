class Grid {

    constructor(x, y) {
        this.gridLC = createVector(x + 5, y + 5);
        this.colour = color(255,180,0);
        this.size = 40;
        this.distance = 50;
        this.spacing = 5;
        this.chamfer = 5;
        this.grid = createVector(10, 10);
    }

    show(){
        noStroke();
        fill(this.colour);
        for (let x = 0; x < this.grid.x; x++){
            for (let y = 0; y < this.grid.y; y++){
                rect(this.gridLC.x + this.distance * x, this.gridLC.y + this.distance * y, this.size, this.size, this.chamfer);
            }
        }       
    }
}