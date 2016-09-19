#Naukri Daily update
import time, re
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Option
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException

class Login(unittest.TestCase):
	def setUp(self):
		self.driver = webdriver.Chrome()
		self.driver.implicitly_wait(1)
		self.driver.get("https://login.naukri.com")

	def test_Login(self):
		driver = self.driver
		username = "email id" 				#Enter Your Email
		password = "*************"			#Enter Your Password
		mob = "987654321"				#Enter Phone Number
		
		emailID				= "emailTxt"
		passID				= "pwd1"
		loginbuttonName			= "Login"
		profXpath			= "//*[@id='colL']/div[2]/div[1]/a[1]"
		editXpath			= "//*[@id='rPanel']/div/div[1]/div[2]/h1/a"
		mobName				= "mobile"
		saveXpath			= ".//*[@id='rPanel']/div/div/form/div[5]/div/button"
		uploadNew                       = "uploadLink"
                attachXpath                     = '//*[@id="attachCV"]'
		cvID = "attachCV"
		emailFieldElement	= WebDriverWait(driver, 5).until(lambda driver: driver.find_element_by_id(emailID))
		passFieldElement	= WebDriverWait(driver, 5).until(lambda driver: driver.find_element_by_id(passID))
		loginButtonElement	= WebDriverWait(driver, 5).until(lambda driver: driver.find_element_by_name(loginbuttonName))
		
		emailFieldElement.clear()
		emailFieldElement.send_keys(username)
		passFieldElement.clear()
		passFieldElement.send_keys(password)
		loginButtonElement.send_keys(Keys.ENTER);
		
		profFieldElement = WebDriverWait(driver, 4).until(lambda driver: driver.find_element_by_xpath(profXpath))
		profFieldElement.send_keys(Keys.ENTER);
		self.driver.implicitly_wait(1)
		editFieldElement = WebDriverWait(driver, 4).until(lambda driver: driver.find_element_by_xpath(editXpath))
		editFieldElement.send_keys(Keys.ENTER);
		self.driver.implicitly_wait(1)
		
		mobFieldElement = WebDriverWait(driver, 4).until(lambda driver: driver.find_element_by_name(mobName))
		mobFieldElement.clear()
		mobFieldElement.send_keys(mob);
		self.driver.implicitly_wait(1)
		
		saveFieldElement = WebDriverWait(driver, 4).until(lambda driver: driver.find_element_by_xpath(saveXpath))
		saveFieldElement.send_keys(Keys.ENTER);
		self.driver.implicitly_wait(3)
		self.driver.find_element_by_id("uploadLink").click()
		for i in range(60):
			try:
			if self.is_element_present(By.ID, cvID): break
		except: pass
		time.sleep(1)
		else: self.fail("time out")
		driver.find_element_by_id(cvID).clear()
		time.sleep(1)
		#Update the Resume path
		driver.find_element_by_id(cvID).send_keys("C:\\Resume.pdf\\")
		time.sleep(2)
		driver.find_element_by_xpath("//button[@type='button']").click()
		time.sleep(1)
		self.driver.implicitly_wait(5)
		self.assertTrue(self.is_element_present(By.ID, "confirmMessage"))
		
		self.driver.implicitly_wait(3)
		
	def is_element_present(self, how, what):
		try: self.driver.find_element(by=how, value=what)
		except NoSuchElementException: return False
		return True
		
	def is_alert_present(self):
		try: self.driver.switch_to_alert()
		except NoAlertPresentException: return False
		return True
		
	def close_alert_and_get_its_text(self):
		try:
			alert = self.driver.switch_to_alert()
			alert_text = alert.text
			if self.accept_next_alert:
				alert.accept()
			else:
				alert.dismiss()
			return alert_text
	        finally: self.accept_next_alert = True
	        
	def tearDown(self):
		self.driver.close()
		self.driver.quit()
		
		
if __name__ == '__main__':
	unittest.main()

