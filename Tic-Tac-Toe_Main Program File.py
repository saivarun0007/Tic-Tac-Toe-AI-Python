import pygame
import sys
import time
import tictactoe as ttt # Assuming this module is stable and correct

pygame.init()
pygame.display.set_caption("Tic-Tac-Toe-AI-Python")

# Screen setup
width, height = 1000, 650
screen = pygame.display.set_mode((width, height))

# Colors
background_color = (176, 207, 222)
text_color = (0, 0, 0)
button_color = (255, 255, 255)
hover_color = (200, 200, 255)
active_color = (150, 150, 255)
border_color = (50, 50, 50)
white = (255, 255, 255)
green = (144, 238, 144)
yellow = (255, 255, 153)
red = (255, 102, 102)

# Fonts
mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
mediumFont.set_bold(True)            
largeFont = pygame.font.SysFont("Arial", 40, bold=True)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)
scoreFont = pygame.font.Font("OpenSans-Regular.ttf", 24)
smallFont = pygame.font.Font("OpenSans-Regular.ttf", 20)
boldSmallFont = pygame.font.SysFont("Arial", 35, bold=True) 

# Sounds
click_sound = pygame.mixer.Sound("Sounds/click.wav")
ai_sound = pygame.mixer.Sound("Sounds/ai_move.wav")
button_sound = pygame.mixer.Sound("Sounds/button.wav")
tie_sound = pygame.mixer.Sound("Sounds/tie.wav")
win_x_sound = pygame.mixer.Sound("Sounds/win.wav")
win_o_sound = pygame.mixer.Sound("Sounds/win.wav")


class Button:
    def __init__(self, x, y, width, height, text, font, action=None, hover_color=(200, 200, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.action = action
        self.hovered = False
        self.hover_color = hover_color

    def draw(self, surface, override_color=None):
        color = override_color if override_color else (self.hover_color if self.hovered else button_color)
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=10)
        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def check_click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


def main():
    while True: # Outer loop: keeps the application running, allows full game restarts from main menu
        user = None
        mode = None  # Single or Multiplayer

        # Main menu loop for user and mode selection
        while user is None or mode is None:
            screen.fill(background_color)
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    button_sound.play()
                    sys.exit() 

            # Title
            title = largeFont.render("Play TIC-TAC-TOE Game ", True, text_color)
            screen.blit(title, title.get_rect(center=(width / 2, 30)))

            # Rules Section
            mediumFont.set_underline(True)
            rules_title = mediumFont.render("Rules to Play Game :", True, text_color)
            screen.blit(rules_title, rules_title.get_rect(midleft=(50, 80)))
            mediumFont.set_underline(False)
            
            rules = [
                 "1. Choose your symbol and select a game mode to begin.",
                 "2. Each players take turns clicking on empty blocks in the 3x3 grid with no time limit!",
                 "3. The game is played over 3 rounds. After each round, choose 'Next Round' or 'Quit'.",
                 "4. The goal is to get 3 matching symbols in a row (horizontally, vertically, or diagonally).",
                 "5. You can pause, resume, or restart the round anytime during gameplay.",
                 "6. The first player to align 3 matching symbols wins the round!",
                 "7. If the grid is full and no one wins, it's a tie game!",
                 "8. Don't want to play? Click 'Quit' anytime to exit the game."
            ]
            
            rule_y_offset = 110
            for rule in rules:
                rule_text = smallFont.render(rule, True, text_color)
                screen.blit(rule_text, (50, rule_y_offset))
                rule_y_offset += 25

            quote_text = boldSmallFont.render('"THINK AHEAD AND BLOCK YOUR OPPONENT FROM WINNING"', True, text_color)
            screen.blit(quote_text, quote_text.get_rect(center=(width / 2, rule_y_offset + 50)))


            # Player and Mode Selection Buttons
            play_x_btn = Button(width / 8, height / 2 + 80, width / 4, 50, "Play as X", mediumFont, hover_color = (204, 255, 204))
            play_o_btn = Button(5 * width / 8, height / 2 + 80, width / 4, 50, "Play as O", mediumFont, hover_color = "#F8B88B")
            single_btn = Button(width / 8, height / 2 + 150, width / 4, 50, "Single Player", mediumFont, hover_color = "#E3F9A6")
            multi_btn = Button(5 * width / 8, height / 2 + 150, width / 4, 50, "Multiplayer", mediumFont, hover_color=(255, 255, 204))
            quit_main_menu_btn = Button(width / 2 - 75, height - 70, 150, 50, "Quit", mediumFont, hover_color=red)


            for btn in [play_x_btn, play_o_btn, single_btn, multi_btn, quit_main_menu_btn]:
                btn.check_hover(mouse)
                btn.draw(screen)

            # Cursor change on hover
            if any([play_x_btn.hovered, play_o_btn.hovered, single_btn.hovered, multi_btn.hovered, quit_main_menu_btn.hovered]):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                if play_x_btn.check_click(mouse):
                    button_sound.play()
                    user = ttt.X
                    time.sleep(0.2)
                elif play_o_btn.check_click(mouse):
                    button_sound.play()
                    user = ttt.O
                    time.sleep(0.2)
                elif single_btn.check_click(mouse):
                    button_sound.play()
                    mode = "single"
                    time.sleep(0.2)
                elif multi_btn.check_click(mouse):
                    button_sound.play()
                    mode = "multi"
                    time.sleep(0.2)
                elif quit_main_menu_btn.check_click(mouse):
                    button_sound.play()
                    pygame.display.flip()
                    time.sleep(0.2)
                    pygame.quit() 
                    sys.exit()

            pygame.display.flip()

        # Initialize game state for a new set of rounds (3 rounds)
        board = ttt.initial_state()
        ai_turn = False
        win_sound_played = False
        rounds_played = 0
        x_wins = 0
        o_wins = 0
        ties = 0
        total_rounds = 3
        paused = False
        
        # This flag controls the exit from the inner game loop, returning to main menu cycle
        should_return_to_main_menu = False 

        button_width = 140
        button_height = 50
        button_x = width - button_width - 20
        button_gap = 20
        start_y = 180

        pause_button = Button(button_x, start_y, button_width, button_height, "Pause", mediumFont, hover_color=yellow)
        resume_button = Button(button_x, start_y + button_gap + button_height, button_width, button_height, "Resume", mediumFont, hover_color=green)
        restart_button = Button(button_x, start_y + 2 * (button_gap + button_height), button_width, button_height, "Restart", mediumFont, hover_color=red)

        level_btn_x = 20
        level_start_y = 180
        easy_btn = Button(level_btn_x, level_start_y, button_width, button_height, "Easy", mediumFont)
        medium_btn = Button(level_btn_x, level_start_y + button_height + button_gap, button_width, button_height, "Medium", mediumFont)
        hard_btn = Button(level_btn_x, level_start_y + 2 * (button_height + button_gap), button_width, button_height, "Hard", mediumFont)

        # Game round loop: This loop runs for a full set of `total_rounds`
        while True:
            # Check the flag at the very beginning of each iteration of the game loop
            if should_return_to_main_menu:
                break # This breaks out of the current (inner) game round loop

            screen.fill(background_color)
            mouse = pygame.mouse.get_pos()

            # Event handling for game play
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Drawing the Tic-Tac-Toe board
            tile_size = 100
            tile_origin = (width / 2 - 1.5 * tile_size, height / 2 - 1.5 * tile_size + 30)
            tiles = []

            for i in range(3):
                row = []
                for j in range(3):
                    rect = pygame.Rect(tile_origin[0] + j * tile_size, tile_origin[1] + i * tile_size, tile_size, tile_size)
                    pygame.draw.rect(screen, white, rect, 3)
                    if board[i][j] != ttt.EMPTY:
                        move = moveFont.render(board[i][j], True, text_color)
                        screen.blit(move, move.get_rect(center=rect.center))
                    row.append(rect)
                tiles.append(row)

            # Game state checks
            game_over = ttt.terminal(board)
            player = ttt.player(board)

            # Display game title
            title_surface = largeFont.render("TIC-TAC-TOE", True, text_color)
            screen.blit(title_surface, title_surface.get_rect(center=(width / 2, 30)))

            # Determine and display status text
            if paused:
                status_text = "Game Paused"
            elif game_over:
                winner = ttt.winner(board)
                if winner:
                    status_text = f"{winner} Wins!"
                    if not win_sound_played:
                        (win_x_sound if winner == "X" else win_o_sound).play()
                        if winner == "X":
                            x_wins += 1
                        else:
                            o_wins += 1
                        win_sound_played = True
                else:
                    status_text = "Tie Game - Well Played!"
                    if not win_sound_played:
                        tie_sound.play()
                        ties += 1
                        win_sound_played = True
            else:
                if mode == "multi":
                    status_text = f"{player}'s Turn"
                else:
                    status_text = "AI Thinking..." if user != player else f"Your Turn ({user})"

            status_render = mediumFont.render(status_text, True, text_color)
            screen.blit(status_render, status_render.get_rect(center=(width / 2, 80)))

            # Display score and round information
            score_text = f"Round: {rounds_played + 1}/{total_rounds}  X Wins: {x_wins}  O Wins: {o_wins}  Ties: {ties}"
            score_render = scoreFont.render(score_text, True, text_color)
            screen.blit(score_render, score_render.get_rect(center=(width / 2, 120)))

            # Draw in-game control buttons (Pause, Resume, Restart)
            for btn in [pause_button, resume_button, restart_button]:
                btn.check_hover(mouse)
                btn.draw(screen)

            # Draw difficulty level buttons (assuming single player only for now)
            level_colors = [green, yellow, red]
            level_buttons = [easy_btn, medium_btn, hard_btn]
            for i, btn in enumerate(level_buttons):
                btn.check_hover(mouse)
                blink = (rounds_played == i) 
                blink_color = level_colors[i] if blink else None
                btn.draw(screen, override_color=blink_color)

            # Determine and draw end-game buttons (Next Round/Play Again, Quit)
            if game_over:
                next_btn_text = "Play Again" if rounds_played >= total_rounds - 1 else "Next Round"
                next_btn = Button(width / 2 - 150, height - 70, 150, 50, next_btn_text, scoreFont, hover_color=green)
                quit_btn = Button(width / 2 + 30, height - 70, 120, 50, "Quit", scoreFont, hover_color=red)
                hovered_buttons_at_end = [next_btn, quit_btn]
            else:
                hovered_buttons_at_end = [] 

            # Cursor change based on any hovered button
            all_hovered_buttons = [pause_button, resume_button, restart_button] + level_buttons + hovered_buttons_at_end
            if any(btn.hovered for btn in all_hovered_buttons):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            click, _, _ = pygame.mouse.get_pressed()

            # Handle clicks on control buttons (Pause, Resume, Restart)
            if click == 1:
                if pause_button.check_click(mouse):
                    button_sound.play()
                    paused = True
                    time.sleep(0.2)
                elif resume_button.check_click(mouse):
                    button_sound.play()
                    paused = False
                    time.sleep(0.2)
                elif restart_button.check_click(mouse) and not game_over:
                    button_sound.play()
                    board = ttt.initial_state()
                    win_sound_played = False
                    ai_turn = False
                    paused = False
                    time.sleep(0.2)

            # Handle clicks on difficulty level buttons (if in single player mode)
            if mode == "single": 
                for i, btn in enumerate(level_buttons):
                    if click == 1 and btn.check_click(mouse):
                        button_sound.play()
                        time.sleep(0.2)

            # AI's turn logic
            if not paused and not game_over:
                if mode == "single" and user != player:
                    if ai_turn:
                        time.sleep(0.5)
                        move = ttt.minimax(board) 
                        if move is not None:
                            board = ttt.result(board, move)
                            ai_sound.play()
                            ai_turn = False
                    else:
                        ai_turn = True

            # Human player's turn logic (click on tiles)
            if click == 1 and not game_over and not paused:
                for i in range(3):
                    for j in range(3):
                        if board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse):
                            if mode == "multi" or user == player:
                                board = ttt.result(board, (i, j))
                                click_sound.play()

            # Logic when a round is over (game_over is True)
            if game_over:
                for btn in hovered_buttons_at_end: 
                    btn.check_hover(mouse)
                    btn.draw(screen)

                if click == 1:
                    if next_btn.check_click(mouse):
                        button_sound.play()
                        if rounds_played < total_rounds - 1:
                            board = ttt.initial_state()
                            win_sound_played = False
                            ai_turn = False
                            paused = False
                            rounds_played += 1 
                        else:
                            # ALL 3 ROUNDS ARE DONE.
                            # Set flag to return to the initial player/mode selection menu.
                            should_return_to_main_menu = True 
                        time.sleep(0.2)
                    elif quit_btn.check_click(mouse):
                        pygame.quit()
                        sys.exit()

            pygame.display.flip()
    

if __name__ == "__main__":
    main() 
    