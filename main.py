import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# GitHub Actions Secrets
USERNAME = os.environ['YLH_USER']
PASSWORD = os.environ['YLH_PASS']

def init_driver():
    options = Options()
    options.add_argument('--headless=new') # New headless mode is better
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1920,1080")
    # Fake User Agent to look like a Real Gamer PC
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    return webdriver.Chrome(options=options)

def main():
    driver = init_driver()
    try:
        print("--- BEASTGPT GHOST PROTOCOL (GITHUB) ---")
        print("Logging in...")
        driver.get("https://www.youlikehits.com/login.php")
        
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(USERNAME)
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        driver.find_element(By.CSS_SELECTOR, "input[value='Log in']").click()
        time.sleep(5)
        
        # Verify Login
        if "login.php" in driver.current_url:
            print("❌ Login Failed! Check Username/Password in Secrets.")
            return

        print("✅ Login Success! Targeting YouTube Likes...")
        driver.get("https://www.youlikehits.com/youtubelikes.php")
        
        start_time = time.time()
        # 5.5 Hours Loop (Safe Zone)
        while time.time() - start_time < 19800:
            try:
                # 1. Balance Check
                try:
                    p = driver.find_element(By.ID, "currentpoints").text
                    print(f"💰 Balance: {p} Points")
                except: pass

                # 2. Find Tasks
                # YouTube Likes uses 'followbutton' class
                btns = driver.find_elements(By.CLASS_NAME, "followbutton")
                if not btns:
                    print("⚠️ No tasks found. Refreshing...")
                    driver.refresh()
                    time.sleep(10)
                    continue

                print("👻 Ghosting Video Task...")
                main_window = driver.current_window_handle
                
                # Execute Click
                driver.execute_script("arguments[0].click();", btns[0])
                time.sleep(2)
                
                # Handle Popup
                if len(driver.window_handles) > 1:
                    driver.switch_to.window(driver.window_handles[1])
                    # Wait 35s to trick system
                    time.sleep(35)
                    driver.close()
                    driver.switch_to.window(main_window)
                else:
                    # Inline handling
                    time.sleep(35)
                
                # 3. Confirm Button (Critical for Likes)
                try:
                    confirm = driver.find_elements(By.XPATH, "//a[contains(text(),'Confirm')]")
                    if confirm:
                        confirm[0].click()
                        print("✅ Confirmed Task.")
                    else:
                        print("✅ Auto-Confirmed.")
                except: pass
                
                # Reload for next
                driver.get("https://www.youlikehits.com/youtubelikes.php")
                time.sleep(random.randint(3, 6))

            except Exception as e:
                print(f"⚠️ Error: {e}")
                driver.refresh()
                time.sleep(5)

    except Exception as e:
        print(f"🔥 Critical: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
