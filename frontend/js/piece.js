class Piece {
  constructor(x, y, piece) {
    this.x = x;
    this.y = y;
    this.tiles = piece.pos;
    this.colour = piece.colour;
  }

  update(x, y) {
    // if (x >= 50 && x <= 550 && y >= 120 && y <= 620) {
    //   this.x = Math.floor((x - 50) / 50);
    //   this.y = Math.floor((x - 120) / 50);
    // }
    this.tiles.forEach(tile => {
      let centerX = tile[0] * 50 + x;
      let centerY = tile[1] * 50 + y;
      fill(this.colour);
      rect(centerX, centerY, size, size, radius);
    });
  }
}
