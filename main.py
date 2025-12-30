import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# GitHub Actions Secrets se data uthayega
USERNAME = os.environ['YLH_USER']
PASSWORD = os.environ['YLH_PASS']

def init_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    return webdriver.Chrome(options=options)

def main():
    driver = init_driver()
    try:
        print("--- BEASTGPT GITHUB RUNNER ---")
        print("Logging in...")
        driver.get("https://www.youlikehits.com/login.php")
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(USERNAME)
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        driver.find_element(By.CSS_SELECTOR, "input[value='Log in']").click()
        time.sleep(3)
        
        print("Login Attempted. Switching to Website Hits...")
        driver.get("https://www.youlikehits.com/websites.php")
        
        start_time = time.time()
        # 5 Hours run limit (GitHub kills job after 6 hrs)
        while time.time() - start_time < 18000: 
            try:
                # Check Points
                try:
                    p = driver.find_element(By.ID, "currentpoints").text
                    print(f"💰 Balance: {p}")
                except: pass

                # Find Visit Button
                # 'visitbutton' class usually handles website hits
                buttons = driver.find_elements(By.CLASS_NAME, "visitbutton")
                if not buttons:
                    print("No websites found. Refreshing...")
                    driver.refresh()
                    time.sleep(5)
                    continue
                
                print("🚀 Visiting Website...")
                main_window = driver.current_window_handle
                
                # Click logic
                driver.execute_script("arguments[0].click();", buttons[0])
                time.sleep(2)
                
                # Switch to popup
                if len(driver.window_handles) > 1:
                    driver.switch_to.window(driver.window_handles[1])
                    # Website hits need ~20-25 seconds
                    wait = random.randint(22, 28)
                    time.sleep(wait)
                    driver.close()
                    driver.switch_to.window(main_window)
                    print("✅ Viewed. Points should add.")
                else:
                    print("Failed to open popup.")
                    time.sleep(5)
                
                driver.get("https://www.youlikehits.com/websites.php")
                time.sleep(2)
                
            except Exception as e:
                print(f"Error: {e}")
                driver.refresh()
                time.sleep(5)
                
    except Exception as e:
        print(f"Critical: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
