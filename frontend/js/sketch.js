const boardSize = 10;
const size = 47;
const radius = 8;

var score = 0;

function setup() {
  createCanvas(600, 800);
  board = new Board();
  grid = new Grid(75, 145, boardSize, boardSize);
  isHolding = false;
  pieces = generatePieces();
}

function draw() {
  background(128);
  noStroke();
  rectMode(CENTER);

  board.show();
  board.updateScore(score);
  drawPiecesArray();
  grid.show();

  if (mouseIsPressed && !isHolding) {
    if (mouseY >= 630 && mouseY <= 780) {
      let slot = Math.floor((mouseX - 50) / 187.5);
      piece = pieces[slot];
      pieces.splice(slot, 1);
      isHolding = true;
    }
  }

  if (mouseIsPressed && isHolding) {
    let success = grid.update(mouseX, mouseY, piece);
    if (success) {
      score += piece.tiles.length;
      if (pieces.length === 0) {
        pieces = generatePieces();
      }
      isHolding = false;
    }
  }
  
  if (isHolding) {
    piece.update(mouseX, mouseY);
  }
  
}

function drawPiecesArray() {
  for (let i = 0; i < pieces.length; i++) {
    pieces[i].update(125 + i * 175, 705, 0.5);
  }
}

function generatePieces() {
  let pieces = [_11, _22, _33, _12, _13, _14, _15, _21, _31, _41, _51, _r, _t, _l, _j, _R, _T, _L, _J];
  return [
    new Piece(random(pieces)),
    new Piece(random(pieces)),
    new Piece(random(pieces))
  ];
}
