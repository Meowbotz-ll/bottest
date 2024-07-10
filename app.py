from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

def click_top_20_percent(driver):
    try:
        # Get the size of the window
        window_height = driver.execute_script("return window.innerHeight")
        window_width = driver.execute_script("return window.innerWidth")

        # Define the area to click (top 20% of the page)
        click_height = random.randint(0, int(window_height * 0.2))
        click_width = random.randint(0, window_width)

        # Move to the specified location and click
        actions = ActionChains(driver)
        actions.move_by_offset(click_width, click_height).click().perform()
        print(f"Clicked on the position ({click_width}, {click_height}) within the top 20% of the page.")
        return True

    except Exception as e:
        print(f"Error clicking within top 20%: {e}")
        return False

def automate_task():
    # Set up Chrome options to open in incognito mode
    chrome_options = Options()
    chrome_options.add_argument("--incognito")

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Open the website
        driver.get("https://textbookshop.webflow.io/")  # Replace with the actual URL

        # Wait for 3 seconds on the main page before clicking
        time.sleep(3)

        # Click the top 20% of the page
        if click_top_20_percent(driver):
            # Wait for a new window or tab to open
            WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
            print("New window or tab detected.")

            # Switch to the new window or tab
            new_window = [window for window in driver.window_handles if window != driver.current_window_handle][0]
            driver.switch_to.window(new_window)
            print("Switched to new window/tab.")

            # Wait for 5 seconds to view the new page
            time.sleep(5)
            print("Viewed the new page for 5 seconds.")

            # Close the new window/tab
            driver.close()
            print("Closed the new window/tab.")

            # Switch back to the original window
            driver.switch_to.window(driver.window_handles[0])
            print("Switched back to the original window.")
        
    except Exception as e:
        print(f"Error during automation: {e}")
    finally:
        # Close the browser
        driver.quit()
        print("Browser closed.")

if _name_ == "__main__":
    while True:
        automate_task()
        print("Restarting the task...")
        # Wait a bit before restarting the task
        time.sleep(10)  # Adjust the delay as needed before restarting