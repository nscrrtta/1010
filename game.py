from random import randint, shuffle
from piece import Piece
from constants import *
import numpy as np
import pygame


class Game:

    def new_game(self):

        self.board = [[0 for _ in range(10)] for _ in range(10)]
        self.new_pieces()

        self.game_over = False
        self.score = 0

        self.get_high_score()

    
    def new_pieces(self):

        # Ensure at least one new piece can fit on board
        while True:
            p1 = Piece(randint(1,9))
            if p1.fits_on_board(self.board): break

        self.pieces = [p1, Piece(randint(1,9)), Piece(randint(1,9))]
        shuffle(self.pieces)

        # Adjust x positions of pieces such that they're centered in screen
        p1, p2, p3 = self.pieces
        a = (width//sqr_size, p1.width, p2.width, p3.width)

        for i, b in enumerate([(1,-2,-1,0), (2,0,-2,0), (3,0,1,-2)]):
            self.pieces[i].x_pos = np.dot(a,b)*sqr_size//4


    def add_piece_to_board(self, piece: Piece):

        x,y = pygame.mouse.get_pos()
        a,b = piece.pos_dict[(0,0)]

        # Math to determine which square on board
        # top-left square of piece is located
        row = (y+b- top_edge+sqr_size//2)//sqr_size
        col = (x+a-left_edge+sqr_size//2)//sqr_size

        if not piece.fits_here(row, col, self.board): return

        for r in range(piece.height):
            for c in range(piece.width):

                if piece.shape[r][c] == 0: continue
                self.board[r+row][c+col] = piece.index
                self.score += 1

        self.clear_rows_cols()
        self.pieces.remove(piece)

        if len(self.pieces) == 0:
            self.new_pieces()
            return

        # Check if game over
        self.game_over = True

        for piece in self.pieces:
            if piece.fits_on_board(self.board):
                self.game_over = False
                return
        
        # Game over: set high score
        self.set_high_score()


    def clear_rows_cols(self):

        full_rows = []
        full_cols = []

        for i, row in enumerate(self.board):

            if row.count(0) == 0: full_rows.append(i)
            col = [r[i] for r in self.board]
            if col.count(0) == 0: full_cols.append(i)

        for row in full_rows:
            for i in range(10):
                self.board[row][i] = 0

        for col in full_cols:
            for i in range(10):
                self.board[i][col] = 0

        n = len(full_cols+full_rows)
        self.score += 5*n*(n+1)


    def get_high_score(self):

        try:
            with open('highscore.txt', 'r') as f:
                self.high_score = int(f.read())

        except FileNotFoundError: self.high_score = 0


    def set_high_score(self):

        if self.score > self.high_score:
            with open('highscore.txt', 'w') as f:
                f.write(str(self.score))


    def draw(self, screen, font):

        screen.fill((255,255,255))

        # Draw text
        for s, b, y in zip(
            ['Game Over!', f'High Score: {self.high_score}', f'Score: {self.score}'],
            [self.game_over, True, True],
            [30, 70, 110]
        ):
            if not b: continue
            text = font.render(s, True, (0,0,0))
            rect = text.get_rect()
            rect.center = (width//2, y)
            screen.blit(text, rect)

        # Draw board
        for row in range(10):
            for col in range(10):

                left = left_edge + col*sqr_size + 1
                top  = top_edge  + row*sqr_size + 1
                colour = colours[self.board[row][col]]

                rect = pygame.Rect(left, top, sqr_size-2, sqr_size-2)
                pygame.draw.rect(screen, colour, rect, border_radius=3)

        # Draw static pieces
        for piece in self.pieces:
            if not piece.held: piece.draw(screen)

        # Draw held piece
        for piece in self.pieces:
            if piece.held: piece.draw(screen)
