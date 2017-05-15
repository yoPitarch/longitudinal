from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from selenium.webdriver.support.wait import WebDriverWait


def loadFullPage(driver):
	prior = 0
	while True:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		current = len(WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ProfileCard-screennameLink"))))
		print(current)
		if current == prior:
			return current
		prior = current


driver = webdriver.PhantomJS("./phantomjs/bin/phantomjs")
driver.get("https://twitter.com/mixlamalice/followers?lang=en")

loadFullPage(driver)


print("ici")
