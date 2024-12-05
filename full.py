import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Set the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)  # Gray color for grid lines
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Set the size of each cell in the grid
CELL_SIZE = 38  # smaller, smaller cell size, vice versa

# Default board sizes
black_board_size = 9
gray_board_size = black_board_size + 1

# Initialize grid state
grid_state = [[0] * gray_board_size for _ in range(gray_board_size)]  # Initialize all cells as not clicked

# Define players
PLAYER_1 = 1
PLAYER_2 = 2

# Initialize player turn
current_player = PLAYER_1

# Load the background image
background_image = pygame.image.load('bg3.jpeg')
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

def draw_board(screen, size, grid_color, clicked_cells):
    # Calculate the starting position to center the board
    start_x = (WINDOW_WIDTH - CELL_SIZE * size) // 2
    start_y = (WINDOW_HEIGHT - CELL_SIZE * size) // 2

    for row in range(size):
        for col in range(size):
            cell_rect = pygame.Rect(start_x + col * CELL_SIZE, start_y + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            state = grid_state[row][col]
            if (row, col) in clicked_cells:  # Check if cell is clicked
                if state == PLAYER_1:
                    color = BLUE
                elif state == PLAYER_2:
                    color = RED
                elif state == 3:
                    color = (0, 0, 100)  # Dark blue
                elif state == 4:
                    color = (128, 0, 0)  # Dark red
                elif state == 5:
                    color = (169, 169, 169)  # Dark gray
                pygame.draw.circle(screen, color, (cell_rect.centerx, cell_rect.centery), CELL_SIZE // 2.5)  # Draw a circle at the center
            else:
                pygame.draw.rect(screen, grid_color, cell_rect, 1)

def draw_scores(screen, player1_score, player2_score, gamemode):
    font = pygame.font.SysFont(None, 50)
    text1 = font.render(f"Player 1: {player1_score}", True, BLUE)
    if gamemode == "human":
        text2 = font.render(f"Player 2: {player2_score}", True, RED)
    else:
        text2 = font.render(f"AI Agent: {player2_score}", True, RED)
    
    # Position the text at the top of the screen
    screen.blit(text1, (50, 20))
    screen.blit(text2, (WINDOW_WIDTH - text2.get_width() - 50, 20))

def end_screen(winner):
    
    screen = pygame.display.set_mode(WINDOW_SIZE)
    screen.blit(background_image, (0, 0))
    pygame.display.set_caption("encircle - Game Over")
    running = True
    font = pygame.font.SysFont(None, 80)
    if winner == 1:
        text = font.render("Blue Wins!", True, BLUE)
    elif winner == 2:
        text = font.render("Red Wins!", True, RED)
    else:
        text = font.render("It's a Draw!", True, BLACK)
        
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    
    instruction_font = pygame.font.SysFont(None, 40)
    instruction_text = instruction_font.render("Click anywhere to go to main menu", True, BLACK)
    instruction_rect = instruction_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                main()  # Go back to main menu or exit

        
        screen.blit(text, text_rect)
        screen.blit(instruction_text, instruction_rect)
        pygame.display.flip()

def draw_menu(screen, play_human_rect, play_ai_rect, input_rect, input_text):
    # Draw the background image
    screen.blit(background_image, (0, 0))
    
    # Render the title
    title_font = pygame.font.SysFont(None, 70)
    title_text = title_font.render("Encircling Game", True, BLACK)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 100))
    screen.blit(title_text, title_rect)
    
    # Render the buttons
    font = pygame.font.SysFont(None, 50)
    text1 = font.render("Play Against Human", True, BLACK)
    text2 = font.render("Play Against AI", True, BLACK)
    
    # Center the text within the rectangles
    text1_rect = text1.get_rect(center=play_human_rect.center)
    text2_rect = text2.get_rect(center=play_ai_rect.center)
    
    screen.blit(text1, text1_rect)
    screen.blit(text2, text2_rect)
    
    pygame.draw.rect(screen, BLACK, play_human_rect, 2)
    pygame.draw.rect(screen, BLACK, play_ai_rect, 2)
    
    # Calculate positions for grid size label and input box
    label_rect = pygame.Rect(WINDOW_WIDTH // 2 - 200, input_rect.y, 100, input_rect.height)
    input_label = font.render("Grid Size:", True, BLACK)
    screen.blit(input_label, label_rect)
    
    input_text_surface = font.render(input_text, True, BLACK)
    input_text_rect = input_text_surface.get_rect(midleft=(input_rect.x + 10, input_rect.centery))  # Adjusted position
    screen.blit(input_text_surface, input_text_rect)
    
    pygame.draw.rect(screen, BLACK, input_rect, 2)
    
    pygame.display.flip()


def draw_difficulty_menu(screen, difficulty_rects, back_rect):
    # Draw the background image
    screen.blit(background_image, (0, 0))
    font = pygame.font.SysFont(None, 50)
    text = font.render("Select Difficulty", True, BLACK)
    screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, 50))
    for rect, difficulty in difficulty_rects:
        pygame.draw.rect(screen, BLACK, rect, 2)
        text = font.render(difficulty, True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
    pygame.draw.rect(screen, BLACK, back_rect, 2)
    back_text = font.render("Back", True, BLACK)
    back_text_rect = back_text.get_rect(center=back_rect.center)
    screen.blit(back_text, back_text_rect)
    pygame.display.flip()

def main_menu():
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("encircle - Main Menu")
    running = True
    play_human_rect = pygame.Rect(WINDOW_WIDTH // 2 - 200, 300, 400, 100)
    play_ai_rect = pygame.Rect(WINDOW_WIDTH // 2 - 200, 450, 400, 100)
    input_rect = pygame.Rect(WINDOW_WIDTH // 2 - 20, 600, 140, 50)  # Adjusted x-coordinate
    input_text = "10"  # Default grid size (9 for black board, 10 for gray board)
    user_text = ""
    active = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_human_rect.collidepoint(event.pos):
                    return "human", int(input_text)
                elif play_ai_rect.collidepoint(event.pos):
                    return "ai", int(input_text)
                elif input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        input_text = user_text
                        user_text = ""
                        active = False  # Deactivate after pressing Enter
                    elif event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode

        screen.fill(WHITE)
        draw_menu(screen, play_human_rect, play_ai_rect, input_rect, user_text if active else input_text)
    
    return input_text

def difficulty_menu():
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("encircle - Difficulty Selection")
    running = True
    font = pygame.font.SysFont(None, 50)
    difficulties = ["Easy", "Medium", "Hard"]
    difficulty_rects = []
    for i, difficulty in enumerate(difficulties):
        rect = pygame.Rect(200, 200 + 150 * i, 400, 100)
        difficulty_rects.append((rect, difficulty))
    back_rect = pygame.Rect(50, WINDOW_HEIGHT - 70, 100, 50)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_rect.collidepoint(mouse_pos):
                    return "back"
                for rect, difficulty in difficulty_rects:
                    if rect.collidepoint(mouse_pos):
                        return difficulty
        draw_difficulty_menu(screen, difficulty_rects, back_rect)

def main():
    while True:
        mode, size = main_menu()
        global gray_board_size, black_board_size, grid_state
        black_board_size = size
        gray_board_size = black_board_size + 1
        grid_state = [[0] * gray_board_size for _ in range(gray_board_size)]
        
        if mode == "human":
            result = play_human_vs_human()
            if result == "back":
                continue  # Go back to main menu
        elif mode == "ai":
            while True:
                difficulty = difficulty_menu()
                if difficulty == "back":
                    break  # Go back to main menu
                result = play_human_vs_ai(difficulty)
                if result == "back":
                    continue  # Go back to difficulty menu

def reset_game():
    global grid_state, current_player
    grid_state = [[0] * gray_board_size for _ in range(gray_board_size)]  # Reset the grid state
    current_player = PLAYER_1  # Reset the current player
    

def play_human_vs_human():
    reset_game()  # Reset the game state
    global current_player  # Declare current_player as a global variable
    player1_score = 0
    player2_score = 0
    gamemode = "human"
    # Create the Pygame window
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("encircle")

    # Main game loop
    running = True
    back_rect = pygame.Rect(50, WINDOW_HEIGHT - 70, 100, 50)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button clicked
                    # Convert mouse position to grid coordinates for the gray board
                    mouse_x, mouse_y = event.pos
                    gray_board_start_x = (WINDOW_WIDTH - CELL_SIZE * gray_board_size) // 2
                    gray_board_start_y = (WINDOW_HEIGHT - CELL_SIZE * gray_board_size) // 2
                    grid_row = (mouse_y - gray_board_start_y) // CELL_SIZE
                    grid_col = (mouse_x - gray_board_start_x) // CELL_SIZE
                    if 0 <= grid_row < gray_board_size and 0 <= grid_col < gray_board_size and grid_state[grid_row][grid_col] == 0:  # Check if within bounds and cell is not clicked
                        grid_state[grid_row][grid_col] = current_player
                        
                        # Check captures for the current move and its neighbors
                        check_for_captures(grid_row, grid_col, current_player)
                        
                        # Switch player turn
                        current_player = PLAYER_1 if current_player == PLAYER_2 else PLAYER_2
                        
                        # Check if all spots are filled
                        all_spots_filled = all(all(cell != 0 for cell in row) for row in grid_state)

                        if all_spots_filled:
                            running = False  # Exit the game loop

                        player1_score = sum(row.count(4) for row in grid_state)
                        player2_score = sum(row.count(3) for row in grid_state)
                        # print("Player 1 score: ", player1_score, " Player 2 score: ", player2_score)

            # Handle back button click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if back_rect.collidepoint(mouse_pos):
                    return "back"

        # Fill the background with white
        screen.fill(WHITE)

        # Draw the 6x6 board in black
        draw_board(screen, black_board_size, BLACK, [])

        # Draw the 7x7 board in gray
        draw_board(screen, gray_board_size, WHITE, [(row, col) for row in range(gray_board_size) for col in range(gray_board_size) if grid_state[row][col]])

        draw_scores(screen, player1_score, player2_score, gamemode)

        # Draw the back button
        pygame.draw.rect(screen, BLACK, back_rect, 2)
        font = pygame.font.SysFont(None, 50)
        back_text = font.render("Back", True, BLACK)
        back_text_rect = back_text.get_rect(center=back_rect.center)
        screen.blit(back_text, back_text_rect)

        # Update the display
        pygame.display.flip()

    # Count captured pieces for each player
    player1_score = sum(row.count(4) for row in grid_state)
    player2_score = sum(row.count(3) for row in grid_state)

    # Determine the winner
    if player1_score > player2_score:
        winner = 1
    elif player2_score > player1_score:
        winner = 2
    else:
        winner = None  # It's a draw

    # Show the end screen
    end_screen(winner)

def play_human_vs_ai(difficulty):
    reset_game()  # Reset the game state
    global current_player  # Declare current_player as a global variable
    player1_score = 0
    player2_score = 0
    gamemode = "ai"
    # Create the Pygame window
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("encircle")
    back_rect = pygame.Rect(50, WINDOW_HEIGHT - 70, 100, 50)
    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button clicked
                    # Convert mouse position to grid coordinates for the gray board
                    mouse_x, mouse_y = event.pos
                    gray_board_start_x = (WINDOW_WIDTH - CELL_SIZE * gray_board_size) // 2
                    gray_board_start_y = (WINDOW_HEIGHT - CELL_SIZE * gray_board_size) // 2
                    grid_row = (mouse_y - gray_board_start_y) // CELL_SIZE
                    grid_col = (mouse_x - gray_board_start_x) // CELL_SIZE
                    if 0 <= grid_row < gray_board_size and 0 <= grid_col < gray_board_size and grid_state[grid_row][grid_col] == 0:  # Check if within bounds and cell is not clicked
                        grid_state[grid_row][grid_col] = current_player
                        
                        # Check captures for the current move and its neighbors
                        check_for_captures(grid_row, grid_col, current_player)
                        
                        # Switch player turn
                        current_player = PLAYER_1 if current_player == PLAYER_2 else PLAYER_2
                        
                        # Check if all spots are filled
                        all_spots_filled = all(all(cell != 0 for cell in row) for row in grid_state)

                        if all_spots_filled:
                            running = False  # Exit the game loop

                        player1_score = sum(row.count(4) for row in grid_state)
                        player2_score = sum(row.count(3) for row in grid_state)
                        # print("Player 1 score: ", player1_score, " AI Agent score: ", player2_score)
                    
                    # Handle back button click
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if back_rect.collidepoint(mouse_pos):
                        return "back"

            if current_player == PLAYER_2:
                # difficulty = "Hard"
                ai_move = make_ai_move(difficulty)
                if ai_move:
                    # print(ai_move)
                    grid_state[ai_move[0]][ai_move[1]] = current_player
                    check_for_captures(ai_move[0], ai_move[1], current_player)
                    current_player = PLAYER_1

                    # Check if all spots are filled
                    all_spots_filled = all(all(cell != 0 for cell in row) for row in grid_state)

                    if all_spots_filled:
                        running = False  # Exit the game loop
                    player1_score = sum(row.count(4) for row in grid_state)
                    player2_score = sum(row.count(3) for row in grid_state)
                    # print("Player 1 score: ", player1_score, " AI Agent score: ", player2_score)
                else:
                    current_player = PLAYER_1

        # Fill the background with white
        screen.fill(WHITE)

        # Draw the 6x6 board in black
        draw_board(screen, black_board_size, BLACK, [])

        # Draw the 7x7 board in gray
        draw_board(screen, gray_board_size, WHITE, [(row, col) for row in range(gray_board_size) for col in range(gray_board_size) if grid_state[row][col]])
        
        draw_scores(screen, player1_score, player2_score, gamemode)

        # Draw the back button
        pygame.draw.rect(screen, BLACK, back_rect, 2)
        font = pygame.font.SysFont(None, 50)
        back_text = font.render("Back", True, BLACK)
        back_text_rect = back_text.get_rect(center=back_rect.center)
        screen.blit(back_text, back_text_rect)

        # Update the display
        pygame.display.flip()

    # Count captured pieces for each player
    player1_score = sum(row.count(4) for row in grid_state)
    player2_score = sum(row.count(3) for row in grid_state)

    # Determine the winner
    if player1_score > player2_score:
        winner = 1
    elif player2_score > player1_score:
        winner = 2
    else:
        winner = None  # It's a draw

    # Show the end screen
    end_screen(winner)


def make_ai_move(difficulty):
    player = current_player
    opponent = PLAYER_1 if player == PLAYER_2 else PLAYER_2

    random_move = False
    place_near_opponent = False
    prevent_capture = False
    capture_opponent = False
    the_double_attack = False
    highest_points = False
    predict_points = False

    if difficulty == "Easy":
        random_move = True
        prevent_capture = True
        capture_opponent = True
    elif difficulty == "Medium":
        place_near_opponent = True
        highest_points = True
        the_double_attack = True
    elif difficulty == "Hard":
        place_near_opponent = True
        the_double_attack = True
        highest_points = True
        predict_points = True

    # Variables to store moves and their priorities
    random_move_prio = 0
    random_move_placed = None

    # AI place near opponent pieces
    place_near_opponent_prio = 0
    place_near_opponent_placed = None

    #prevent only one capture
    prevent_capture_prio = 0
    prevent_capture_placed = None

    #go for single capture
    capture_opponent_prio = 0
    capture_opponent_placed = None

    #to trap both single enemy piece
    the_double_attack_prio = 0
    the_double_attack_placed = None

    #select highest point to defend or capture
    highest_points_prio = 0
    highest_points_placed = None

    #predict only 1 next capture or defend
    predict_points_prio = 0
    predict_points_placed = None

    # Define directions
    directions_8 = [
        (-1, 0),  # up
        (-1, 1),  # up + right
        (0, 1),   # right
        (1, 1),   # down + right
        (1, 0),   # down
        (1, -1),  # down + left
        (0, -1),  # left
        (-1, -1)  # up + left
    ]

    directions_4 = [
        (-1, 0),  # up
        (1, 0),   # down
        (0, -1),  # left
        (0, 1)    # right
    ]

    if random_move:
        valid_moves = [(row, col) for row in range(gray_board_size) for col in range(gray_board_size) if grid_state[row][col] == 0]
        if valid_moves:
            random_move_prio = 1
            random_move_placed = random.choice(valid_moves)

    if place_near_opponent:
        valid_moves = []
        for row in range(gray_board_size):
            for col in range(gray_board_size):
                if grid_state[row][col] == opponent:
                    for dr, dc in directions_8:
                        new_row, new_col = row + dr, col + dc
                        if 0 <= new_row < gray_board_size and 0 <= new_col < gray_board_size and grid_state[new_row][new_col] == 0:
                            valid_moves.append((new_row, new_col))
        if valid_moves:
            place_near_opponent_prio = 2
            place_near_opponent_placed = random.choice(valid_moves)

    if prevent_capture:
        valid_moves = []
        for row in range(gray_board_size):
            for col in range(gray_board_size):
                if grid_state[row][col] == player:
                    count_opponent = 0
                    empty_pos = None
                    for dr, dc in directions_4:
                        new_row, new_col = row + dr, col + dc
                        if 0 <= new_row < gray_board_size and 0 <= new_col < gray_board_size:
                            if grid_state[new_row][new_col] == opponent:
                                count_opponent += 1
                            elif grid_state[new_row][new_col] == 0:
                                empty_pos = (new_row, new_col)
                    if count_opponent == 3 and empty_pos:
                        valid_moves.append(empty_pos)
        if valid_moves:
            prevent_capture_prio = 3
            prevent_capture_placed = random.choice(valid_moves)

    if capture_opponent:
        valid_moves = []
        for row in range(gray_board_size):
            for col in range(gray_board_size):
                if grid_state[row][col] == opponent:
                    count_self = 0
                    empty_pos = None
                    for dr, dc in directions_4:
                        new_row, new_col = row + dr, col + dc
                        if 0 <= new_row < gray_board_size and 0 <= new_col < gray_board_size:
                            if grid_state[new_row][new_col] == player:
                                count_self += 1
                            elif grid_state[new_row][new_col] == 0:
                                empty_pos = (new_row, new_col)
                    if count_self == 3 and empty_pos:
                        valid_moves.append(empty_pos)
        if valid_moves:
            capture_opponent_prio = 4
            capture_opponent_placed = random.choice(valid_moves)

    if the_double_attack:
        valid_moves = []
        for row in range(gray_board_size):
            for col in range(gray_board_size):
                if grid_state[row][col] == player:
                    
                    check_legal = False
                    for dr, dc in directions_8:
                        new_row, new_col = row + dr, col + dc
                        if 0 <= new_row < gray_board_size and 0 <= new_col < gray_board_size:
                            check_legal = True
                        else:
                            check_legal = False
                            break

                    if check_legal:        
                        if (
                            grid_state[row][col] == player and grid_state[row-1][col+1] == player and grid_state[row+1][col-1] == player and 
                            grid_state[row][col+1] == opponent and grid_state[row+1][col] == opponent and 
                            grid_state[row+1][col+1] == 0
                        ):

                            valid_moves.append((row+1, col+1))
                        elif (
                            grid_state[row][col] == player and grid_state[row-1][col+1] == player and grid_state[row+1][col-1] == player and 
                            grid_state[row-1][col] == opponent and grid_state[row][col-1] == opponent and 
                            grid_state[row-1][col-1] == 0
                        ):

                            valid_moves.append((row-1, col-1))
                        elif (
                            grid_state[row][col] == player and grid_state[row-1][col-1] == player and grid_state[row+1][col+1] == player and 
                            grid_state[row][col-1] == opponent and grid_state[row+1][col] == opponent and 
                            grid_state[row+1][col-1] == 0
                        ):

                            valid_moves.append((row+1, col-1))
                        elif (
                            grid_state[row][col] == player and grid_state[row-1][col-1] == player and grid_state[row+1][col+1] == player and 
                            grid_state[row-1][col] == opponent and grid_state[row][col+1] == opponent and 
                            grid_state[row-1][col+1] == 0
                        ):

                            valid_moves.append((row-1, col+1))
                        else:
                            pass
        if valid_moves:
            
            the_double_attack_prio = 5
            the_double_attack_placed = random.choice(valid_moves)

    def copy_board_state(board):
        return [row[:] for row in board]

    def restore_board_state(board, state):
        for i in range(len(board)):
            board[i] = state[i][:]

    def calculate_board_score(row, col, cur_player, predict):
        # Take a snapshot of the current board state
        if predict == False:
            original_state = copy_board_state(grid_state)
            grid_state[row][col] = cur_player
            score = 0
            # Calculate the score before making the move
            prev_score = sum(r.count(4) for r in grid_state) if cur_player == PLAYER_1 else sum(r.count(3) for r in grid_state)
            # Check captures
            check_for_captures(row, col, cur_player)
            # Calculate the score after making the move
            new_score = sum(r.count(4) for r in grid_state) if cur_player == PLAYER_1 else sum(r.count(3) for r in grid_state)
            # Calculate the score difference
            score = new_score - prev_score

            restore_board_state(grid_state, original_state)
            return score
        elif predict == True:
            original_state = copy_board_state(grid_state)
            score = 0
            temp_best_score = 0
            for dr, dc in directions_8:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < gray_board_size and 0 <= new_col < gray_board_size and grid_state[new_row][new_col] == 0:
                    grid_state[row][col] = cur_player
                    prev_score = sum(r.count(4) for r in grid_state) if cur_player == PLAYER_1 else sum(r.count(3) for r in grid_state)
                    check_for_captures(row, col, cur_player)
                    grid_state[new_row][new_col] = cur_player

                    # Check captures
                    check_for_captures(row, col, cur_player)
                    # Calculate the score after making the move
                    new_score = sum(r.count(4) for r in grid_state) if cur_player == PLAYER_1 else sum(r.count(3) for r in grid_state)
                    # Calculate the score difference
                    score = new_score - prev_score
                    
                    if score > temp_best_score:
                        temp_best_score = score

                    restore_board_state(grid_state, original_state)

            return temp_best_score

        

    def find_empty_cells_near_states(grid_state, target_states):
        empty_cells = []
        
        for row in range(len(grid_state)):
            for col in range(len(grid_state[0])):
                if grid_state[row][col] == 0:  # If cell is empty
                    for dr, dc in directions_8:
                        new_row, new_col = row + dr, col + dc
                        if 0 <= new_row < len(grid_state) and 0 <= new_col < len(grid_state[0]):
                            if grid_state[new_row][new_col] in target_states:
                                empty_cells.append((row, col))
                                break  # Move to the next empty cell
        return empty_cells

    if highest_points:
        best_score_capture = -float('inf')
        best_score_defend = -float('inf')
        best_score_capture_placed = None
        best_score_defend_placed = None
        predict = False
        
        empty_cells_near_states = find_empty_cells_near_states(grid_state, [player,opponent])
        for row, col in empty_cells_near_states:
            # Calculate scores for capturing and defending
            score_capture = calculate_board_score(row, col, player, predict)
            score_defend = calculate_board_score(row, col, opponent, predict)
            
            if score_capture > best_score_capture:
                best_score_capture = score_capture
                best_score_capture_placed = (row, col)
            
            if score_defend > best_score_defend:
                best_score_defend = score_defend
                best_score_defend_placed = (row, col)
        
        if best_score_capture > best_score_defend:
            highest_points_placed = best_score_capture_placed
        else:
            highest_points_placed = best_score_defend_placed

        if highest_points_placed and max(best_score_defend, best_score_capture):
            highest_points_prio = 6

    if predict_points:

        best_predict_capture = 0
        best_predict_defend = 0
        best_predict_capture_placed = None
        best_predict_defend_placed = None
        predict = True

        empty_cells_near_states_player = find_empty_cells_near_states(grid_state, [player])
        empty_cells_near_states_opponent = find_empty_cells_near_states(grid_state, [opponent])
        # print(empty_cells_near_states_player)
        # print(empty_cells_near_states_opponent)
        for row, col in empty_cells_near_states_player:
            # Calculate scores for capturing and defending
            predict_capture = calculate_board_score(row, col, player, predict)
            
            
            if predict_capture > best_predict_capture:
                best_predict_capture = predict_capture
                best_predict_capture_placed = (row, col)
            
        for row, col in empty_cells_near_states_opponent:
            predict_defend = calculate_board_score(row, col, opponent, predict)

            if predict_defend > best_predict_defend:
                best_predict_defend = score_defend
                best_predict_defend_placed = (row, col)

        if best_predict_capture > best_predict_defend:
            predict_points_placed = best_predict_capture_placed
            
        else:
            predict_points_placed = best_predict_defend_placed

        if predict_points_placed and max(best_predict_defend, best_predict_capture):
            predict_points_prio = 6


    if highest_points and predict_points:
        best_current = max(best_score_defend, best_score_capture)
        best_predict = max(best_predict_defend, best_predict_capture)
        # print("best def cap: ", max(best_score_defend, best_score_capture))
        # print("best predict: ", best_predict_capture)
        if best_current > best_predict:
            # print("highest current")
            highest_points_prio = 7
        elif best_predict == 1 and best_predict > best_current:
            the_double_attack_prio = 7
        elif best_predict > best_current:
            # print("highest predict")
            predict_points_prio = 7
        elif best_current > 0 and best_predict > 0 and best_current == best_predict:
            # print("double prio")
            highest_points_prio = 7
        elif best_current == 0 and best_predict == 0:
            place_near_opponent_prio = 7


    # Compare priorities and return the move with the highest priority
    moves_with_priority = [
        (random_move_prio, random_move_placed),
        (place_near_opponent_prio, place_near_opponent_placed),
        (prevent_capture_prio, prevent_capture_placed),
        (capture_opponent_prio, capture_opponent_placed),
        (the_double_attack_prio, the_double_attack_placed),
        (highest_points_prio, highest_points_placed),
        (predict_points_prio, predict_points_placed)
    ]
    # Sort the moves based on priority
    moves_with_priority.sort(reverse=True, key=lambda x: x[0])

    # Return the move with the highest priority
    for prio, move in moves_with_priority:
        if move is not None:
            # print(prio)
            return move

    # If no valid moves are found, return None
    return None



def check_for_captures(row, col, cur_player):
    player = cur_player
    # Initialize visited array
    visited = [[False] * gray_board_size for _ in range(gray_board_size)]

    # Define directions
    directions = [
        (-1, 0),  # up
        (-1, 1),  # up + right
        (0, 1),   # right
        (1, 1),   # down + right
        (1, 0),   # down
        (1, -1),  # down + left
        (0, -1),  # left
        (-1, -1)  # up + left
    ]

    # Perform DFS to find connected cells of the same player
    connected_cells = []

    def dfs(row, col):
        visited[row][col] = True
        connected_cells.append((row, col))
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < gray_board_size and 0 <= new_col < gray_board_size and not visited[new_row][new_col] and grid_state[new_row][new_col] == player:
                dfs(new_row, new_col)

    dfs(row, col)
    #print(connected_cells)
    counter = 0

    # Define capture directions
    capture_directions = [
        (-1, 0),  # up
        (0, 1),   # right
        (1, 0),   # down
        (0, -1),  # left
    ]

    captured_cells = []

    for row in range(gray_board_size):
        for col in range(gray_board_size):
            check_up_more = True
            check_right_more = True
            check_down_more = True
            check_left_more = True
            check_success = True
            if grid_state[row][col] in (0,1,2,3,4,5):  
                ori_row, ori_col = row, col
                while check_up_more:
                    row,col = row-1,col
                    if 0 <= row < gray_board_size and 0 <= col < gray_board_size and (row,col) not in connected_cells:
                        check_up_more = True
                    elif 0 <= row < gray_board_size and 0 <= col < gray_board_size and (row,col) in connected_cells:
                        check_up_more = False
                        row, col = ori_row, ori_col
                    else:
                        check_up_more = False
                        check_right_more = False
                        check_down_more = False
                        check_left_more = False
                        check_success = False
                        row, col = ori_row, ori_col
                while check_right_more:
                    row,col = row,col+1
                    if 0 <= row < gray_board_size and 0 <= col < gray_board_size and (row,col) not in connected_cells:
                        check_right_more = True
                    elif 0 <= row < gray_board_size and 0 <= col < gray_board_size and (row,col) in connected_cells:
                        check_right_more = False
                        row, col = ori_row, ori_col
                    else:
                        check_right_more = False
                        check_down_more = False
                        check_left_more = False
                        check_success = False
                        row, col = ori_row, ori_col
                while check_down_more:
                    row,col = row+1,col
                    if 0 <= row < gray_board_size and 0 <= col < gray_board_size and (row,col) not in connected_cells:
                        check_down_more = True
                    elif 0 <= row < gray_board_size and 0 <= col < gray_board_size and (row,col) in connected_cells:
                        check_down_more = False
                        row, col = ori_row, ori_col
                    else:
                        check_down_more = False
                        check_left_more = False
                        check_success = False
                        row, col = ori_row, ori_col
                while check_left_more:
                    row,col = row,col-1
                    if 0 <= row < gray_board_size and 0 <= col < gray_board_size and (row,col) not in connected_cells:
                        check_left_more = True
                    elif 0 <= row < gray_board_size and 0 <= col < gray_board_size and (row,col) in connected_cells:
                        check_left_more = False
                        row, col = ori_row, ori_col
                    else:
                        check_left_more = False
                        check_success = False
                        row, col = ori_row, ori_col
                if check_success:
                    captured_cells.append((ori_row,ori_col))

   # Remove captured cells with adjacent empty spaces
    changed = True
    while changed:
        changed = False
        to_remove = []
        for node in captured_cells:
            row, col = node
            for dr, dc in capture_directions:
                new_row, new_col = row + dr, col + dc
                if (new_row, new_col) in captured_cells:
                    continue  # Skip already marked captured cells
                if player == PLAYER_1:
                    
                    if 0 <= new_row < gray_board_size and 0 <= new_col < gray_board_size and grid_state[new_row][new_col] in (0,2,3,5):
                        to_remove.append((row, col))
                        changed = True
                        break  # Move to the next captured cell if any adjacent cell is empty
                elif player == PLAYER_2:
                
                    if 0 <= new_row < gray_board_size and 0 <= new_col < gray_board_size and grid_state[new_row][new_col] in (0,1,4,5):
                        to_remove.append((row, col))
                        changed = True
                        break  # Move to the next captured cell if any adjacent cell is empty

        # Remove cells with adjacent empty spaces
        for node in to_remove:
            captured_cells.remove(node)

    # Mark captured cells on the grid
    for node in captured_cells:
        row, col = node
        if player == PLAYER_1:
            if grid_state[row][col] == 0:
                grid_state[row][col] = 5
            elif grid_state[row][col] == 2:
                grid_state[row][col] = 4
        elif player == PLAYER_2:
            if grid_state[row][col] == 0:
                grid_state[row][col] = 5
            elif grid_state[row][col] == 1:
                grid_state[row][col] = 3

    # for row in range(gray_board_size):
    #     for col in range(gray_board_size):
    #         print(f"grid_state[{row}][{col}] = {grid_state[row][col]}")
    
    # print("\n")


if __name__ == "__main__":
    main()