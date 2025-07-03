import pygame
import json
import os

def load_high_scores():
    """Load high scores from a JSON file"""
    if not os.path.exists('highscores.json'):
        return []
    
    try:
        with open('highscores.json', 'r') as f:
            return json.load(f)
    except:
        return []

def save_high_scores(scores):
    """Save high scores to a JSON file"""
    with open('highscores.json', 'w') as f:
        json.dump(scores, f)

def add_high_score(scores, name, score):
    """Add a new high score to the list and keep only top 10"""
    scores.append({'name': name, 'score': score})
    # Sort in descending order and keep only top 10
    scores.sort(key=lambda x: x['score'], reverse=True)
    return scores[:10]

def draw_high_scores(surface, scores, x_pos, y_pos):
    """Draw the high scores list"""
    font = pygame.font.SysFont('comicsans', 30)
    title = font.render("High Scores:", 1, (255, 255, 255))
    surface.blit(title, (x_pos, y_pos))
    
    for i, entry in enumerate(scores[:10]):  # Only show top 10
        score_text = f"{i+1}. {entry['name']}: {entry['score']}"
        label = font.render(score_text, 1, (255, 255, 255))
        surface.blit(label, (x_pos, y_pos + 40 + i * 30))

def get_player_name(surface):
    """Get player name input after game over"""
    name = ""
    input_active = True
    font = pygame.font.SysFont('comicsans', 40)
    
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
        
        surface.fill((0, 0, 0))
        prompt = font.render("Enter your name:", 1, (255, 255, 255))
        name_text = font.render(name, 1, (255, 255, 255))
        
        surface.blit(prompt, (surface.get_width()/2 - prompt.get_width()/2, 
                     surface.get_height()/2 - 50))
        surface.blit(name_text, (surface.get_width()/2 - name_text.get_width()/2, 
                     surface.get_height()/2 + 10))
        pygame.display.flip()
    
    return name if name.strip() else "Player"

def create_grid(width, height):
    return [[0 for _ in range(width)] for _ in range(height)]

def draw_grid(surface, grid, block_size, colors, gray):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            pygame.draw.rect(surface, gray, 
                           (x * block_size, y * block_size, block_size, block_size), 1)
            if grid[y][x]:
                pygame.draw.rect(surface, colors[grid[y][x] - 1],
                               (x * block_size, y * block_size, block_size, block_size))

def draw_tetromino(surface, tetromino, block_size, offset_x=0, offset_y=0, small=False):
    size = block_size // 2 if small else block_size
    for y in range(len(tetromino.shape)):
        for x in range(len(tetromino.shape[0])):
            if tetromino.shape[y][x]:
                pygame.draw.rect(surface, tetromino.color,
                               ((tetromino.x + x + offset_x) * (size if small else block_size), 
                                (tetromino.y + y + offset_y) * (size if small else block_size), 
                                size, size))

def valid_space(tetromino, grid):
    for y in range(len(tetromino.shape)):
        for x in range(len(tetromino.shape[0])):
            if tetromino.shape[y][x]:
                if (tetromino.y + y >= len(grid) or 
                    tetromino.x + x < 0 or 
                    tetromino.x + x >= len(grid[0]) or 
                    grid[tetromino.y + y][tetromino.x + x]):
                    return False
    return True

def check_lost(grid):
    return any(grid[0][x] for x in range(len(grid[0])))

def clear_rows(grid, score):
    completed_rows = []
    for y in range(len(grid)):
        if all(grid[y][x] for x in range(len(grid[0]))):
            completed_rows.append(y)
    
    for row in completed_rows:
        del grid[row]
        grid.insert(0, [0 for _ in range(len(grid[0]))])
        score += 10
    
    return score

def draw_score(surface, score, x_pos, y_pos, font_size=30, color=(255, 255, 255)):
    font = pygame.font.SysFont('comicsans', font_size)
    label = font.render(f"Score: {score}", 1, color)
    surface.blit(label, (x_pos, y_pos))

def draw_next_piece(surface, piece, x_pos, y_pos, block_size):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render("Next:", 1, (255, 255, 255))
    surface.blit(label, (x_pos, y_pos))
    
    # Draw the next piece preview (smaller size)
    for y in range(len(piece.shape)):
        for x in range(len(piece.shape[0])):
            if piece.shape[y][x]:
                pygame.draw.rect(surface, piece.color,
                               (x_pos + 20 + x * block_size//2, 
                                y_pos + 50 + y * block_size//2, 
                                block_size//2, block_size//2))

def draw_text_middle(surface, text, size, color, y_offset=0):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)
    
    surface.blit(label, (surface.get_width()/2 - label.get_width()/2, 
                       surface.get_height()/2 - label.get_height()/2 + y_offset))

def show_start_screen(surface):
    surface.fill((0, 0, 0))
    
    # Draw title
    draw_text_middle(surface, "TETRIS", 60, (255, 255, 255), -180)
    
    # Draw menu options
    font = pygame.font.SysFont("comicsans", 40)
    
    # Play game option
    play_text = font.render("1. Play Game", 1, (255, 255, 255))
    surface.blit(play_text, (surface.get_width()//2 - play_text.get_width()//2, 
                           surface.get_height()//2 - 50))
    
    # View high scores option
    scores_text = font.render("2. View High Scores", 1, (255, 255, 255))
    surface.blit(scores_text, (surface.get_width()//2 - scores_text.get_width()//2, 
                              surface.get_height()//2 + 20))

    # Quit option
    quit_text = font.render("3. Quit", 1, (255, 255, 255))
    surface.blit(quit_text, (surface.get_width()//2 - quit_text.get_width()//2, 
                             surface.get_height()//2 + 100))
    
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return True, False
                if event.key == pygame.K_2:
                    # Show high scores screen
                    should_continue = show_high_scores_screen(surface)
                    if not should_continue:
                        return False, False
                    # Redraw start screen after returning from high scores
                    return show_start_screen(surface)
                if event.key == pygame.K_3:
                    return False, False
    return True, False, False

def show_game_over_screen(surface, score):
    highscores = load_high_scores()
    
    # Get player name
    name = get_player_name(surface)
    if name is None:  # User closed the window
        return False
    
    # Add to high scores
    highscores = add_high_score(highscores, name, score)
    save_high_scores(highscores)
    
    while True:
        surface.fill((0, 0, 0))
        draw_text_middle(surface, "GAME OVER", 50, (255, 255, 255), -120)
        draw_text_middle(surface, f"Your Score: {score}", 40, (255, 255, 255), -60)
        
        # Draw menu options
        font = pygame.font.SysFont("comicsans", 40)
        
        # Play again option
        play_text = font.render("1. Play Again", 1, (255, 255, 255))
        surface.blit(play_text, (surface.get_width()//2 - play_text.get_width()//2, 
                               surface.get_height()//2))
        
        # View high scores option
        scores_text = font.render("2. View High Scores", 1, (255, 255, 255))
        surface.blit(scores_text, (surface.get_width()//2 - scores_text.get_width()//2, 
                                 surface.get_height()//2 + 50))
        
        # Quit option
        quit_text = font.render("3. Quit", 1, (255, 255, 255))
        surface.blit(quit_text, (surface.get_width()//2 - quit_text.get_width()//2, 
                               surface.get_height()//2 + 100))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return True
                if event.key == pygame.K_2:
                    # Show high scores screen
                    should_continue = show_high_scores_screen(surface)
                    if not should_continue:
                        return False
                    # Redraw game over screen after returning
                    continue
                if event.key == pygame.K_3:
                    return False

def show_high_scores_screen(surface):
    """Display a dedicated screen for high scores"""
    highscores = load_high_scores()
    
    while True:
        surface.fill((0, 0, 0))
        
        # Draw title
        draw_text_middle(surface, "HIGH SCORES", 60, (255, 255, 255), -180)
        
        # Draw high scores
        if highscores:
            draw_high_scores(surface, highscores, 
                           surface.get_width()//2 - 100, 
                           surface.get_height()//2 - 100)
        else:
            draw_text_middle(surface, "No scores yet!", 40, (255, 255, 255), 0)
        
        # Draw return instruction
        draw_text_middle(surface, "Press ESC to return", 30, (255, 255, 255), 200)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
