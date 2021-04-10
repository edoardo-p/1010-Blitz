function setup() {
  createCanvas(600, 800);
  board = new Board();
  piece = new Piece(board.boardLC.x, board.boardLC.y, _J);
}

function draw() {
  background(128);
  board.show();
  board.updateScore("hi");



  noStroke();
  piece.show();
  noLoop();
}
