function setup() {
  createCanvas(600, 800);
  piece = new Piece(100, 100, _12);
}

function draw() {
  background(120);
  noStroke();
  piece.show();
  noLoop();
}
