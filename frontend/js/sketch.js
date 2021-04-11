const boardSize = 10;
const size = 47;
const radius = 8;

var timeLeft = 30;
var score = 0;

function setup() {
  createCanvas(600, 800);
  board = new Board();
  grid = new Grid(75, 145);
  isHolding = false;
  pieces = generatePieces();
}

function draw() {
  background(0);
  noStroke();
  rectMode(CENTER);
  timeLeft -= 1 / 60;
  board.show();
  board.updateHeader(score);
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
    let [x, y] = convert(mouseX, mouseY);
    let success = grid.update(x, y, piece);
    if (success) {
      score += piece.tiles.length;
      timeLeft += piece.tiles.length;
        if (timeLeft > 60) {
          timeLeft = 60;
        }
      if (pieces.length === 0) {
        pieces = generatePieces();
      }
      if (grid.hasLost(pieces)) {
        drawPiecesArray();
        grid.update(x, y, piece);
        grid.show()
        board.updateHeader(`Game Over!\nFinal score: ${score}`);
        noLoop();
      }
      isHolding = false;
    }
  }
  
  if (isHolding) {
    if (keyIsPressed && keyCode === 32) {
      isHolding = false;
      pieces.push(piece);
    }
    piece.update(mouseX, mouseY);
  }

  if (timeLeft <= 0) {
    board.updateHeader(`Time's up!\nFinal score: ${score}`);
    noLoop();
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

function convert(x, y) {
  let newX = Math.floor((x - 50) / 50);
  let newY = Math.floor((y - 120) / 50);
  return [newX, newY];
}
