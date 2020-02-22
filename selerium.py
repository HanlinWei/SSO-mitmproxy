import mydriver
from selenium.webdriver.common.by import By
import time

# start browser
driver = mydriver.efficientChrome(False, "chrome-profile", "127.0.0.1:8080")
driver2 = mydriver.efficientChrome(False, "chrome-profile2", "127.0.0.1:8081")

# driver.get('test.xxx:8000')
driver.get('https://www.biblegateway.com')
driver2.get('https://www.biblegateway.com')

# log in
mydriver.click_xpath(driver, "/html/body/header/nav/div[2]/a")
mydriver.click_xpath(driver2, "/html/body/header/nav/div[2]/a")
mydriver.click_xpath(driver, "/html/body/header/nav/div[3]/div[4]/a")
mydriver.click_xpath(driver2, "/html/body/header/nav/div[3]/div[4]/a")
time.sleep(6)
# log out
mydriver.click_xpath(driver, "//*[@id=\"plus-welcome-modal\"]/div/div/div[1]/button")
mydriver.click_xpath(driver, "/html/body/header/nav/ul[2]/li/a/span[1]")
mydriver.click_xpath(driver, "/html/body/header/nav/ul[2]/li/ul/li[4]/a")

mydriver.click_xpath(driver2, "//*[@id=\"plus-welcome-modal\"]/div/div/div[1]/button")
mydriver.click_xpath(driver2, "/html/body/header/nav/ul[2]/li/a/span[1]")
mydriver.click_xpath(driver2, "/html/body/header/nav/ul[2]/li/ul/li[4]/a")