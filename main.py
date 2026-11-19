from engi1020.arduino.api import *
from alarm_clock import clock
from alarm_system import system
from games import *
from speech_rec import rec
from time import sleep

def main_menu():
    """
    Display the main menu and handle navigation and selection using rotary and button inputs.
    """
    while True:
        oled_clear()
        selector = analog_read(0)

        # Display menu based on selector range
        if selector <= 200:
            oled_print('Main Menu:       ALARM CLOCK?')
            selected_option = "ALARM CLOCK"
        elif 201 <= selector <= 400:
            oled_print('Main Menu:       ALARM SYSTEM?')
            selected_option = "ALARM SYSTEM"
        elif 401 <= selector <= 600:
            oled_print('Main Menu:       GAMES?')
            selected_option = "GAMES"
        elif 601 <= selector <= 1023:
            oled_print('Main Menu:       ASSISTANT?')
            selected_option = "ASSISTANT"

        # Confirm selection with button press
        if digital_read(6):  # Selection button
            oled_clear()
            oled_print(f'Selected: {selected_option}')
            sleep(2)
            oled_clear()
            return selected_option  # Pass the selected option to handle its execution

        sleep(0.1)

def game_menu():
    """
    Handles the game selection menu.
    """
    while True:
        selected_game = Game_Selector()  # Select a game
        if selected_game == "ROCK  PAPER SCISSORS":
            run_module(lambda: RPS_game())
        elif selected_game == "BOP-IT":
            run_module(lambda: BI_game())
        elif selected_game == "REACTION TIME":
            run_module(lambda: RT_game())
        elif selected_game == "ROCKET GAME":
            run_module(lambda: Rocket_game())
        elif selected_game == "SNAKE":
            run_module(lambda: Snake_game())
        else:
            break

def run_module(module_function):
    """
    Run a module and return to the main menu when 'back' button is pressed.
    """
    while True:
        # Check for the "back to menu" button
        if digital_read(7):
            oled_clear()
            oled_print("Returning to Main Menu...")
            sleep(2)
            break

        # Run the module function
        module_function()
        sleep(0.1)

if _name_ == "_main_":
    try:
        while True:
            selected_option = main_menu()  # Get the selected option

            # Handle the selected option
            if selected_option == "ALARM CLOCK":
                run_module(lambda: clock())
            elif selected_option == "ALARM SYSTEM":
                run_module(lambda: system())  # Replace with your alarm system logic
            elif selected_option == "GAMES":
                gaming()
            elif selected_option == "ASSISTANT":
                run_module(lambda: rec())

    except KeyboardInterrupt:
        oled_clear()
        oled_print("Exiting Program...")
        sleep(2)
        oled_clear()