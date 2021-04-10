function setup() {
  createCanvas(600, 800);
  board = new Board();
  grid = new Grid(board.boardLC.x, board.boardLC.y);
}

function draw() {
  background(128);
  board.show();
  grid.show();
  board.updateScore("hi");
}
