import time
import threading
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Listener, KeyCode, Controller as KeyboardController

# Global variables
abort = False
select_mode = False
delay = 0.1
click_button = Button.left
start_stop_key = KeyCode(char='q')
exit_key = KeyCode(char='e')
selecting_key = KeyCode(char='`')

mouse = MouseController()
keyboard = KeyboardController()


class ClickMouse(threading.Thread):
    def __init__(self, delay, button):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True

    def start_clicking(self):
        global abort
        abort = False
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running and not abort:
                if isinstance(self.button, Button):
                    mouse.click(self.button)
                else:
                    keyboard.press(self.button)
                    keyboard.release(self.button)
                time.sleep(self.delay)
            time.sleep(0.05)


click_thread = ClickMouse(delay, click_button)
click_thread.start()


def on_press(key):
    global click_button, select_mode, selecting_key, abort

    if select_mode:
        print("Select mode detected")
        if key == selecting_key:
            # Double tap to reset
            click_button = Button.left
            click_thread.button = Button.left
            print("Reset click button to left mouse button")
        else:
            click_button = key
            click_thread.button = key
            print(f"New click button: {key}")
        select_mode = False
        print("Exiting select mode...")
    elif key == start_stop_key:
        if click_thread.running:
            click_thread.stop_clicking()
        else:
            click_thread.start_clicking()
    elif key == exit_key:
        abort = True
        click_thread.stop_clicking()
        print("Aborting...")
    elif key == selecting_key:
        select_mode = True
        print("Entering select mode...")


with Listener(on_press=on_press) as listener:
    listener.join()
