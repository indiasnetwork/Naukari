#! python3
# -*- coding: utf-8 -*-
# Naukri Daily update - Using Chrome
import re, os
import sys
import time
import logging
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException

ResumePath = "Resume.pdf"
NaukriURL = "https://login.naukri.com/nLogin/Login.php"

log_file_path = "naukri.log"
logging.basicConfig(level=logging.INFO,
                    filename=log_file_path,
                    format='%(asctime)s    : %(message)s')
# logging.disable(logging.CRITICAL)


def GetElement(driver, elementTag, locator='ID'):
    '''Wait max 15 secs for element and then select when it is available'''
    try:
        if locator == 'ID':
            if is_element_present(driver, By.ID, elementTag):
                return WebDriverWait(driver, 15).until(lambda driver: driver.find_element_by_id(elementTag))
            else:
                print('%s Not Found.' % elementTag)
                return None

        elif locator == 'NAME':
            if is_element_present(driver, By.NAME, elementTag):
                return WebDriverWait(driver, 15).until(lambda driver: driver.find_element_by_name(elementTag))
            else:
                print('%s Not Found.' % elementTag)
                return None

        elif locator == 'XPATH':
            if is_element_present(driver, By.XPATH, elementTag):
                return WebDriverWait(driver, 15).until(lambda driver: driver.find_element_by_xpath(elementTag))
            else:
                print('%s Not Found.' % elementTag)
                return None

        elif locator == 'CSS':
            if is_element_present(driver, By.CSS_SELECTOR, elementTag):
                return WebDriverWait(driver, 15).until(
                    lambda driver: driver.find_element_by_css_selector(elementTag))
            else:
                print('%s Not Found.' % elementTag)
                return None

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        lineNo = str(exc_tb.tb_lineno)
        logging.info('Error identifying element - %s : %s : %s at Line %s.' %
                     (elementTag, type(e), e, lineNo))
        print('Error identifying element - %s : %s : %s at Line %s.' %
              (elementTag, type(e), e, lineNo))
        return None


def is_element_present(driver, how, what):
    try:
        driver.find_element(by=how, value=what)
    except NoSuchElementException:
        return False
    return True


def WaitTillElementPresent(driver, elementTag, locator='ID'):
    '''Wait till element present. Max 60 seconds'''
    for i in range(60):
        try:
            if locator == 'ID':
                if is_element_present(driver, By.ID, elementTag):
                    break
            elif locator == 'NAME':
                if is_element_present(driver, By.NAME, elementTag):
                    break
            elif locator == 'XPATH':
                if is_element_present(driver, By.XPATH, elementTag):
                    break
            elif locator == 'CSS':
                if is_element_present(driver, By.CSS_SELECTORS, elementTag):
                    break
        except Exception as e:
            print('Exception when WaitTillElementPresent : %s' % e)
            pass
        time.sleep(0.99)
    else:
        print("Timed out. Unable to find the Element: %s" % elementTag)


def tearDown(driver):
    try:
        driver.close()
        logging.info('Driver Closed Successfully')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        lineNo = str(exc_tb.tb_lineno)
        logging.info('Error : %s : %s at Line %s.' % (type(e), e, lineNo))
        pass

    try:
        driver.quit()
        logging.info('Driver Quit Successfully')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        lineNo = str(exc_tb.tb_lineno)
        logging.info('Error quitting: %s : %s at Line %s.' % (type(e), e, lineNo))
        print('Error quitting: %s : %s at Line %s.' % (type(e), e, lineNo))
        pass


def naukriLogin():
    options = webdriver.ChromeOptions()
    # Path to your chrome profile
    chromedriver = "chromedriver.exe"
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")       # ("--kiosk") for MAC
    options.add_argument("--disable-popups")

    if os.path.exists(ChromePath) and os.path.exists(chromedriver):
        try:
            driver = webdriver.Chrome(chrome_options=options, executable_path=chromedriver)
            driver.maximize_window()
            print("Google Chrome Launched!")
            logging.info("Google Chrome Launched!")

            driver.implicitly_wait(3)
            driver.get(NaukriURL)
            
            if 'Naukri.com' in driver.title:
                print("Website Loaded Successfully.")
                logging.info("Website Loaded Successfully.")

            username = "Type Your email ID Here"
            password = "Type Your Password Here"

            if is_element_present(driver, By.ID, "emailTxt"):
                emailFieldElement = GetElement(driver, "emailTxt", locator='ID')
                time.sleep(1)
                passFieldElement = GetElement(driver, "pwd1", locator='ID')
                time.sleep(1)
                loginButton = driver.find_element_by_xpath("//*[@type='submit' and @value='Login']")
            elif is_element_present(driver, By.ID, "usernameField"):
                emailFieldElement = GetElement(driver, "usernameField", locator='ID')
                time.sleep(1)
                passFieldElement = GetElement(driver, "passwordField", locator='ID')
                time.sleep(1)
                loginButton = driver.find_element_by_xpath('//*[@type="submit"]')

            else:
                print('None of the elements found to login.')
                logging.info('None of the elements found to login.')
                return None

            if emailFieldElement is not None:
                emailFieldElement.clear()
                emailFieldElement.send_keys(username)
                passFieldElement.clear()
                passFieldElement.send_keys(password)
                time.sleep(1)
                loginButton.send_keys(Keys.ENTER)

                # CheckPoint
                WaitTillElementPresent(driver, 'dPic', locator='ID')
                CheckPoint = GetElement(driver, 'dPic', locator='ID')
                if CheckPoint:
                    print('Login Successful')
                    logging.info('Login Successful')
                    return driver
                else:
                    print('Unknown Login Error')
                    logging.info('Unknown Login Error')
                    return None

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            lineNo = str(exc_tb.tb_lineno)
            logging.info('Error logging in Naukri: %s : %s at Line %s.\n'% (type(e), e, lineNo))
            print('Error logging in Naukri: %s : %s at Line %s.' % (type(e), e, lineNo))
            tearDown(driver)
            return None

    else:
        print('Chrome installation/driver not found.')
        logging.info('Chrome installation/driver not found')
        return None


def UpdateProfile(driver):
    try:
        mob = "123456789" # Type your mobile number here
        mobName = "mobile"
        profeditXpath = "//a[contains(text(), ' Snapshot')]"
        saveXpath = "//button[@ type=\"submit\"][@value=\"Save Changes\"]"

        profElement = GetElement(driver, profeditXpath, locator='XPATH')
        profElement.click()
        driver.implicitly_wait(2)

        mobFieldElement = GetElement(driver, mobName, locator='NAME')
        mobFieldElement.clear()
        mobFieldElement.send_keys(mob)
        driver.implicitly_wait(2)

        saveFieldElement = GetElement(driver, saveXpath, locator='XPATH')
        saveFieldElement.send_keys(Keys.ENTER)
        driver.implicitly_wait(3)

        if is_element_present(driver, By.ID, "confirmMessage"):
            logging.info('Mob num Update Successful')
            print('Mob num Update Successful')
        else:
            logging.info('Mob num Update failed')
            print('Mob num Update failed')

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        lineNo = str(exc_tb.tb_lineno)
        logging.info('Error Updating Mob num: %s : %s at Line %s.\n' % (type(e), e, lineNo))
        print('Error Updating Mob num: %s : %s at Line %s.' % (type(e), e, lineNo))
        return None


def UploadResume(driver):
        try:
            uploadID = "uploadLink"
            attachCVID = "attachCV"
            saveXpath = "//button[@type='button']"
            CheckPointID = "attachCVMsg"

            driver.get('https://my.naukri.com/Profile/view')
            uploadElem = GetElement(driver, uploadID, locator='ID')
            uploadElem.click()

            AttachElement = GetElement(driver, attachCVID, locator='ID')
            AttachElement.send_keys(ResumePath)
            time.sleep(5)

            CheckPoint = GetElement(driver, CheckPointID, locator='ID')
            if 'success' in CheckPoint.text:
                print('Resume Document Upload Successful')
                logging.info('Resume Document Upload Successful')
            else:
                print('Resume Document Upload failed')
                logging.info('Resume Document Upload failed')

            saveElement = GetElement(driver, saveXpath, locator='XPATH')
            saveElement.click()

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            lineNo = str(exc_tb.tb_lineno)
            logging.info('Error while uploading Resume : %s : %s at Line %s.'% (type(e), e, lineNo))
            print('Error while uploading Resume : %s : %s at Line %s.' % (type(e), e, lineNo))
            pass

        time.sleep(2)

        try:
            typeCss = "a > strong"
            pasteID = "copyPaste"

            driver.get('https://my.naukri.com/Profile/view')
            uploadElem = GetElement(driver, uploadID, locator='ID')
            uploadElem.click()
            time.sleep(1)
            typeElement = GetElement(driver, typeCss, locator='CSS')
            typeElement.click()
            pasteElement = GetElement(driver, pasteID, locator='ID')
            pasteElement.clear()
            time.sleep(1)
            pasteElement.send_keys(u'''\n Add Your Resume Text Content \n''')

            saveElement = GetElement(driver, saveXpath, locator='XPATH')
            saveElement.click()
            time.sleep(1)
            driver.implicitly_wait(2)

            confirmID = "confirmMessage"
            CheckPoint = GetElement(driver, confirmID, locator='ID')
            if "Your naukri profile has been updated " in CheckPoint.text:
                print('Resume Text Update Successful')
                logging.info('Resume Text Update Successful')
            else:
                print('Resume Text Update failed')
                logging.info('Resume Text Update failed')

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            lineNo = str(exc_tb.tb_lineno)
            logging.info('Error while updating resume text : %s : %s at Line %s.'% (type(e), e, lineNo))
            print('Error while updating resume text: %s : %s at Line %s.' % (type(e), e, lineNo))
            pass


def main():
    logging.info('-----Naukri.qa.py Script Run Begin-----')
    try:
        driver = naukriLogin()
        if driver:
            UpdateProfile(driver)

            if os.path.exists(ResumePath):
                UploadResume(driver)
            else:
                print('Resume not found at %s ' % ResumePath)
                logging.info('Resume not found at %s ' % ResumePath)
        
            tearDown(driver)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        lineNo = str(exc_tb.tb_lineno)
        logging.info('Error Updating Naukri Profile: %s : %s at Line %s.'% (type(e), e, lineNo))
        print('Error Updating Naukri Profile: %s : %s at Line %s.' % (type(e), e, lineNo))

    logging.info('-----Naukri.qa.py Script Run Ended-----\n')


if __name__ == '__main__':
    main()
