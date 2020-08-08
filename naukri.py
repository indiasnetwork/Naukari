#! python3
# -*- coding: utf-8 -*-
"""Naukri Daily update - Using Chrome"""
import re
import os
import sys
import time
import logging
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from PyPDF2 import PdfFileReader, PdfFileWriter
import random,string,io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from webdriver_manager.chrome import ChromeDriverManager

# Add folder Path of your resume
originalResumePath = "original_resume.pdf"
# Add Path where modified resume should be saved
modifiedResumePath = "modified_resume.pdf"

# Update your naukri username and password here before running
username = "Type Your email ID Here"
password = "Type Your Password Here"
mob = "1234567890" # Type your mobile number here

# ----- No other changes required ----- 

# Set login URL
NaukriURL = "https://login.naukri.com/nLogin/Login.php"

log_file_path = "naukri.log"
logging.basicConfig(level=logging.INFO,
                    filename=log_file_path,
                    format='%(asctime)s    : %(message)s')
# logging.disable(logging.CRITICAL)
os.environ['WDM_LOG_LEVEL'] = '0'


def log_msg(message):
    """Print to console and store to Log"""
    print(message)
    logging.info(message)


def catch(error):
    """Method to catch errors and log error details"""
    exc_type, exc_obj, exc_tb = sys.exc_info()
    lineNo = str(exc_tb.tb_lineno)
    msg = '%s : %s at Line %s.' % (type(error), error, lineNo)
    print(msg)
    logging.error(msg)


def GetElement(driver, elementTag, locator='ID'):
    """Wait max 15 secs for element and then select when it is available"""
    try:
        if locator == 'ID':
            if is_element_present(driver, By.ID, elementTag):
                return WebDriverWait(driver, 15).until(lambda driver: driver.find_element_by_id(elementTag))
            else:
                log_msg('%s Not Found.' % elementTag)
                return None

        elif locator == 'NAME':
            if is_element_present(driver, By.NAME, elementTag):
                return WebDriverWait(driver, 15).until(lambda driver: driver.find_element_by_name(elementTag))
            else:
                log_msg('%s Not Found.' % elementTag)
                return None

        elif locator == 'XPATH':
            if is_element_present(driver, By.XPATH, elementTag):
                return WebDriverWait(driver, 15).until(lambda driver: driver.find_element_by_xpath(elementTag))
            else:
                log_msg('%s Not Found.' % elementTag)
                return None

        elif locator == 'CSS':
            if is_element_present(driver, By.CSS_SELECTOR, elementTag):
                return WebDriverWait(driver, 15).until(lambda driver: driver.find_element_by_css_selector(elementTag))
            else:
                log_msg('%s Not Found.' % elementTag)
                return None

    except Exception as e:
        catch(e)
    return None


def is_element_present(driver, how, what):
    """Returns True if element is present"""
    try:
        driver.find_element(by=how, value=what)
    except NoSuchElementException:
        return False
    return True


def WaitTillElementPresent(driver, elementTag, locator='ID', timeout=30):
    """Wait till element present. Default 30 seconds"""
    result = False
    driver.implicitly_wait(0)
    for i in range(timeout):
        try:
            if locator == 'ID':
                if is_element_present(driver, By.ID, elementTag):
                    result = True
                    break
            elif locator == 'NAME':
                if is_element_present(driver, By.NAME, elementTag):
                    result = True
                    break
            elif locator == 'XPATH':
                if is_element_present(driver, By.XPATH, elementTag):
                    result = True
                    break
            elif locator == 'CSS':
                if is_element_present(driver, By.CSS_SELECTORS, elementTag):
                    result = True
                    break
        except Exception as e:
            log_msg('Exception when WaitTillElementPresent : %s' % e)
            pass
        time.sleep(0.99)
    else:
        log_msg("Timed out. Element not found: %s" % elementTag)
    driver.implicitly_wait(3)
    return result


def tearDown(driver):
    try:
        driver.close()
        log_msg('Driver Closed Successfully')
    except Exception as e:
        catch(e)
        pass

    try:
        driver.quit()
        log_msg('Driver Quit Successfully')
    except Exception as e:
        catch(e)
        pass


def naukriLogin():
    """ Open Chrome browser and Login to Naukri.com"""
    status = False
    driver = None
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")       # ("--kiosk") for MAC
    options.add_argument("--disable-popups")
    options.add_argument("--disable-gpu")

    try:
        # updated to use ChromeDriverManager to match correct chromedriver automatically
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
        log_msg("Google Chrome Launched!")

        driver.implicitly_wait(3)
        driver.get(NaukriURL)
        
        if 'naukri' in driver.title.lower():
            log_msg("Website Loaded Successfully.")

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
            log_msg('None of the elements found to login.')

        if emailFieldElement is not None:
            emailFieldElement.clear()
            emailFieldElement.send_keys(username)
            passFieldElement.clear()
            passFieldElement.send_keys(password)
            time.sleep(1)
            loginButton.send_keys(Keys.ENTER)

            # Added click to Skip button
            print('Checking Skip button')
            if WaitTillElementPresent(driver, "//*[text() = 'SKIP AND CONTINUE']", locator='XPATH', timeout=10):
                GetElement(driver, "//*[text() = 'SKIP AND CONTINUE']", locator='XPATH').click()

            # CheckPoint to verify login
            if WaitTillElementPresent(driver, 'search-jobs', locator='ID', timeout=40):
                CheckPoint = GetElement(driver, 'search-jobs', locator='ID')
                if CheckPoint:
                    log_msg('Naukri Login Successful')
                    status = True
                    return (status, driver)
                else:
                    log_msg('Unknown Login Error')
                    return (status, driver)

    except Exception as e:
        catch(e)
    return (status, driver)


def UpdateProfile(driver):
    try:
        mobXpath = "//*[@name='mobile'] | //*[@id='mob_number']"
        profeditXpath = "//a[contains(text(), 'UPDATE PROFILE')] | //a[contains(text(), ' Snapshot')] | //a[contains(@href, 'profile') and contains(@href, 'home')]"
        saveXpath = "//button[@ type='submit'][@value='Save Changes'] | //*[@id='saveBasicDetailsBtn']"
        editXpath = "//em[text()='Edit']"

        WaitTillElementPresent(driver, profeditXpath, locator='XPATH', timeout=20)
        profElement = GetElement(driver, profeditXpath, locator='XPATH')
        profElement.click()
        driver.implicitly_wait(2)
        
        WaitTillElementPresent(driver, editXpath + " | " + saveXpath, locator='XPATH', timeout=20)
        if is_element_present(driver, By.XPATH, editXpath):
            editElement = GetElement(driver, editXpath, locator='XPATH')
            editElement.click()
            
            WaitTillElementPresent(driver, mobXpath, locator='XPATH', timeout=20)
            mobFieldElement = GetElement(driver, mobXpath, locator='XPATH')
            mobFieldElement.clear()
            mobFieldElement.send_keys(mob)
            driver.implicitly_wait(2)

            saveFieldElement = GetElement(driver, saveXpath, locator='XPATH')
            saveFieldElement.send_keys(Keys.ENTER)
            driver.implicitly_wait(3)
            
            WaitTillElementPresent(driver, "//*[text()='today']", locator='XPATH', timeout=10)
            if is_element_present(driver, By.XPATH, "//*[text()='today']"):
                log_msg('Profile Update Successful')
            else:
                log_msg('Profile Update Failed')

        elif is_element_present(driver, By.XPATH, saveXpath):
            mobFieldElement = GetElement(driver, mobXpath, locator='XPATH')
            mobFieldElement.clear()
            mobFieldElement.send_keys(mob)
            driver.implicitly_wait(2)

            saveFieldElement = GetElement(driver, saveXpath, locator='XPATH')
            saveFieldElement.send_keys(Keys.ENTER)
            driver.implicitly_wait(3)

            WaitTillElementPresent(driver, "confirmMessage", locator='ID', timeout=10)
            if is_element_present(driver, By.ID, "confirmMessage"):
                log_msg('Profile Update Successful')
            else:
                log_msg('Profile Update Failed')

        time.sleep(5)

    except Exception as e:
        catch(e)


def UpdateResume():
    try:
        #random text with with random location and size
        txt = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(1,10)))
        xloc = random.randint(700,1000) #this ensures that text is 'out of page'
        fsize = random.randint(1,10)

        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("Helvetica", fsize) 
        can.drawString(xloc, 100, "lon")
        can.save()

        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        existing_pdf = PdfFileReader(open(originalResumePath, "rb"))
        pagecount = existing_pdf.getNumPages()
        print('Found %s pages in PDF' % pagecount)

        output = PdfFileWriter()
        # Merging new pdf with last page of my existing pdf
        # Updated to get last page for pdf files with varying page count
        for pageNum in range(pagecount-1):
            output.addPage(existing_pdf.getPage(pageNum))

        page = existing_pdf.getPage(pagecount-1)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        # save the new resume file
        with open(modifiedResumePath, "wb") as outputStream:
            output.write(outputStream)
        print('Saved modified PDF : %s' % modifiedResumePath)
        return os.path.abspath(modifiedResumePath)
    except Exception as e:
        catch(e)
    return os.path.abspath(originalResumePath)
    


def UploadResume(driver, resumePath):
    try:
        attachCVID = "attachCV"
        CheckPointID = "attachCVMsgBox"
        saveXpath = "//button[@type='button']"

        driver.get('https://www.naukri.com/mnjuser/profile')
        WaitTillElementPresent(driver, attachCVID, locator='ID', timeout=10)
        AttachElement = GetElement(driver, attachCVID, locator='ID')
        AttachElement.send_keys(resumePath)

        WaitTillElementPresent(driver, CheckPointID, locator='ID', timeout=30)
        CheckPoint = GetElement(driver, CheckPointID, locator='ID')
        if CheckPoint and 'success' in CheckPoint.text.lower():
            log_msg('Resume Document Upload Successful')
        else:
            log_msg('Resume Document Upload failed')

        if WaitTillElementPresent(driver, saveXpath, locator='ID', timeout=5):
            saveElement = GetElement(driver, saveXpath, locator='XPATH')
            saveElement.click()

    except Exception as e:
        catch(e)
    time.sleep(2)


def main():
    log_msg('-----Naukri.py Script Run Begin-----')
    driver = None
    try:
        status, driver = naukriLogin()
        if status:
            UpdateProfile(driver)
            if os.path.exists(originalResumePath):
                resumePath = UpdateResume()
                UploadResume(driver, resumePath)
            else:
                log_msg('Resume not found at %s ' % originalResumePath)

    except Exception as e:
        catch(e)

    finally:
        tearDown(driver)

    log_msg('-----Naukri.py Script Run Ended-----\n')


if __name__ == '__main__':
    main()
