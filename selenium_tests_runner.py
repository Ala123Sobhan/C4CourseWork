import Selenium

Selenium.valid_creditcard_test("chrome", True, "4242424242424242")
Selenium.valid_creditcard_test("firefox", False, "4000000000009995")


# generic decline 4000000000000002 , 4000000000009995 (insufficient funds)
  