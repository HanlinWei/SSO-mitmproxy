from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# driver version: 78.0.3904.105
# the driver version (78.0.3904.xxx) should be the same as the Chrome browser in your computer
"""
an efficient way to open a browser instance
"""
def efficientChrome(test=True, dir=None):
    chrome_options = Options()
    chrome_options.add_argument('--no-proxy-server')
    # chrome_options.add_argument('--proxy-server=127.0.0.1:8080')
    if dir:
        chrome_options.add_argument("--user-data-dir=" + dir)
    if test:
        chrome_options.add_argument('--headless') # forbid browser UI
        chrome_options.add_argument('blink-settings=imagesEnabled=false') # forbid loading image
    return webdriver.Chrome(chrome_options=chrome_options)

"""
wait for a specific element loading
"""
def wait(driver, expected, timeout=4):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(expected)
        )
    except Exception as e:
        logging.error("[mybrowsers.wait] " + e.__str__())

"""
open a new tab in driver
"""
def open_tab(driver, url):
    driver.execute_script("window.open(" + url + ",'_blank');")

"""
pause the browser, block the 302 redirect
"""
def pause_before_redirect(driver):
    driver.execute_script("window.addEventListener(\"beforeunload\", function() { debugger; }, false)")

# driver version: phantomjs-2.1.1-windows
# def getPhantomJS():
#     return webdriver.PhantomJS()