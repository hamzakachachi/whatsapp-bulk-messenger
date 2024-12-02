from playwright.sync_api import sync_playwright
from urllib.parse import quote
from time import sleep
import os

class Style:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

print(Style.BLUE)
print("**********************************************************")
print("**********************************************************")
print("*****                                               ******")
print("*****  THANK YOU FOR USING WHATSAPP BULK MESSENGER  ******")
print("*****      This tool was built by Anirudh Bagri     ******")
print("*****           www.github.com/anirudhbagri         ******")
print("*****                                               ******")
print("**********************************************************")
print("**********************************************************")
print(Style.RESET)

# Read the message from the file
with open("message.txt", "r", encoding="utf8") as f:
    message = f.read()

print(Style.YELLOW + '\nThis is your message:')
print(Style.GREEN + message + "\n" + Style.RESET)
message = quote(message)

# Read the numbers from the file
numbers = []
with open("numbers.txt", "r") as f:
    for line in f.read().splitlines():
        if line.strip():
            numbers.append(line.strip())

total_number = len(numbers)
print(Style.RED + f'We found {total_number} numbers in the file' + Style.RESET)
delay = 30

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir="/var/tmp/chrome_user_data", headless=False
    )
    page = browser.new_page()

    print('Once your browser opens up sign in to web WhatsApp')
    page.goto('https://web.whatsapp.com')

    input(Style.MAGENTA + "AFTER logging into WhatsApp Web is complete and your chats are visible, press ENTER..." + Style.RESET)

    for idx, number in enumerate(numbers):
        number = number.strip()
        if not number:
            continue
        print(Style.YELLOW + f'{idx + 1}/{total_number} => Sending message to {number}.' + Style.RESET)

        try:
            url = f'https://web.whatsapp.com/send?phone={number}&text={message}'
            sent = False
            for i in range(3):
                if not sent:
                    page.goto(url)
                    try:
                        page.wait_for_selector("button[aria-label='Send']", timeout=delay * 1000)
                        send_button = page.query_selector("button[aria-label='Send']")
                        if send_button:
                            send_button.click()
                            sent = True
                            sleep(3)
                            print(Style.GREEN + f'Message sent to: {number}' + Style.RESET)
                    except Exception as e:
                        print(Style.RED + f"\nFailed to send message to: {number}, retry ({i + 1}/3)")
                        print("Make sure your phone and computer are connected to the internet.")
                        print("If there is an alert, please dismiss it." + Style.RESET)
        except Exception as e:
            print(Style.RED + f'Failed to send message to {number}: {str(e)}' + Style.RESET)

    # browser.close()
