# Importing the necessary modules
from engi1020.arduino.api import *
from time import *
import random
import pygame


# Pick auido
def pick_audio():
    buzzer_frequency(5, 600)
    sleep(0.1)
    buzzer_stop(5)

# Victory audio
def victory_audio():
    buzzer_frequency(5, 400)
    sleep(0.1)
    buzzer_frequency(5, 500)
    sleep(0.1)
    buzzer_frequency(5, 650)
    sleep(0.1)
    buzzer_frequency(5, 730)
    sleep(0.2)
    buzzer_frequency(5, 650)
    sleep(0.1)
    buzzer_frequency(5, 730)
    sleep(0.6)
    buzzer_stop(5)

# Point awarded audio
def point_awarded_audio():
    buzzer_frequency(5, 430)
    sleep(0.1)
    buzzer_frequency(5, 750)
    sleep(0.4)
    buzzer_stop(5)
    
# Victory light
def victory_light():
    digital_write(4, True)
    sleep(0.07)
    digital_write(4, False)
    sleep(0.07)
    digital_write(4, True)
    sleep(0.07)
    digital_write(4, False)
    sleep(0.07)
    digital_write(4, True)
    sleep(0.07)
    digital_write(4, False)

def defeat_audio():
    buzzer_frequency(5, 600)
    sleep(0.2)
    buzzer_frequency(5, 500)
    sleep(0.5)
    buzzer_stop(5)
    
def loading_audio():
    buzzer_frequency(5, 400)
    sleep(0.2)
    buzzer_frequency(5, 500)
    sleep(0.2)
    buzzer_frequency(5, 400)
    sleep(0.2)
    buzzer_frequency(5, 500)
    sleep(0.2)
    buzzer_frequency(5, 400)
    sleep(0.2)
    buzzer_frequency(5, 500)
    sleep(0.2)
    buzzer_frequency(5, 400)
    sleep(0.4)
    buzzer_stop(5)

# Dialog 1
oled_clear()
oled_print('                ')
oled_print("     Let's      ")
oled_print('     Play!      ')
oled_print('                ')
victory_light()
victory_audio()
sleep(1)
oled_clear()

# Game Selector function using the Rotary Potentiometer and thresholds
sleep(0.5)
def Game_Selector():  
    while True:
        oled_clear()
        selector = analog_read(0)
        
        if selector <= 200:
            oled_print('Select a Game:   ROCK PAPER      SCISSORS?')
            selected_game = "ROCK  PAPER SCISSORS"
        elif 201 <= selector <= 400:
            oled_print('Select a game:   BOP-IT?')
            selected_game = "BOP-IT"
        elif 401 <= selector <= 600:
            oled_print('Select a game:   REACTION TIME?')
            selected_game = "REACTION TIME"
        elif 601 <= selector <= 800:
            oled_print('Select a game:   ROCKET GAME')
            selected_game = "ROCKET GAME"
        elif 801 <= selector <= 1023:
            oled_print('Select a game:   SNAKE')
            selected_game = "SNAKE"
            
        # Printing the selected game on the OLED display     
        if digital_read(6):
            oled_clear()
            oled_print(f'Selected: {selected_game}')
            loading_audio()
            sleep(2)
            oled_clear()
            return selected_game
        
        sleep(0.1)


# Rock Paper Scissors game code
def RPS_game():
    options = ("ROCK", "PAPER", "SCISSORS")  # Ensure consistent casing
    running = True

    while running:
        player = None  # Reset player choice each round
        computer = random.choice(options)  # Randomly choose for computer
        oled_clear()

        # Rock paper scissor selection
        while True:
            oled_clear()
            RPS_selector = analog_read(0)  # Read the potentiometer value

            # Determine weapon based on potentiometer value
            if RPS_selector <= 340:
                oled_print('Pick a weapon:\n ROCK')
                player = "ROCK"
            elif 341 <= RPS_selector <= 680:
                oled_print('Pick a weapon:\n PAPER')
                player = "PAPER"
            elif 681 <= RPS_selector <= 1023:
                oled_print('Pick a weapon:\n SCISSORS')
                player = "SCISSORS"

            sleep(0.1)

            # Confirm selection with button press
            if digital_read(6):
                oled_clear()
                oled_print(f'Selected: {player}')
                point_awarded_audio()
                sleep(2)
                oled_clear()
                break

        # Show choices
        oled_print(f"Player: {player}")
        pick_audio()
        sleep(1)
        oled_print(f"Computer: {computer}")
        pick_audio()
        sleep(1.5)
        oled_clear()

        # Determine winner
        if player == computer:
            oled_print("IT'S A TIE!")
            defeat_audio()
        elif (player == "ROCK" and computer == "SCISSORS") or \
             (player == "PAPER" and computer == "ROCK") or \
             (player == "SCISSORS" and computer == "PAPER"):
            oled_print("YOU WIN!")
            victory_audio()
            victory_light()
            sleep(0.2)
        else:
            oled_print("YOU LOSE!")
            defeat_audio()

        sleep(2)
        oled_clear()

        # Check if the player wants to play again
        oled_print('Play Again?     Hold the button')
        pick_audio()
        sleep(4)
        if digital_read(6) != True:
            oled_clear()
            running = False
            oled_print("Exiting RPS...")
            loading_audio()
            sleep(2)
            oled_clear()
        else:
            oled_clear()
            oled_print('Starting new    game...')
            loading_audio()
            sleep(2)

def BI_game():         
    running = True
    commands = ("Bop it!", "Twist it!", "Shout it!",)
    score = 0
    time_limit = 3.0
    
    # Command chooser code
    while running:
        oled_clear()
        command = random.choice(commands)
        oled_print(command)
        pick_audio()
        sleep(1)

        # Perform action based on the command
        success = False
        start_time = time()

        while time() - start_time < time_limit:
            if command == "Bop it!" and digital_read(6) == True:  # Button press
                success = True
                break
            elif command == "Twist it!" and analog_read(0) > 600:  # Potentiometer twist
                success = True
                break
            elif command == "Shout it!" and analog_read(2) > 600:  # Microphone detects sound
                success = True
                break

        oled_clear()
        if success:
            oled_print("Good job!")
            digital_write(4,True)
            point_awarded_audio()
            score += 1
            time_limit = max(0.3, time_limit - 0.3)
            sleep(1)
            digital_write(4,False)
        else:
            oled_print("Game Over!")
            defeat_audio()
            running = False
            sleep(2)
            oled_clear()
            oled_print(f'Your score is: {score}')
            pick_audio()
            sleep(3)
            oled_clear()
            oled_print('Play Again?     Hold the button')
            pick_audio()
            sleep(4)
            if digital_read(6) != True:
                oled_clear()
                running = False
                oled_print("Exiting Bop-It...")
                loading_audio()
                sleep(2)
                oled_clear()
            else:
                oled_clear()
                oled_print('Starting new    game...')
                loading_audio()
                sleep(2)
                time_limit = 3.0

def RT_game():
    running = True
    score = 0

    oled_clear()
    oled_print("Get Ready...")
    pick_audio()
    sleep(2)

    while running:
        oled_clear()
        oled_print("Wait for it...")
        random_delay = random.uniform(1, 5)  # Random delay between 1 and 5 seconds
        delay_start = time()  # Record the start of the delay
        button_pressed = False
        
        # Buzzer sound during the random delay
        while time() - delay_start < random_delay:
            buzzer_frequency(5, 800)
            sleep(0.06)
            buzzer_stop(5)
            
        # Start the signal
        oled_clear()
        oled_print("Press NOW!")
        buzzer_frequency(5, 500)
        start_time = time()

        # Wait for player to press the button
        button_pressed = False
        while not button_pressed:
            if digital_read(6):
                reaction_time = time() - start_time
                button_pressed = True
                buzzer_stop(5)

        # Step 4: Display reaction time
        oled_clear()
        oled_print(f"Time: {reaction_time:.2f}s")
        victory_audio()

        sleep(2)

        # Step 5: Ask if the player wants to play again
        oled_clear()
        oled_print('Play Again?     Hold the button')
        pick_audio()
        sleep(4)
        if digital_read(6) != True:
            oled_clear()
            running = False
            oled_print("Exiting Reaction Time...")
            loading_audio()
            sleep(2)
            oled_clear()
        else:
            oled_clear()
            oled_print('Starting new    game...')
            loading_audio()
            sleep(2)
            continue


def Rocket_game():
    # Initialize pygame
    pygame.init()

    # Screen dimensions
    WIDTH, HEIGHT = 800, 300
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Lane Dodger")

    # Colors
    SKY_BLUE = (30, 30, 60)  # Dark sky
    WHITE = (255, 255, 255)  # Stars and text
    GREY = (169, 169, 169)  # Spaceship
    RED = (178, 34, 34)  # Asteroids (darker red for a rock look)
    BLACK = (0, 0, 0)  # Outlines

    # Lane settings
    lane_y_positions = [HEIGHT // 4, HEIGHT // 2, 3 * HEIGHT // 4]  # Lanes (Y-coordinates)

    # Spaceship settings
    ship_width, ship_height = 50, 30
    ship_x = 100
    current_lane = 1  # Start in the middle lane (index 1)

    # Asteroid settings
    asteroid_width, asteroid_height = 40, 40
    asteroid_speed = 6
    active_asteroids = []  # Track active asteroids
    max_asteroids = 2  # Limit asteroids on screen

    # Star settings
    stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(100)]  # Full-screen stars

    # Game settings
    clock = pygame.time.Clock()
    score = 0
    font = pygame.font.Font(None, 36)

    # Load background music
    music_path = r"C:\Users\Nabiha\OneDrive\Desktop\PROJECT\Space_music.mp3"
    pygame.mixer.music.load(music_path)  # Load music
    pygame.mixer.music.set_volume(0.5)  # Adjust volume (0.0 to 1.0)
    pygame.mixer.music.play(-1)  # Loop the music indefinitely

    def draw_spaceship(lane):
        y = lane_y_positions[lane] - ship_height // 2
        pygame.draw.polygon(win, GREY, [(ship_x, y), (ship_x + ship_width, y + ship_height // 2), (ship_x, y + ship_height)])
        pygame.draw.circle(win, WHITE, (ship_x + 15, y + ship_height // 2), 8)
        pygame.draw.polygon(win, RED, [(ship_x, y + ship_height // 4), (ship_x - 15, y + ship_height // 2), (ship_x, y + 3 * ship_height // 4)])

    def draw_asteroid(x, lane):
        y = lane_y_positions[lane] - asteroid_height // 2
        points = [
            (x + 10, y + 5),
            (x + 20, y),
            (x + 30, y + 10),
            (x + 40, y + 20),
            (x + 30, y + 30),
            (x + 20, y + 35),
            (x + 10, y + 30),
            (x, y + 20),
        ]
        pygame.draw.polygon(win, RED, points)  # Fill
        pygame.draw.polygon(win, BLACK, points, 2)  # Outline

    def draw_stars():
        for star in stars:
            pygame.draw.circle(win, WHITE, star, 2)

    # Main game loop
    running = True
    while running:
        clock.tick(30)
        win.fill(SKY_BLUE)

        # Draw stars
        draw_stars()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Rotary dial control
        rotary_value = analog_read(0)
        if rotary_value < 340:  # First third
            current_lane = 0  # Top lane
        elif 340 <= rotary_value < 680:  # Second third
            current_lane = 1  # Middle lane
        else:  # Third third
            current_lane = 2  # Bottom lane

        # Move and manage asteroids
        for asteroid in active_asteroids[:]:
            asteroid["x"] -= asteroid_speed # Copy list to safely modify while iterating
            
            if asteroid["x"] < -asteroid_width:
              active_asteroids.remove(asteroid)
              score += 1
            
            if asteroid["lane"] == current_lane and asteroid["x"] < ship_x + ship_width and asteroid["x"] + asteroid_width > ship_x:
                pygame.quit()
                oled_clear()
                oled_print("Game Over!")
                defeat_audio()
                sleep(2)
                oled_clear()
                oled_print(f'Your score is: {score}')
                pick_audio()
                sleep(3)
                oled_clear()
                oled_print('Play Again?     Hold the button')
                pick_audio()
                sleep(4)
                if digital_read(6) == False:
                    oled_clear()
                    running = False
                    oled_print("Exiting Rocket...")
                    loading_audio()
                    sleep(2)
                    oled_clear()
                    return
                else:
                    oled_clear()
                    oled_print('Starting new    game...')
                    loading_audio()
                    sleep(2)
                    Rocket_game()  # Restart the game
                    return

        # Spawn new asteroids if below max limit
        if len(active_asteroids) < max_asteroids:
            available_lanes = [lane for lane in range(3) if lane not in [a["lane"] for a in active_asteroids]]
            if available_lanes:  # Ensure there's at least one free lane
                new_asteroid = {"x": WIDTH, "lane": random.choice(available_lanes)}
                active_asteroids.append(new_asteroid)

        # Gradually increase asteroid speed based on score
        asteroid_speed = 6 + score // 5  # Speed increases every 5 points

        # Draw spaceship and asteroids
        draw_spaceship(current_lane)
        for asteroid in active_asteroids:
            draw_asteroid(asteroid["x"], asteroid["lane"])

        # Display score
        score_text = font.render(f"Score: {score}", True, WHITE)
        win.blit(score_text, (10, 10))

        pygame.display.flip()

    pygame.quit()


def Snake_game():
    # Initialize pygame
    pygame.init()

    # Screen dimensions
    WIDTH, HEIGHT = 600, 600
    GRID_SIZE = 20  # Size of each grid cell
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")

    # Colors
    BLACK = (0, 0, 0)
    DARK_GREY = (30, 30, 30)  # Background
    GREEN = (0, 255, 0)  # Outline
    RED = (255, 0, 0)  # Apple
    WHITE = (255, 255, 255)

    # Game settings
    clock = pygame.time.Clock()
    snake_speed = 3  # Frames per second

    # Snake settings
    snake_pos = [[WIDTH // 2, HEIGHT // 2]]  # List of positions [x, y]
    snake_direction = "UP"  # Initial direction

    # Apple settings
    apple_pos = [
        random.randrange(0, WIDTH, GRID_SIZE),
        random.randrange(0, HEIGHT, GRID_SIZE),
    ]

    # Load background music
    music_path = r"C:\Users\Nabiha\OneDrive\Desktop\PROJECT\Snake_music.mp3"
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.5)  # Adjust volume (0.0 to 1.0)
    pygame.mixer.music.play(-1)  # Play music in a loop

    def draw_snake(snake):
        #Draw the snake with a triangle head and square body.
        for index, segment in enumerate(snake):
            x, y = segment
            if index == 0:  # Head
                if snake_direction == "UP":
                    pygame.draw.polygon(win, BLACK, [(x + GRID_SIZE // 2, y), (x, y + GRID_SIZE), (x + GRID_SIZE, y + GRID_SIZE)])
                    pygame.draw.polygon(win, GREEN, [(x + GRID_SIZE // 2, y), (x, y + GRID_SIZE), (x + GRID_SIZE, y + GRID_SIZE)], 2)
                elif snake_direction == "DOWN":
                    pygame.draw.polygon(win, BLACK, [(x, y), (x + GRID_SIZE, y), (x + GRID_SIZE // 2, y + GRID_SIZE)])
                    pygame.draw.polygon(win, GREEN, [(x, y), (x + GRID_SIZE, y), (x + GRID_SIZE // 2, y + GRID_SIZE)], 2)
                elif snake_direction == "LEFT":
                    pygame.draw.polygon(win, BLACK, [(x + GRID_SIZE, y), (x, y + GRID_SIZE // 2), (x + GRID_SIZE, y + GRID_SIZE)])
                    pygame.draw.polygon(win, GREEN, [(x + GRID_SIZE, y), (x, y + GRID_SIZE // 2), (x + GRID_SIZE, y + GRID_SIZE)], 2)
                elif snake_direction == "RIGHT":
                    pygame.draw.polygon(win, BLACK, [(x, y), (x + GRID_SIZE, y + GRID_SIZE // 2), (x, y + GRID_SIZE)])
                    pygame.draw.polygon(win, GREEN, [(x, y), (x + GRID_SIZE, y + GRID_SIZE // 2), (x, y + GRID_SIZE)], 2)
            else:  # Body
                pygame.draw.rect(win, BLACK, (x, y, GRID_SIZE, GRID_SIZE))  # Body square
                pygame.draw.rect(win, GREEN, (x, y, GRID_SIZE, GRID_SIZE), 2)  # Outline

    def draw_apple(x, y):
        #Draw the apple as a red circle.
        pygame.draw.circle(win, RED, (x + GRID_SIZE // 2, y + GRID_SIZE // 2), GRID_SIZE // 2)

    def check_collision(head, body):
        #Check if the snake's head collides with its body or the wall.
        x, y = head
        # Wall collision
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            return True
        # Body collision
        if head in body[1:]:
            return True
        return False

    # Main game loop
    running = True
    while running:
        clock.tick(snake_speed)
        win.fill(DARK_GREY)  # Background color

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Exit the game
                pygame.quit()
                oled_clear()
                oled_print("Exiting SNAKE...")
                loading_audio()
                sleep(2)
                oled_clear()
                return  # Return to game selector

        # Rotary dial control for direction
        rotary_value = analog_read(0)
        if 768 <= rotary_value <= 1023 and snake_direction != "UP":  # Fourth quarter
            snake_direction = "DOWN"
        elif 512 <= rotary_value <= 767 and snake_direction != "RIGHT":  # Third quarter
            snake_direction = "LEFT"
        elif 256 <= rotary_value <= 511 and snake_direction != "DOWN":  # Second quarter
            snake_direction = "UP"
        elif 0 <= rotary_value <= 255 and snake_direction != "LEFT":  # First quarter
            snake_direction = "RIGHT"

        # Move snake
        head_x, head_y = snake_pos[0]
        if snake_direction == "UP":
            head_y -= GRID_SIZE
        elif snake_direction == "DOWN":
            head_y += GRID_SIZE
        elif snake_direction == "LEFT":
            head_x -= GRID_SIZE
        elif snake_direction == "RIGHT":
            head_x += GRID_SIZE
        new_head = [head_x, head_y]
        snake_pos.insert(0, new_head)

        # Check for apple collision
        if new_head == apple_pos:
            apple_pos = [
                random.randrange(0, WIDTH, GRID_SIZE),
                random.randrange(0, HEIGHT, GRID_SIZE),
            ]
        else:
            snake_pos.pop()  # Remove tail unless the snake grows

        # Check for collisions
        if check_collision(new_head, snake_pos):
            pygame.quit()
            oled_clear()
            oled_print("Game Over!")
            defeat_audio()
            sleep(2)
            oled_clear()
            oled_print(f'Your score is: {len(snake_pos) - 1}')
            pick_audio()
            sleep(3)
            oled_clear()
            oled_print('Play Again?     Hold the button')
            pick_audio()
            sleep(4)
            if digital_read(6) != True:
                oled_clear()
                running = False
                oled_print("Exiting Snake...")
                loading_audio()
                sleep(2)
                oled_clear()
                break
            else:
                oled_clear()
                oled_print('Starting new    game...')
                loading_audio()
                sleep(2)
                Snake_game()  # Restart the game
                return

        # Draw everything
        draw_snake(snake_pos)
        draw_apple(apple_pos[0], apple_pos[1])

        # Display score
        score_text = f"Score: {len(snake_pos) - 1}"
        font = pygame.font.Font(None, 36)
        score_surface = font.render(score_text, True, WHITE)
        win.blit(score_surface, (10, 10))

        pygame.display.flip()

    pygame.quit()


# Main program loop
while True:
    # Show the game selection menu
    selected_game = Game_Selector()
    
    # Execute the selected game
    if selected_game == "ROCK  PAPER SCISSORS":
        RPS_game()
        
    elif selected_game == "BOP-IT":
        BI_game()
        
    elif selected_game == "REACTION TIME":
        RT_game()
        
    elif selected_game == "ROCKET GAME":
        Rocket_game()
        
    elif selected_game == "SNAKE":
        Snake_game()

