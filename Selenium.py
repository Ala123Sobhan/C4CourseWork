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
print(f"Page title: {title}")

temperature = int(driver.find_element(By.ID,"temperature").text.split(" ")[0].strip())

print(temperature)

if temperature < 19:
    driver.find_element(By.CSS_SELECTOR, "a[href='/moisturizer']").click()
elif temperature > 34:
    driver.find_element(By.CSS_SELECTOR, "a[href='/sunscreen']").click()



driver.quit()
