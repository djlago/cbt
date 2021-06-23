from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os, time

username = os.getenv("daniel.lagomarsino@smartbear.com")
authkey = os.getenv("ub705bde7b5900d2")


caps = {
 'platform': 'Windows',
 'browserName': 'Chrome',
}

driver = webdriver.Remote(
    command_executor="http://%s:%s@hub.crossbrowsertesting.com/wd/hub"%(username, authkey),
    desired_capabilities=caps)



driver.get("http://www.google.com")
if not "Google" in driver.title:
    raise Exception("Unable to load google page!")
elem = driver.find_element_by_name("q")
elem.send_keys("CrossBrowserTesting")
elem.submit()
print(driver.title)
driver.quit()