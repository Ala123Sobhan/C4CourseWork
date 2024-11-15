from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time


def setup_browser(browser):
    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--headless")  # Uncomment for headless mode
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(options=options)
    elif browser == "firefox":
        options = FirefoxOptions()
        options.add_argument("--headless") 
        driver = webdriver.Firefox(options=options)  # Or with service: driver = webdriver.Firefox(service=service, options=options)
    driver.maximize_window()
    driver.get("https://weathershopper.pythonanywhere.com/")
    return driver


# options = Options()
# # options.add_argument('--headless')  # Enable headless mode
# # Optional: If geckodriver is not in your PATH
# # service = Service(executable_path='/path/to/geckodriver')
# driver = webdriver.Firefox(options=options)  # Or with service: driver = webdriver.Firefox(service=service, options=options)

def valid_creditcard_test(browser, valid_card,  test_card):
    driver = setup_browser(browser)
    title = driver.title
    low_temp = False
    print(f"Page title: {title}")

    temperature = int(driver.find_element(By.ID,"temperature").text.split(" ")[0].strip())

    print(temperature)

    if temperature < 19:
        driver.find_element(By.CSS_SELECTOR, "a[href='/moisturizer']").click()
        low_temp = True
    elif temperature > 34:
        driver.find_element(By.CSS_SELECTOR, "a[href='/sunscreen']").click()

    product_price = driver.find_element(By.CSS_SELECTOR, "div.text-center.text-center.col-4:nth-child(1) p:nth-child(3)").text.split(" ")[2].strip()
    driver.find_element(By.CSS_SELECTOR, "div.text-center.col-4:nth-child(1) button").click()
    print(product_price)
    driver.find_element(By.CSS_SELECTOR, ".thin-text.nav-link").click()
    checkout_price= driver.find_element(By.CSS_SELECTOR, "tbody tr td:nth-child(2)").text.strip()
    assert checkout_price == product_price, f"Expected price {product_price}, but got {checkout_price}"

    driver.find_element(By.CSS_SELECTOR, "button[type='submit'] span").click()
    driver.switch_to.frame(0)
    wait = WebDriverWait(driver, 10)
    email_element = wait.until(EC.element_to_be_clickable((By.ID, "email")))
    email_element.click()
    email_element.send_keys("a@gmail.com")

 
    card_num_element = wait.until(EC.element_to_be_clickable((By.ID, "card_number")))
    card_num_element.click()
    test_exp = "04 / 28"
 
    if valid_card == True:
        driver.execute_script("document.getElementById('card_number').value = arguments[0];", test_card)
    else:
        driver.execute_script("document.getElementById('card_number').value = arguments[0];", test_card)

    driver.find_element(By.ID, "cc-exp").click()
    driver.execute_script("document.getElementById('cc-exp').value = arguments[0];", test_exp)
    driver.find_element(By.ID, "cc-csc").click()
    driver.find_element(By.ID, "cc-csc").send_keys("242")

    
    zip_element = wait.until(EC.visibility_of_element_located((By.ID, "billing-zip")))
    zip_element.send_keys("10462")

    driver.find_element(By.CSS_SELECTOR, ".iconTick").click()
    driver.switch_to.default_content()
    message_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "p.text-justify")))
    actual_text = message_element.text
    expected_substring = "Your payment was successful"
    if valid_card == True:
        assert expected_substring in actual_text, f"Expected text to include: '{expected_substring}', but got: '{actual_text}'"
    else:
        assert expected_substring not in actual_text, f"Expected text not to include: '{expected_substring}', but got: '{actual_text}'"
    driver.quit()


  