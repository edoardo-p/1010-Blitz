class Tile {
  constructor(colour=0, empty=true) {
    this.colour = colour;
    this.empty = empty;
  }

  // show() {
  //   rectMode(CENTER);
  //   let centerX = this.side / 2 + this.pos.x;
  //   let centerY = this.side / 2 + this.pos.y;
  //   fill(this.colour);
  //   rect(centerX, centerY, this.side - this.padding, this.side - this.padding, this.radius);
  // }

  update(colour) {
    this.colour = colour;
    if (colour === 0) {
      this.empty = true;
    } else {
      this.empty = false;
    }
  }
}
