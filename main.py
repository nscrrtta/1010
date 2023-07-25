from constants import width, height
from game import Game
import pygame


pygame.init()
font = pygame.font.Font(None, 40)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('1010! by Nick Sciarretta')


game = Game()
game.new_game()


running = True
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_n:
                game.set_high_score()
                game.new_game()

        elif game.game_over: pass

        elif event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = pygame.mouse.get_pos()

            for piece in game.pieces:
                if piece.clicked(mouse_pos):
                    break

        elif event.type == pygame.MOUSEBUTTONUP:

            for piece in game.pieces:
                if piece.held:
                    game.add_piece_to_board(piece)
                    piece.held = False
                    break

    game.draw(screen, font)
    pygame.display.update()


game.set_high_score()
pygame.quit()