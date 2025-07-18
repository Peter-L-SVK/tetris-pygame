#!/usr/bin/env python

import pygame
from tetromino import Tetromino
from lib import *

def main():
    # Initialize pygame
    pygame.init()
    
    # Game settings
    BLOCK_SIZE = 30
    GRID_WIDTH = 10
    GRID_HEIGHT = 20
    SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 6)
    SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT
    GAME_AREA = pygame.Rect(0, 0, BLOCK_SIZE * GRID_WIDTH, SCREEN_HEIGHT)
    
    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    
    clock = pygame.time.Clock()
    
    run = True
    while run:
        start_game, show_scores, show_credits = show_start_screen(screen)
        if not start_game and not show_scores and not show_credits:
            break
        
        if show_scores:
            continue  

        if show_credits:
            continue  

        grid = create_grid(GRID_WIDTH, GRID_HEIGHT)
        current_piece = Tetromino(grid_width=GRID_WIDTH)
        next_piece = Tetromino(grid_width=GRID_WIDTH)
        change_piece = False
        score = 0
        fall_time = 0
        fall_speed = 0.5  # seconds
        
        game_over = False
        while not game_over:
            fall_time += clock.get_rawtime() / 1000  # Convert to seconds
            clock.tick()
            
            # Piece falling
            if fall_time >= fall_speed:
                fall_time = 0
                current_piece.y += 1
                if not valid_space(current_piece, grid):
                    current_piece.y -= 1
                    change_piece = True
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        current_piece.x -= 1
                        if not valid_space(current_piece, grid):
                            current_piece.x += 1
                    
                    if event.key == pygame.K_RIGHT:
                        current_piece.x += 1
                        if not valid_space(current_piece, grid):
                            current_piece.x -= 1
                    
                    if event.key == pygame.K_DOWN:
                        current_piece.y += 1
                        if not valid_space(current_piece, grid):
                            current_piece.y -= 1
                    
                    if event.key == pygame.K_UP:
                        rotated = current_piece.rotate()
                        old_shape = current_piece.shape
                        current_piece.shape = rotated
                        if not valid_space(current_piece, grid):
                            current_piece.shape = old_shape
            
            # Add piece to the grid
            if change_piece:
                for y in range(len(current_piece.shape)):
                    for x in range(len(current_piece.shape[0])):
                        if current_piece.shape[y][x]:
                            grid[current_piece.y + y][current_piece.x + x] = current_piece.shape_idx + 1
                
                score = clear_rows(grid, score)
                current_piece = next_piece
                next_piece = Tetromino(grid_width=GRID_WIDTH)
                change_piece = False
                
                if check_lost(grid):
                    game_over = True
            
            screen.fill((0, 0, 0))
            draw_grid(screen, grid, BLOCK_SIZE, Tetromino.COLORS, (128, 128, 128))
            draw_tetromino(screen, current_piece, BLOCK_SIZE)
            draw_score(screen, score, GAME_AREA.width + 10, 20)
            draw_next_piece(screen, next_piece, GAME_AREA.width + 10, 100, BLOCK_SIZE)
            pygame.display.update()
        
        if not show_game_over_screen(screen, score):
            break

if __name__ == "__main__":
    main()
    pygame.quit()
