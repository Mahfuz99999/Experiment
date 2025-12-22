import pyautogui
import time
import sys

def send_messages(message, count=1, delay=2):
    """
    Sends messages by simulating keyboard input
    """
    print(f"Starting in 10 seconds. Click on the text input field...")
    time.sleep(10)
    
    for i in range(count):
        # Type the message
        pyautogui.write(message)
        time.sleep(0.5)
        
        # Press Enter to send
        pyautogui.press('enter')
        
        print(f"Sent message {i+1}/{count}")
        
        if i < count - 1:
            time.sleep(delay)

if __name__ == "__main__":
    # Get user input
    msg = input("Enter message to send: ")
    num = int(input("How many times? (1): ") or "1")
    
    send_messages(msg, num)