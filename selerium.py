import mydriver
from selenium.webdriver.common.by import By
import time

# start browser
driver = mydriver.efficientChrome(False, "chrome-profile2")

driver.get('https://www.biblegateway.com')
# mydriver.wait(driver, (By.CLASS_NAME, "btn navbar-btn btn-sign-in login-btn-in navbar-right"))
# driver.find_element_by_class_name('btn navbar-btn btn-sign-in login-btn-in navbar-right').click()

# log in
mydriver.click_xpath(driver, "/html/body/header/nav/div[2]/a")
mydriver.click_xpath(driver, "/html/body/header/nav/div[3]/div[4]/a")
time.sleep(6)
# log out
mydriver.click_xpath(driver, "//*[@id=\"plus-welcome-modal\"]/div/div/div[1]/button")
mydriver.click_xpath(driver, "/html/body/header/nav/ul[2]/li/a/span[1]")
mydriver.click_xpath(driver, "/html/body/header/nav/ul[2]/li/ul/li[4]/a")
