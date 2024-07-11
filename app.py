from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from concurrent.futures import ThreadPoolExecutor
import time
import random
import threading

# Global counter and stop flag
task_counter = 0
stop_flag = threading.Event()
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
    

    while not stop_flag.is_set():
        try:
            # Initialize the WebDriver with the local ChromeDriver
            driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

            # Open the website
            driver.get("https://myriowwebsite.vercel.app/")  # Replace with the actual URL

            # Wait for 3 seconds on the main page before clicking
            time.sleep(3)

            # Click the top 20% of the page
            if click_top_20_percent(driver):
                # Wait for a new window or tab to open
                WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)

                # Switch to the new window or tab
                new_window = [window for window in driver.window_handles if window != driver.current_window_handle][0]
                driver.switch_to.window(new_window)

                # Wait for 5 seconds to view the new page
                time.sleep(5)

                # Close the new window/tab
                driver.close()

                # Switch back to the original window
                driver.switch_to.window(driver.window_handles[0])
            
            # Update the task counter
            with counter_lock:
                task_counter += 1
                print(f"{task_counter}")

        except Exception as e:
            if stop_flag.is_set():
                break
            print(f"Error during automation: {e}")
            time.sleep(2)  # Wait before retrying

        finally:
            # Close the browser
            try:
                driver.quit()
            except:
                pass  # Ignore errors while closing the driver

def start_threads(num_threads):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        try:
            futures = [executor.submit(automate_task) for _ in range(num_threads)]
            for future in futures:
                future.result()
        except KeyboardInterrupt:
            print("Interrupted! Stopping all threads...")

def monitor_stop_flag():
    global stop_flag
    while True:
        user_input = input()
        if user_input.lower() == 'q':
            stop_flag.set()
            print("Stopping all tasks...")
            break

if __name__ == "__main__":
    number_of_threads = 20  # Set the number of threads you want to run

    # Start the monitor thread
    stop_thread = threading.Thread(target=monitor_stop_flag)
    stop_thread.start()

    try:
        start_threads(number_of_threads)
    except KeyboardInterrupt:
        print("Program interrupted by user. Exiting...")
