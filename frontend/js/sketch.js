function setup() {
  createCanvas(600, 800);
  board = new Board();
  grid = new Grid(board.boardLC.x, board.boardLC.y);
  piece = new Piece(100, 100, _J);

}

function draw() {
  background(128);
  board.show();
  grid.show();
  board.updateScore("hi");



  background(120);
  noStroke();
  // piece.show();
  noLoop();
}
