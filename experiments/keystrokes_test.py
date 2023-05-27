import pyautogui
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Keystroke simulator')
    parser.add_argument('--delay', type=float, default=0.5, help='Time to delay before outputting keystrokes')
    parser.add_argument('--text', type=str, default='Hello World', help='Text to be typed')
    args = parser.parse_args()
    return args

def run(delay: float, text: str):
    pyautogui.sleep(delay)
    pyautogui.typewrite(text)

if __name__ == '__main__':
    args = parse_args()
    run(args.delay, args.text)
