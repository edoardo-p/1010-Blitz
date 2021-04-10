class Piece {
  constructor(x, y, piece) {
    this.x = x;
    this.y = y;
    this.tiles = piece.pos;
    this.colour = piece.colour;
  }

  update(x, y) {
    this.tiles.forEach(tile => {
      let centerX = tile[0] * 50 + x;
      let centerY = tile[1] * 50 + y;
      fill(this.colour);
      rect(centerX, centerY, size, size, radius);
    });
  }
}
