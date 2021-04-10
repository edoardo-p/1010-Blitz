class Tile {
  constructor(x, y, colour) {
    this.pos = createVector(x, y);
    this.colour = colour;
    this.side = 50;
    this.radius = 5;
    this.padding = 10;
  }

  show() {
    rectMode(CENTER);
    let centerX = this.side / 2 + this.pos.x;
    let centerY = this.side / 2 + this.pos.y;
    fill(this.colour);
    rect(centerX, centerY, this.side - this.padding, this.side - this.padding, this.radius);
  }
}
