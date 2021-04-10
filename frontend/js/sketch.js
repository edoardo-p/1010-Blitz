function setup() {
  createCanvas(600, 800);
  board = new Board();
  // piece = new Piece(board.boardLC.x, board.boardLC.y, _J);
}

function draw() {
  background(128);
  noStroke();
  rectMode(CENTER);
  board.show();
  board.updateScore("hi");



  // piece.show();
  noLoop();
}
