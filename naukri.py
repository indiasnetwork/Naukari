#Naukri Daily update
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest

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
		
	def tearDown(self):
		self.driver.quit()
		
if __name__ == '__main__':
	unittest.main()
