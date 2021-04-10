function setup() {
  createCanvas(600, 800);
  board = new Board();
  grid = new Grid(75, 145, 10, 10);
  piece = new Piece(4, 4, _L);
}

function draw() {
  background(128);
  noStroke();
  rectMode(CENTER);
  board.show();
  board.updateScore("hi");
  grid.update(piece.x, piece.y, piece);
  grid.show();

  // piece.show();
  noLoop();
}
