import random
import time
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
import cv2
import numpy as np
import pyautogui
import threading
import time

recording = True

def record_screen(filename="selenium_test_record.avi", duration=60):
    screen_size = pyautogui.size()
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(filename, fourcc, 10.0, screen_size)
    start_time = time.time()
    
    while recording and (time.time() - start_time) < duration:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)

    out.release()

# Start screen recording in a background thread
thread = threading.Thread(target=record_screen)
thread.start()

# Initialize the ChromeDriver Service
service = Service("./chromedriver.exe")

# Start Chrome
driver = webdriver.Chrome(service=service)

# Go to Google
driver.get("https://www.google.com")

# # Initialize webdriver
# driver = webdriver.Chrome('C:/bin/chromedriver3.exe')

# Open URL and maximize window
driver.get('http://tutorialsninja.com/demo/')
driver.maximize_window()



# Phones button
phones = driver.find_element(By.XPATH, '//a[text()="Phones & PDAs"]')
phones.click()

# iPhone
iphone = driver.find_element(By.XPATH, '//a[text()="iPhone"]')
iphone.click()
time.sleep(1)

# First picture
first_pic = driver.find_element(By.XPATH, '//ul[@class="thumbnails"]/li[1]')
first_pic.click()
time.sleep(2)

# Next picture
next_click = driver.find_element(By.XPATH, '//button[@title="Next (Right arrow key)"]')
for i in range(5):
    next_click.click()
    time.sleep(2)

# Save screenshot
driver.save_screenshot('screenshot#' + str(random.randint(0, 101)) + '.png')

# Close image popup
x_button = driver.find_element(By.XPATH, '//button[@title="Close (Esc)"]')
x_button.click()
time.sleep(1)

# Quantity
quantity = driver.find_element(By.ID, 'input-quantity')
quantity.clear()
quantity.send_keys('2')
time.sleep(1)

# Add to cart
add_to_button = driver.find_element(By.ID, 'button-cart')
add_to_button.click()
time.sleep(2)

# scroll window
# Scroll to bottom of the page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)

# Navigate to laptops
laptops = driver.find_element(By.XPATH, '//a[text()="Laptops & Notebooks"]')
action = ActionChains(driver)
action.move_to_element(laptops).perform()
time.sleep(2)

# Navigate to My Account > Register
my_account = driver.find_element("xpath", '//span[text()="My Account"]')
my_account.click()
time.sleep(1)

register = driver.find_element("xpath", '//a[text()="Register"]')
register.click()
time.sleep(2)

# Fill registration form
driver.find_element("id", "input-firstname").send_keys("TestFirst")
driver.find_element("id", "input-lastname").send_keys("TestLast")
driver.find_element("id", "input-email").send_keys(f"varshithabrtest{random.randint(1000,9999)}@mail.com")
driver.find_element("id", "input-telephone").send_keys("9876543210")
driver.find_element("id", "input-password").send_keys("Test@1234")
driver.find_element("id", "input-confirm").send_keys("Test@1234")

# Subscribe? No
driver.find_element("xpath", '//input[@name="newsletter" and @value="0"]').click()

# Agree to privacy policy
driver.find_element("name", "agree").click()

# Click Continue
driver.find_element("xpath", '//input[@value="Continue"]').click()
time.sleep(2)

# Print success message
success = driver.find_element("xpath", '//div[@id="content"]/h1')
print("Registration Success Message:", success.text)

driver.quit()

# Stop recording
recording = False
thread.join()
