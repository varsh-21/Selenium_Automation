import random
import time
import threading
import cv2
import numpy as np
import pyautogui

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

recording = True

def record_screen(filename="selenium_test_order-creation.avi", duration=120):
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

# Start screen recording
thread = threading.Thread(target=record_screen)
thread.start()

# Initialize WebDriver
service = Service("./chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.get("http://tutorialsninja.com/demo/")


# Navigate to Phones
driver.find_element(By.LINK_TEXT, "Phones & PDAs").click()
driver.find_element(By.LINK_TEXT, "iPhone").click()
time.sleep(1)
driver.find_element(By.XPATH, '//ul[@class="thumbnails"]/li[1]').click()
time.sleep(2)

next_button = driver.find_element(By.XPATH, '//button[@title="Next (Right arrow key)"]')
for _ in range(5):
    next_button.click()
    time.sleep(2)

driver.save_screenshot(f'screenshot_{random.randint(0,101)}.png')
driver.find_element(By.XPATH, '//button[@title="Close (Esc)"]').click()
time.sleep(1)

# Add iPhone to cart
# quantity = driver.find_element(By.ID, 'input-quantity')
# quantity.clear()
# quantity.send_keys('2')
# driver.find_element(By.ID, 'button-cart').click()
# time.sleep(2)

# Navigate to laptops
laptops = driver.find_element(By.LINK_TEXT, "Laptops & Notebooks")
ActionChains(driver).move_to_element(laptops).perform()
time.sleep(2)
driver.find_element(By.LINK_TEXT, "Show AllLaptops & Notebooks").click()
time.sleep(1)

#scroll

# Add HP laptop
driver.find_element(By.LINK_TEXT, "HP LP3065").click()
driver.find_element(By.XPATH, '//i[@class="fa fa-calendar"]').click()
time.sleep(1)

while driver.find_element(By.CLASS_NAME, "picker-switch").text != 'December 2011':
    driver.find_element(By.CLASS_NAME, "next").click()
time.sleep(2)

driver.find_element(By.XPATH, '//td[text()="31"]').click()
time.sleep(1)
driver.find_element(By.ID, 'button-cart').click()
time.sleep(1)

# driver.execute_script("window.scrollBy(0, 2000);")  # scroll down 500px

# View cart
driver.find_element(By.ID, 'cart-total').click()
time.sleep(1)
driver.find_element(By.XPATH, '//p[@class="text-right"]/a[1]').click()
time.sleep(2)

wait = WebDriverWait(driver, 10)

# Proceed to checkout (more stable selector)
checkout_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Checkout")]')))
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkout_btn)
checkout_btn.click()
time.sleep(3)
# # Click cart
# cart_link = wait.until(EC.element_to_be_clickable((By.ID, "cart")))
# cart_link.click()

# # Wait and click "View Cart" or "Checkout"
# checkout_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Checkout")]')))
# driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkout_btn)
# checkout_btn.click()

# Click on guest checkout option
guest = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="guest"]')))
guest.click()

# Click continue (Step 1)
continue_1 = wait.until(EC.element_to_be_clickable((By.ID, 'button-account')))
continue_1.click()

# Wait for Step 2 to load
wait.until(EC.visibility_of_element_located((By.ID, 'input-payment-firstname')))

# Fill out guest billing details
driver.find_element(By.ID, 'input-payment-firstname').send_keys('test_first_name')
driver.find_element(By.ID, 'input-payment-lastname').send_keys('test_last_name')
driver.find_element(By.ID, 'input-payment-email').send_keys('test@test.com')
driver.find_element(By.ID, 'input-payment-telephone').send_keys('012345678')
driver.find_element(By.ID, 'input-payment-address-1').send_keys('teststreet 187')
driver.find_element(By.ID, 'input-payment-city').send_keys('Frankfurt')
driver.find_element(By.ID, 'input-payment-postcode').send_keys('112233')

# Country
country_dropdown = Select(driver.find_element(By.ID, 'input-payment-country'))
country_dropdown.select_by_visible_text('Germany')

# Region
region_dropdown = Select(driver.find_element(By.ID, 'input-payment-zone'))
region_dropdown.select_by_visible_text('Hessen')

# Click continue (Step 2)
continue_2 = wait.until(EC.element_to_be_clickable((By.ID, 'button-guest')))
continue_2.click()

# Click continue (Step 3 - Shipping method)
continue_3 = wait.until(EC.element_to_be_clickable((By.ID, 'button-shipping-method')))
continue_3.click()

# Accept terms & conditions
agree = wait.until(EC.element_to_be_clickable((By.NAME, 'agree')))
agree.click()

# Click continue (Step 4 - Payment method)
continue_4 = wait.until(EC.element_to_be_clickable((By.ID, 'button-payment-method')))
continue_4.click()

# Final price
final_price = wait.until(EC.visibility_of_element_located(
    (By.XPATH, '//table[@class="table table-bordered table-hover"]/tfoot/tr[3]/td[2]')
))
print("The final price of both products is:", final_price.text)

# Click confirm
confirm = wait.until(EC.element_to_be_clickable((By.ID, 'button-confirm')))
confirm.click()

# Get success message
success_message = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="col-sm-12"]/h1')))
print("Order Success:", success_message.text)

# Optional: Close browser
# driver.quit()


# Billing Details already filled, just continue
driver.find_element(By.ID, 'button-payment-address').click()
time.sleep(2)

# Delivery Details
driver.find_element(By.ID, 'button-shipping-address').click()
time.sleep(2)

# Delivery Method
driver.find_element(By.ID, 'button-shipping-method').click()
time.sleep(2)

# Agree to Terms & Conditions
driver.find_element(By.NAME, 'agree').click()

# Payment Method
driver.find_element(By.ID, 'button-payment-method').click()
time.sleep(3)

# Final Total
final_price = driver.find_element(By.XPATH, '//table[@class="table table-bordered table-hover"]/tfoot/tr[last()]/td[2]')
print("The final price of both products is", final_price.text)

# Confirm Order
driver.find_element(By.ID, 'button-confirm').click()
time.sleep(3)

# Success
print("Success message:", driver.find_element(By.XPATH, '//div[@class="col-sm-12"]/h1').text)


driver.quit()
recording = False 
thread.join()
