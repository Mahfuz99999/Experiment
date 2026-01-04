"""
MESSENGER AUTOMATION SCRIPT
Read warnings below before using
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import json
import os

# ⚠️ WARNING: Against Facebook's Terms of Service
# Risk of temporary or permanent account suspension
# Use only for legitimate, non-spam purposes

class MessengerAutomator:
    def __init__(self, headless=False):
        """Initialize the browser"""
        options = webdriver.ChromeOptions()
        
        # Optional: Run in background (remove to see browser)
        if headless:
            options.add_argument('--headless')
        
        # Add arguments to appear more human-like
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 20)
        
    def login(self, email=None, password=None):
        """
        Login to Facebook Messenger
        Either auto-login or manual login
        """
        print("Opening Messenger...")
        self.driver.get("https://www.messenger.com")
        
        # Check if already logged in
        time.sleep(3)
        if "login" not in self.driver.current_url.lower():
            print("Already logged in!")
            return True
        
        if email and password:
            print("Attempting auto-login...")
            try:
                # Enter email
                email_field = self.wait.until(
                    EC.presence_of_element_located((By.ID, "email"))
                )
                self.human_type(email_field, email)
                time.sleep(random.uniform(0.5, 1.5))
                
                # Enter password
                password_field = self.driver.find_element(By.ID, "pass")
                self.human_type(password_field, password)
                time.sleep(random.uniform(0.5, 1.5))
                
                # Click login
                login_button = self.driver.find_element(By.NAME, "login")
                login_button.click()
                
                # Wait for login to complete
                time.sleep(5)
                print("Login successful!")
                return True
                
            except Exception as e:
                print(f"Auto-login failed: {e}")
                print("Please login manually...")
                input("Press Enter after manual login...")
                return True
        else:
            print("Please login manually in the browser...")
            input("Press Enter after you've logged in successfully...")
            return True
    
    def human_type(self, element, text, min_delay=0.05, max_delay=0.2):
        """Type like a human with random delays"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(min_delay, max_delay))
    
    def search_and_select_contact(self, contact_name):
        """Search for a contact and open conversation"""
        print(f"Searching for: {contact_name}")
        
        try:
            # Find search box
            search_box = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search Messenger']"))
            )
            search_box.clear()
            time.sleep(random.uniform(0.5, 1))
            
            # Type contact name
            self.human_type(search_box, contact_name)
            time.sleep(random.uniform(1, 2))
            
            # Press Enter to select first result
            search_box.send_keys(Keys.ENTER)
            time.sleep(random.uniform(2, 3))
            
            # Wait for chat to load
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']"))
            )
            print(f"Conversation with {contact_name} opened")
            return True
            
        except Exception as e:
            print(f"Could not find contact '{contact_name}': {e}")
            return False
    
    def send_message(self, message, contact_name=None):
        """Send a message to current or specified contact"""
        if contact_name:
            if not self.search_and_select_contact(contact_name):
                return False
        
        try:
            # Find message input box
            message_box = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']"))
            )
            
            # Click to focus
            message_box.click()
            time.sleep(random.uniform(0.3, 0.7))
            
            # Type message
            self.human_type(message_box, message)
            time.sleep(random.uniform(0.5, 1))
            
            # Press Enter to send
            message_box.send_keys(Keys.ENTER)
            
            # Random delay after sending
            time.sleep(random.uniform(1, 3))
            
            print(f"Message sent: '{message[:50]}...'")
            return True
            
        except Exception as e:
            print(f"Failed to send message: {e}")
            return False
    
    def send_multiple_messages(self, messages, contact_name, delay_between=5):
        """Send multiple messages to one contact"""
        if not self.search_and_select_contact(contact_name):
            return
        
        for i, msg in enumerate(messages):
            print(f"Sending message {i+1}/{len(messages)}")
            self.send_message(msg)
            
            # Delay between messages (with randomness)
            if i < len(messages) - 1:
                delay = delay_between + random.uniform(-1, 1)
                print(f"Waiting {delay:.1f} seconds...")
                time.sleep(delay)
    
    def send_to_multiple_contacts(self, contact_messages, delay_between=10):
        """Send messages to multiple contacts"""
        for contact, messages in contact_messages.items():
            print(f"\n--- Contact: {contact} ---")
            
            if isinstance(messages, str):
                self.send_message(messages, contact)
            else:
                self.send_multiple_messages(messages, contact)
            
            # Longer delay between different contacts
            time.sleep(random.uniform(delay_between, delay_between + 5))
    
    def schedule_message(self, contact_name, message, send_time):
        """Schedule a message for later"""
        from datetime import datetime
        current_time = datetime.now()
        
        if isinstance(send_time, str):
            send_time = datetime.strptime(send_time, "%Y-%m-%d %H:%M:%S")
        
        wait_seconds = (send_time - current_time).total_seconds()
        
        if wait_seconds > 0:
            print(f"Message scheduled for {send_time}")
            print(f"Waiting {wait_seconds/60:.1f} minutes...")
            time.sleep(wait_seconds)
            return self.send_message(message, contact_name)
        else:
            print("Scheduled time has already passed!")
            return False
    
    def close(self):
        """Close the browser"""
        self.driver.quit()
        print("Browser closed")

# ========== CONFIGURATION ==========
def load_config():
    """Load configuration from file or create default"""
    config = {
        # ⭐ CHANGE THESE SETTINGS ⭐
        "headless": False,  # Set True to run in background
        "manual_login": True,  # Set False to use auto-login below
        
        # ⭐ Auto-login credentials (use with caution!)
        "email": "",  # Your Facebook email
        "password": "",  # Your Facebook password
        
        # ⭐ Message configuration
        "messages": [
            "Hello! This is a test message.",
            "Just checking in.",
            "Hope you're having a great day!"
        ],
        
        # ⭐ Contacts to message
        "contacts": {
            "Friend 1": "Hi! How are you?",
            "Friend 2": ["Message 1", "Message 2"],
            "Group Name": "Hello everyone!"
        },
        
        # ⭐ Timing settings
        "delay_between_messages": 5,  # Seconds
        "delay_between_contacts": 15  # Seconds
    }
    
    # Save config file for easy editing
    if not os.path.exists('messenger_config.json'):
        with open('messenger_config.json', 'w') as f:
            json.dump(config, f, indent=4)
        print("Config file created: messenger_config.json")
        print("Edit it before running!")
        return None
    
    return config

# ========== MAIN USAGE EXAMPLES ==========
def example_usage():
    """Different ways to use the automator"""
    
    # Example 1: Simple single message
    def send_single_message():
        bot = MessengerAutomator()
        if bot.login():
            bot.send_message("Hello from Python!", "Friend's Name")
            bot.close()
    
    # Example 2: Bulk messages to multiple contacts
    def bulk_messaging():
        config = load_config()
        if not config:
            return
        
        bot = MessengerAutomator(headless=config['headless'])
        
        # Choose login method
        if config['manual_login']:
            bot.login()
        else:
            bot.login(config['email'], config['password'])
        
        # Send to all contacts
        bot.send_to_multiple_contacts(
            config['contacts'],
            delay_between=config['delay_between_contacts']
        )
        
        bot.close()
    
    # Example 3: Scheduled message
    def scheduled_message():
        bot = MessengerAutomator()
        bot.login()
        
        # Schedule for 10 minutes from now
        from datetime import datetime, timedelta
        send_time = datetime.now() + timedelta(minutes=10)
        
        bot.schedule_message(
            "Contact Name",
            "This is a scheduled message!",
            send_time
        )
        
        bot.close()
    
    # Example 4: Conversation starter
    def conversation_starter():
        bot = MessengerAutomator()
        bot.login()
        
        conversation_icebreakers = [
            "Hey! Long time no talk. How have you been?",
            "I was just thinking about our last conversation!",
            "Hope you're having a productive week!",
            "Saw this and thought of you: [link or content]"
        ]
        
        contacts = ["Close Friend 1", "Close Friend 2", "Family Member"]
        
        for contact in contacts:
            message = random.choice(conversation_icebreakers)
            bot.send_message(message, contact)
            time.sleep(random.uniform(30, 60))  # Long delays
    
    return bulk_messaging  # Choose which example to run

# ========== SAFETY FEATURES ==========
def safety_checks():
    """Add these safety measures before running"""
    
    print("=" * 60)
    print("MESSENGER AUTOMATION SAFETY CHECK")
    print("=" * 60)
    
    checks = [
        ("Have you read Facebook's Terms of Service?", False),
        ("Are you only messaging people who expect to hear from you?", False),
        ("Is this for non-commercial, personal use?", False),
        ("Will you keep message frequency low (max 5-10/hour)?", False),
        ("Do you have a backup account in case of restrictions?", False),
    ]
    
    all_yes = True
    for question, default in checks:
        response = input(f"{question} (y/N): ").lower()
        if response != 'y':
            all_yes = False
    
    if not all_yes:
        print("\n⚠️  SAFETY CHECK FAILED!")
        print("Please reconsider using automation.")
        print("Press Enter to exit...")
        input()
        return False
    
    print("\n✅ Safety checks passed (but risk still exists)")
    print("Starting in 5 seconds...")
    time.sleep(5)
    return True

# ========== MAIN EXECUTION ==========
if __name__ == "__main__":
    # Run safety checks first
    if not safety_checks():
        exit()
    
    # Load or create configuration
    config = load_config()
    if config is None:
        print("Please edit messenger_config.json first!")
        exit()
    
    # Initialize bot
    print("\nInitializing Messenger automation...")
    bot = MessengerAutomator(headless=config['headless'])
    
    try:
        # Login
        if config['manual_login']:
            print("\nPlease login manually in the Chrome window...")
            print("You have 60 seconds to login")
            success = bot.login()
        else:
            print("\nAttempting auto-login...")
            success = bot.login(config['email'], config['password'])
        
        if not success:
            print("Login failed!")
            bot.close()
            exit()
        
        print("\nLogin successful! Starting messaging...")
        time.sleep(2)
        
        # Send messages based on config
        if config['contacts']:
            bot.send_to_multiple_contacts(
                config['contacts'],
                delay_between=config['delay_between_contacts']
            )
        else:
            print("No contacts configured in messenger_config.json")
        
        print("\n✅ All messages sent successfully!")
        
    except KeyboardInterrupt:
        print("\n⚠️  Stopped by user")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
    finally:
        bot.close()
        print("\nScript ended. Remember to use responsibly!")