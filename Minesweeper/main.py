from game import Game
from board import Board
size = (9, 9)
prob = 0.1
board = Board(size, prob)
screenSize = (500,500)
game = Game(board, screenSize)
game.run()
