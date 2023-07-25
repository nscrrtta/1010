from random import randint
from constants import *
import pygame


class Piece:

    def __init__(self, index: int):

        self.index = index
        self.shape = shapes[index]

        # Rotate shape random number of times
        for _ in range(randint(0,3)):
            self.shape = list(zip(*self.shape[::-1]))

        self.colour = colours[index]

        self.height = len(self.shape)
        self.width  = len(self.shape[0])

        self.x_pos: int
        self.y_pos = 510

        self.held = False


    def clicked(self, mouse_pos: tuple) -> bool:

        x, y = mouse_pos

        def create_pos_dict():
            
            self.pos_dict = {(0,0): (self.x_pos-x, self.y_pos-y)}

            for row in range(self.height):
                for col in range(self.width):

                    if self.shape[row][col] == 0: continue

                    dc = self.x_pos + col*sqr_size - x
                    dr = self.y_pos + row*sqr_size - y

                    self.pos_dict[(col,row)] = (dc,dr)

        for row in range(self.height):
            for col in range(self.width):

                if self.shape[row][col] == 0: continue

                left = self.x_pos + col*sqr_size
                top  = self.y_pos + row*sqr_size

                if left < x < left+sqr_size and top < y < top+sqr_size:
                    create_pos_dict()
                    self.held = True
                    return True

        return False


    def fits_on_board(self, board: list) -> bool:

        for row in range(11-self.height):
            for col in range(11-self.width):

                if board[row][col] > 0: continue
                if self.fits_here(row, col, board): return True

        return False
    

    def fits_here(self, row: int, col: int, board: list) -> bool:

        for r in range(self.height):
            for c in range(self.width):

                if self.shape[r][c] == 0: continue

                # Out of bounds
                if not (0 <= row+r <= 9 and 0 <= col+c <= 9): return False

                # Overlapping existing piece on board
                if board[row+r][col+c] > 0: return False

        return True


    def draw(self, screen):

        if self.held: x,y = pygame.mouse.get_pos()
        else: x,y = self.x_pos, self.y_pos

        for row in range(self.height):
            for col in range(self.width):

                if self.shape[row][col] == 0: continue

                if self.held: dc,dr = self.pos_dict[(col,row)]
                else: dc, dr = col*sqr_size, row*sqr_size

                rect = pygame.Rect(dc+x+1, dr+y+1, sqr_size-2, sqr_size-2)
                pygame.draw.rect(screen, self.colour, rect, border_radius=3)
