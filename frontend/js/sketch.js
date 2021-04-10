const boardSize = 10;
const size = 48;
const radius = 5;

function setup() {
  createCanvas(600, 800);
  board = new Board();
  grid = new Grid(75, 145, boardSize, boardSize);
  piece = new Piece(0, 0, getRandomPiece());
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
  piece = new Piece(0, 0, getRandomPiece());
}

function getRandomPiece() {
  let pieces = [_11, _22, _33, _12, _13, _14, _15, _21, _31, _41, _51, _r, _t, _l, _j, _R, _T, _L, _J];
  return random(pieces);
} 
