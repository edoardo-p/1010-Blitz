## What we wanted
1010 game with AI player

## What we achieved
Were unable to implement AI solver in time, but had planned to try all possible next moves and play highest scoring following a set of criteria
Wrote 1010 game using p5.js – great for UI work
Had very close functionality to original 1010
We added a timer to create a “blitz” mode

## Functionality
 - 10 x 10 grid, score board and timer above, next pieces below
 - Can click on a piece from below and place it onto the board
 - Game checks whether move is valid (not off screen/ over other blocks) before placing it
 - Pressing spacebar while holding blocks puts it back in the next pieces box
 - After placement game checks for any completed lines and removes them 
 - Also awards score based on size of piece and lines cleared
 - Scoring points increases remaining time
 - Game is drawn using coordinates relative to window but game logic is performed in 10 x 10 array with unit coordinates ((0,0), (1,6), (9,9))
 - Pieces are defined as series of relative unit coordinates to their grips
 - Game converts user input coordinates into unit game space to apply logic and then converts results of logic back into window coordinates to draw

## Features:
 - Time out – Timer starts at 30s, scoring points increases time remaining, 1 point =  1sec, max time cap 60s if timer hits 0 you lose
 - No more moves, if placing a piece leaves you with no possible positions for any of your remaining pieces you lose
 - Losing freezes the game and prints your final score at the top of the board

## Bugs
 - Pieces at the bottom won’t snap back to original location, but in the next available space
 - If the losing move happens to clear lines, the score will increase accordingly but the grid won’t update properly