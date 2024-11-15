from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

options = Options()
# options.add_argument('--headless')  # Enable headless mode

# Optional: If geckodriver is not in your PATH
# service = Service(executable_path='/path/to/geckodriver')

driver = webdriver.Firefox(options=options)  # Or with service: driver = webdriver.Firefox(service=service, options=options)

driver.get("https://weathershopper.pythonanywhere.com/")
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


print(low_temp)

if low_temp == True:
    product_price = driver.find_element(By.CSS_SELECTOR, "div.text-center.text-center.col-4:nth-child(1) p:nth-child(3)").text.split(" ")[2].strip()
    driver.find_element(By.CSS_SELECTOR, "div.text-center.col-4:nth-child(1) button").click()
   

else:
    product_price = driver.find_element(By.CSS_SELECTOR, "div.text-center.text-center.col-4:nth-child(1) p:nth-child(3)").text.split(" ")[2].strip()
    driver.find_element(By.CSS_SELECTOR, "div.text-center.col-4:nth-child(1) button").click()

print(product_price)
driver.find_element(By.CSS_SELECTOR, ".thin-text.nav-link").click()
checkout_price= driver.find_element(By.CSS_SELECTOR, "tbody tr td:nth-child(2)").text.strip()
assert checkout_price == product_price, f"Expected price {product_price}, but got {checkout_price}"







    
# driver.quit()
