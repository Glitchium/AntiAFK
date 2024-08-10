from pynput import keyboard, mouse
from pynput.keyboard import Controller as KeyboardController
import time
import threading

# Initialize the keyboard and mouse controllers
keyboard_controller = KeyboardController()
mouse_controller = mouse.Controller()

# List of keys to simulate circular movement (W, A, S, D)
keys = ['w', 'a', 's', 'd']

# Duration for holding each key
key_hold_duration = 0.2  # seconds

# Duration between mouse clicks
click_interval = 1  # seconds

# State variable to track whether the script is active
is_active = False
state_lock = threading.Lock()

def on_press(key):
    global is_active
    
    try:
        if key.char == 'f':  # Check if the 'f' key was pressed
            with state_lock:
                is_active = not is_active  # Toggle the active state
                if is_active:
                    print("Circular movement and clicking activated.")
                else:
                    print("Circular movement and clicking deactivated.")
    except AttributeError:
        # Handle special keys (not needed in this case)
        pass

def click_mouse():
    while True:
        with state_lock:
            if is_active:
                mouse_controller.click(mouse.Button.left)
                print("Mouse clicked.")
        time.sleep(click_interval)

def move_in_circle():
    while True:
        with state_lock:
            if not is_active:
                time.sleep(0.1)  # Short delay before checking the state again
                continue

        for key in keys:
            with state_lock:
                if not is_active:
                    break
            
            # Press and hold the key
            keyboard_controller.press(key)
            
            # Hold the key for the specified duration
            time.sleep(key_hold_duration)
            
            # Release the key
            keyboard_controller.release(key)
            
            # Print which key was pressed (for logging/debugging)
            print(f"Pressed {key}")
            
            # Short delay before the next key press to simulate smoother movement
            time.sleep(0.1)

# Print instructions to the console
print("Press 'F' to activate or deactivate circular movement and clicking.")
print("The script will keep running, listening for key presses.")

# Start mouse clicking in a separate thread
click_thread = threading.Thread(target=click_mouse, daemon=True)
click_thread.start()

# Start circular movement in the main thread
move_in_circle_thread = threading.Thread(target=move_in_circle, daemon=True)
move_in_circle_thread.start()

# Set up the keyboard listener
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
