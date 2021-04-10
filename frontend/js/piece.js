class Piece {
  constructor(x, y, piece) {
    this.x = x;
    this.y = y;
    this.tiles = piece.pos;
    this.colour = piece.colour;
  }

  show() {
    this.tiles.forEach(pos => {
      let tile = new Tile(this.x + pos[0], this.y + pos[1], this.colour);
      tile.show();
    });
  }
}