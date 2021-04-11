const boardSize = 10;
const size = 47;
const radius = 8;

var score = 0;

function setup() {
  createCanvas(600, 800);
  board = new Board();
  grid = new Grid(75, 145);
  isHolding = false;
  pieces = generatePieces();
  agent = new Agent(new Grid(75, 145), pieces);
  agent.nextMove();
}

function draw() {
  background(0);
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
    let [x, y] = convert(mouseX, mouseY);
    let success = grid.update(x, y, piece);
    if (success) {
      score += piece.tiles.length;
      if (pieces.length === 0) {
        pieces = generatePieces();
      }
      if (grid.hasLost(pieces)) {
        board.updateScore(`Game Over!\nFinal score: ${score}`);
        grid.update();
        noLoop();
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
  // let pieces = [_33];
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

function gridMask(grid) {
  let tiling = [];
  for (let row = 0; row < boardSize; row++) {
    let temp = [];
    for (let col = 0; col < boardSize; col++) {
      if (grid.tiles[row][col].empty) { 
        temp.push(0);
      } else {
        temp.push(1);
      }
    }
    tiling.push(temp);
  }
  return tiling;
}
