from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Start browser
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15)

# Open target page (CHANGE THIS)
driver.get("https://facebook.com/login")
driver.maximize_window()

# Email field
email_element = wait.until(
    EC.visibility_of_element_located((By.XPATH, "//input[@type='email']"))
)
email_element.send_keys("rajiv@test.org")

# Password field
pass_element = wait.until(
    EC.visibility_of_element_located((By.XPATH, "//input[@type='password']"))
)
pass_element.send_keys("testing@123")

# Login button
login_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
)
login_button.click()

# Optional: wait for status/message after login
status_element = wait.until(
    EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'message')]"))
)
print("Status message:", status_element.text)

time.sleep(5)
driver.quit()
