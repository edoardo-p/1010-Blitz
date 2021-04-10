class Piece {
  constructor(piece) {
    this.tiles = piece.pos;
    this.colour = piece.colour;
  }

  update(x, y, scale=1) {
    this.tiles.forEach(tile => {
      let centerX = tile[0] * 50 * scale + x;
      let centerY = tile[1] * 50 * scale + y;
      fill(this.colour);
      rect(centerX, centerY, size * scale, size * scale, radius);
    });
  }
}
