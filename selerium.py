import mydriver
from selenium.webdriver.common.by import By

# start browser
driver = mydriver.efficientChrome(False, "chrome-profile")

# open gitlab and login with github
driver.get('https://gitlab.com/users/sign_in')
# mydriver.wait(driver, (By.ID, "oauth-login-github"))
# mydriver.pause_before_redirect(driver)
# sign_in = driver.find_element_by_id("oauth-login-github")
# sign_in.click()