const boardSize = 10;
const size = 48;
const radius = 5;

function setup() {
  createCanvas(600, 800);
  board = new Board();
  grid = new Grid(75, 145, boardSize, boardSize);
  piece = new Piece(0, 0, _33);
}

function draw() {
  background(128);
  noStroke();
  rectMode(CENTER);
  board.show();
  board.updateScore("hi");
  piece.update(mouseX, mouseY);
  // if (mouseIsPressed) {
  //   grid.update(mouseX, mouseY, piece);
  // }
  grid.show();
}

function mouseClicked() {
  grid.update(mouseX, mouseY, piece);
}
