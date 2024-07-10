from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from concurrent.futures import ThreadPoolExecutor
import time
import random
import threading

# Global counter
task_counter = 0
counter_lock = threading.Lock()

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
        # print(f"Clicked on the position ({click_width}, {click_height}) within the top 20% of the page.")
        return True

    except Exception as e:
        print(f"Error clicking within top 20%: {e}")
        return False

def automate_task():
    global task_counter

    # Set up Chrome options to open in incognito mode
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=200,300")  # Smaller window size
    chrome_options.add_argument("--log-level=3")

    # Path to your local ChromeDriver
    chrome_driver_path = "./chromedriver.exe"

    # Initialize the WebDriver with the local ChromeDriver
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

    try:
        # Open the website
        driver.get("https://bottest-phi.vercel.app/")  # Replace with the actual URL

        # Wait for 3 seconds on the main page before clicking
        time.sleep(3)

        # Click the top 20% of the page
        if click_top_20_percent(driver):
            # Wait for a new window or tab to open
            WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
            # print("New window or tab detected.")

            # Switch to the new window or tab
            new_window = [window for window in driver.window_handles if window != driver.current_window_handle][0]
            driver.switch_to.window(new_window)
            # print("Switched to new window/tab.")

            # Wait for 5 seconds to view the new page
            time.sleep(5)
            # print("Viewed the new page for 5 seconds.")

            # Close the new window/tab
            driver.close()
            # print("Closed the new window/tab.")

            # Switch back to the original window
            driver.switch_to.window(driver.window_handles[0])
            # print("Switched back to the original window.")
        
        # Update the task counter
        with counter_lock:
            task_counter += 1
            print(f"c: {task_counter}")
        
    except Exception as e:
        print(f"Error during automation: {e}")
    finally:
        # Close the browser
        driver.quit()
        # print("Browser closed.")

def start_threads(num_threads):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        try:
            while True:
                futures = [executor.submit(automate_task) for _ in range(num_threads)]
                for future in futures:
                    future.result()
        except KeyboardInterrupt:
            print("Interrupted! Stopping all threads...")

if __name__ == "__main__":
    number_of_threads = 16  # Set the number of threads you want to run
    try:
        start_threads(number_of_threads)
    except KeyboardInterrupt:
        print("Program interrupted by user. Exiting...")
