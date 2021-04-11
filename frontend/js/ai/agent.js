class Agent {
  constructor(grid, pieces) {
    this.grid = grid;
    this.pieces = pieces;
    console.log(grid);
  }

  nextMove() {
    let gridCopy = this.grid.tiles;
    let bestScore = 0;
    let bestMove = [-1, -1, -1];
    for (let i = 0; i < this.pieces.length; i++) {
      for (let row = 0; row <= boardSize; row++) {
        for (let col = 0; col <= boardSize; col++) {
          let moveScore = this.moveEval(row, col, pieces[i], new Grid(0, 0, gridCopy));
          if (moveScore > bestScore) {
            bestScore = moveScore;
            bestMove = [row, col, i];
          }
        }
      }
    }
    console.log(bestScore, bestMove);
    // this.grid.update(bestMove[0], bestMove[1], this.pieces[bestMove[2]]);
    // this.move(bestMove[0], bestMove[1], this.pieces[bestMove[2]], newGrid);
  }

  moveEval(row, col, piece, grid) {
    let currScore = score;
    if (!grid.update(col, row, piece)) {
      return -1;
    }
    // console.log(score - currScore);
    return score - currScore;
  }
  
  move(row, col, piece, grid) {
    piece.tiles.forEach(tile => {
      grid[row + tile[1]][col + tile[0]] = 1;
    });
  }

  checkValid(row, col, piece, grid) {
    for (let i = 0; i < piece.tiles.length; i++) {
      let tile = piece.tiles[i];
      let actualRow = row + tile[1];
      let actualCol = col + tile[0];
      if (actualRow < 0 || actualRow >= boardSize || actualCol < 0 || actualCol >= boardSize || grid[actualRow][actualCol] === 1) {
        return false;
      }
    }
    return true;
  }
}
