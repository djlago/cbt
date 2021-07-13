# Please visit http://selenium-python.readthedocs.io/ for detailed installation and instructions
# Getting started: http://docs.seleniumhq.org/docs/03_webdriver.jsp
# API details: https://github.com/SeleniumHQ/selenium#selenium

# http://docs.python-requests.org/en/master/user/install/

import unittest
from selenium import webdriver
import requests
import time

class BasicTest(unittest.TestCase):
    def setUp(self):

        # Put your username and authey below
        # You can find your authkey at crossbrowsertesting.com/account
        self.username = "daniel.lagomarsino@smartbear.com"
        self.authkey  = "ub705bde7b5900d2"

        self.api_session = requests.Session()
        self.api_session.auth = (self.username,self.authkey)

        self.test_result = None

        self.contactFormFill = 'CrossBrowserTesting'

        caps = {}

        caps['name'] = 'Smartstore Test'
        caps['build'] = '1.0'
        caps['platform'] = 'Windows 10'
        caps['browserName'] = 'MicrosoftEdge'
        caps['version'] = '87'
        caps['screenResolution'] = '1366x768'
        caps['record_video'] = 'true'

        # start the remote browser on our server
        self.driver = webdriver.Remote(
            desired_capabilities=caps,
            command_executor="http://%s:%s@hub.crossbrowsertesting.com:80/wd/hub"%(self.username,self.authkey)
        )

        self.driver.implicitly_wait(20)

    def test_CBT(self):
        # We wrap this all in a try/except so we can set pass/fail at the end
        try:
            # load the page url
            print('Loading Url')
            self.driver.get('https://smartstore.alertsite.com/')


            # maximize the window - DESKTOPS ONLY
            print('Maximizing window')
            self.driver.maximize_window()

            # check the title
            print('Checking title')
            title = self.driver.title
            print('The title of the page should be = Shop')
            print("Actual page title is = %s" % title)
            self.assertEqual("Shop", self.driver.title)

            # Let's take a screenshot!
            self.api_session.post('https://crossbrowsertesting.com/api/v3/screenshots/?url=https://smartstore.alertsite.com&browsers=win10-E18|Edge87')


            # Login into the SmartStore!
            # Note, we can use multiple selectors! Such as XPath, element Name and css_selectors for buttons!
            print('Logging In')
            self.driver.find_element_by_xpath('//html[1]/body[1]/div[1]/div[2]/header[1]/div[1]/div[1]/nav[1]/nav[4]/div[1]/a[1]/span[1]').click()
            self.driver.find_element_by_name('Username').send_keys('cbttester')
            self.driver.find_element_by_name('Password').send_keys('cbttester')
            self.driver.find_element_by_css_selector(':nth-child(4) > button').click()


            # Hold up, wait a minute! Let the login complete and redirect us back to the home page.
            time.sleep(3)


            # Let's fill out the contact form!
            # First, find the Contact Us button and click it.
            print('Filling out the Contact Form and Submitting')
            self.driver.find_element_by_xpath('//*[@id="header"]/div[1]/div/nav/nav[2]/a').click()
            # Then enter text into the form field.
            self.driver.find_element_by_xpath('//*[@id="Enquiry"]').send_keys(self.contactFormFill)
            time.sleep(3)
            # Lastly, click on the Submit button.
            self.driver.find_element_by_xpath('//*[@id="content-center"]/div/div[3]/form/div[4]/div/button').click()


            # Redirect back to the homepage. It's easier to use a driver.get on a URL than switching frames.
            # This isn't so bad for desktops, but switching frames on mobile can be very problametic, especially for iOS.
            print('Heading back home')
            self.driver.get('https://smartstore.alertsite.com/')

            # Waiting for redirect
            time.sleep(3)

            # Let's add some cool stuff to our cart. I think we'll pick out some Gaming items!
            # First let's scroll the element we want to click into view. This isn't required, but helps when viewing the test's Video feed.
            print('Adding a Stationbox to out cart!')
            gamingElement = self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/section/div/div/div/div/div[2]/article[9]')
            self.driver.execute_script("return arguments[0].scrollIntoView();", gamingElement)
            time.sleep(3)

            # Now let's click on the Gaming section to find some items to add to our cart.
            self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/section/div/div/div/div/div[2]/article[9]').click()
            time.sleep(3)

            # Let's select a Stationbox!
            self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/section/div[2]/div/div/div[2]/div/div[2]/article[1]').click()
            # Now add it to the cart.
            self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/section/div[2]/div/div/article/div/form/section/aside/div[4]/div[4]/div/div[2]/a').click()
            time.sleep(3)

            # Redirect back to the homepage. It's easier to use a driver.get on a URL than switching frames.
            # This isn't so bad for desktops, but switching frames on mobile can be very problametic, especially for iOS.
            print('Heading back home')
            self.driver.get('https://smartstore.alertsite.com/')

            # Holding on!
            time.sleep(3)

            # Let's add The tablet from Mobile phones. First click on Mobile Phone
            print('Adding a Tablet to our cart!')
            self.driver.find_element_by_xpath('//*[@id="content-center"]/div/div/div[2]/article[1]/div[1]/a').click()
            # Now let's click on The Tablet. NOTE, we are using the Full XPATH here based on how the page is written.
            self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/section/div[2]/div/div/div[2]/div[1]/div[2]/article[1]').click()
            # Add The Tablet to the cart
            self.driver.find_element_by_xpath('//*[@id="pd-form"]/section/aside/div[4]/div[4]/div/div[2]/a').click()
            time.sleep(3)

            # Now let's verify the subtotal of the cart!
            print('Verifying Subtotal')
            subtotal = self.driver.find_element_by_xpath('/html/body/aside[2]/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div[2]')
            assert subtotal.text == '$588.00 excl tax'
            print('Subtotal should be = $588.00 excl tax')
            print("Subtotal is = %s" % subtotal.text)
            time.sleep(3)

            # Now let's remove the Stationbox and Tablet so we have an empty cart when we start this script.
            print('Emptying Cart Contents')
            self.driver.find_element_by_xpath('//*[@id="occ-cart"]/div[1]/div/div[1]/div[2]/div[3]/a[2]').click()
            time.sleep(3)
            self.driver.find_element_by_xpath('//*[@id="occ-cart"]/div[1]/div/div[1]/div[2]/div[3]/a[2]').click()
            time.sleep(3)


            # Redirect to home
            print('Heading back home, Test is complete!')
            self.driver.get('https://smartstore.alertsite.com/')

            time.sleep(3)

            # if we are still in the try block after all of our assertions that
            # means our test has had no failures, so we set the status to "pass"
            print('Everthing looks good! Setting score to Pass!')
            self.test_result = 'pass'

        except AssertionError as e:

            # if any assertions are false, we take a snapshot of the screen, log
            # the error message, and set the score to "during tearDown()".

            snapshot_hash = self.api_session.post('https://crossbrowsertesting.com/api/v3/selenium/' + self.driver.session_id + '/snapshots').json()['hash']
            self.api_session.put('https://crossbrowsertesting.com/api/v3/selenium/' + self.driver.session_id + '/snapshots/' + snapshot_hash,
                data={'description':"AssertionError: " + str(e)})
            self.test_result = 'fail'
            raise

    def tearDown(self):
        print("Done with session %s" % self.driver.session_id)
        self.driver.quit()
        # Here we make the api call to set the test's score.
        # Pass if it passes, fail if an assertion fails, unset if the test didn't finish
        if self.test_result is not None:
            self.api_session.put('https://crossbrowsertesting.com/api/v3/selenium/' + self.driver.session_id,
                data={'action':'set_score', 'score':self.test_result})


if __name__ == '__main__':
    unittest.main()
