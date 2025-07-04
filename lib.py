import json
import pygame
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
                           surface.get_height()//2 - 80))
    
    # View high scores option
    scores_text = font.render("2. View High Scores", 1, (255, 255, 255))
    surface.blit(scores_text, (surface.get_width()//2 - scores_text.get_width()//2, 
                              surface.get_height()//2 - 20))

    # Credits option
    credits_text = font.render("3. Credits", 1, (255, 255, 255))
    surface.blit(credits_text, (surface.get_width()//2 - credits_text.get_width()//2, 
                              surface.get_height()//2 + 40))
    
    # Quit option
    quit_text = font.render("4. Quit", 1, (255, 255, 255))
    surface.blit(quit_text, (surface.get_width()//2 - quit_text.get_width()//2, 
                           surface.get_height()//2 + 100))
    
    # Small credits at bottom
    small_font = pygame.font.SysFont("comicsans", 20)
    bottom_text = small_font.render("© 2025 Peter Leukanič - MIT License", 1, (150, 150, 150))
    surface.blit(bottom_text, (surface.get_width()//2 - bottom_text.get_width()//2, 
                             surface.get_height() - 30))
    
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, False, False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return True, False, False  # Start game
                if event.key == pygame.K_2:
                    # Show high scores screen
                    should_continue = show_high_scores_screen(surface)
                    if not should_continue:
                        return False, False, False
                    # Redraw start screen
                    return show_start_screen(surface)
                if event.key == pygame.K_3:
                    # Show credits screen
                    should_continue = show_credits_screen(surface)
                    if not should_continue:
                        return False, False, False
                    # Redraw start screen
                    return show_start_screen(surface)
                if event.key == pygame.K_4:
                    return False, False, False  # Quit
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
        draw_text_middle(surface, "GAME OVER", 50, (255, 255, 255), -150)
        draw_text_middle(surface, f"Your Score: {score}", 40, (255, 255, 255), -100)
        
        # Draw menu options
        font = pygame.font.SysFont("comicsans", 40)
        
        # Play again option
        play_text = font.render("1. Play Again", 1, (255, 255, 255))
        surface.blit(play_text, (surface.get_width()//2 - play_text.get_width()//2, 
                                 surface.get_height()//2 - 50))
        
        # View high scores option
        scores_text = font.render("2. View High Scores", 1, (255, 255, 255))
        surface.blit(scores_text, (surface.get_width()//2 - scores_text.get_width()//2, 
                                   surface.get_height()//2))

        # Credits option
        credits_text = font.render("3. Credits", 1, (255, 255, 255))
        surface.blit(credits_text, (surface.get_width()//2 - credits_text.get_width()//2, 
                                    surface.get_height()//2 + 50))
        
        # Quit option
        quit_text = font.render("4. Quit", 1, (255, 255, 255))
        surface.blit(quit_text, (surface.get_width()//2 - quit_text.get_width()//2, 
                                 surface.get_height()//2 + 100))

        # Small credits at bottom
        small_font = pygame.font.SysFont("comicsans", 20)
        bottom_text = small_font.render("© 2025 Peter Leukanič - MIT License", 1, (150, 150, 150))
        surface.blit(bottom_text, (surface.get_width()//2 - bottom_text.get_width()//2, 
                                   surface.get_height() - 30))
        
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
                if event.key == pygame.K_3:
                    # Show credits screen
                    should_continue = show_credits_screen(surface)
                    if not should_continue:
                        return False
                    # Redraw game over screen after returning
                    continue
                if event.key == pygame.K_4:
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

def show_credits_screen(surface):
    """Display scrolling credits from bottom to top"""
    credits = [
        "CREDITS",
        "",
        "Game Development",
        "Peter Leukanič",
        "",
        "Programming",
        "Peter Leukanič",
        "",
        "Game Design",
        "Peter Leukanič",
        "",
        "Special Thanks",
        "Pygame Community",
        "",
        "License",
        "MIT License",
        "",
        "© 2025 All Rights Reserved"
    ]
    
    # Create a surface that will contain all credits text
    font = pygame.font.SysFont("comicsans", 30)
    line_height = 40
    total_height = len(credits) * line_height + surface.get_height()
    credits_surface = pygame.Surface((surface.get_width(), total_height))
    credits_surface.fill((0, 0, 0))
    
    # Render all credits text onto the credits surface
    for i, text in enumerate(credits):
        if text == "CREDITS":
            title_font = pygame.font.SysFont("comicsans", 50, bold=True)
            text_surface = title_font.render(text, True, (255, 255, 255))
        else:
            text_surface = font.render(text, True, (255, 255, 255))
        
        x_pos = credits_surface.get_width() // 2 - text_surface.get_width() // 2
        y_pos = i * line_height + surface.get_height()  # Start below visible area
        credits_surface.blit(text_surface, (x_pos, y_pos))
    
    scroll_speed = 1  # Pixels per frame
    y_offset = 0
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
                # Allow speed control with up/down arrows
                if event.key == pygame.K_UP:
                    scroll_speed = max(1, scroll_speed - 0.5)
                if event.key == pygame.K_DOWN:
                    scroll_speed = min(5, scroll_speed + 0.5)
                if event.key == pygame.K_SPACE:
                    scroll_speed = 0  # Pause
        
        # Scroll the credits
        y_offset += scroll_speed
        
        # Reset if we've scrolled all the way through
        if y_offset > total_height:
            y_offset = 0
        
        # Draw
        surface.fill((0, 0, 0))
        surface.blit(credits_surface, (0, -y_offset))
        
        # Show scroll speed indicator
        speed_font = pygame.font.SysFont("comicsans", 20)
        speed_text = speed_font.render(f"Scroll Speed: {scroll_speed:.1f}x (Up/Down to adjust, SPACE to pause)", 
                                     True, (150, 150, 150))
        surface.blit(speed_text, (20, surface.get_height() - 30))
        
        pygame.display.flip()
        clock.tick(60)
    
    return True
