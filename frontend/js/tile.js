class Tile {
  constructor(x, y, colour) {
    this.pos = createVector(x, y);
    this.colour = colour;
    this.width = 50;
    this.height = 50;
    this.radius = 10;
    this.padding = 5;
  }

  show() {
    let padded = this.padding / 2;
    fill(0);
    rect(this.pos.x, this.pos.y, this.width, this.height);
    fill(this.colour);
    rect(this.pos.x + padded, this.pos.y + padded, this.width - 2 * padded, this.height - 2 * padded, this.radius);
  }
}