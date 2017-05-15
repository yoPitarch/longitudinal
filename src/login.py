#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def correct_url(url):
	if not url.startswith("http://") and not url.startswith("https://"):
		url = "http://" + url
	return url


def scrollDown(browser, numberOfScrollDowns):
	body = browser.find_element_by_tag_name("body")
	while numberOfScrollDowns >= 0:
		body.send_keys(Keys.PAGE_DOWN)
		# time.sleep(1)
		numberOfScrollDowns -= 1
		if numberOfScrollDowns % 10 == 0:
			print('remaining scroll downs ... {}'.format(numberOfScrollDowns))
	return browser


def scrollDown2(driver):
	prior = 0
	while True:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		current = len(WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "u-linkComplex-target"))))
		print(current)
		if current == prior:
			return driver
		prior = current
		time.sleep(2)

def scrollDown3(browser):

	pause = 10

	lastHeight = browser.execute_script("return document.body.scrollHeight")
	print(lastHeight)
	i = 0
	browser.get_screenshot_as_file("test03_1_"+str(i)+".jpg")
	while True:
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(pause)
		newHeight = browser.execute_script("return document.body.scrollHeight")
		print (newHeight)
		if newHeight == lastHeight:
			return browser
		lastHeight = newHeight
		i += 1
		browser.get_screenshot_as_file("test03_1_"+str(i)+".jpg")



def crawl_url(url, run_headless=True):
	if run_headless:
		display = Display(visible=0, size=(1024, 768))
		display.start()

	url = correct_url(url)
	#browser = webdriver.PhantomJS("./phantomjs/bin/phantomjs")
	#browser = webdriver.Safari()
	browser = webdriver.Chrome("./phantomjs/bin/chromedriver")
	browser.get(url)

	username = browser.find_element_by_class_name("js-username-field")
	password = browser.find_element_by_class_name("js-password-field")

	username.send_keys("pitYo")
	time.sleep(1)
	password.send_keys("delphine")

	browser.find_element_by_css_selector("button.submit.btn.primary-btn").click()
	browser = scrollDown3(browser)


	target_set = set()

	all_targets = browser.find_elements_by_class_name("u-linkComplex-target")
	for a_target in all_targets:
		target_set.add(a_target.text)

	with open("followers.txt", "w") as f :
		for target in target_set:
			f.write(target + '\n')

	"""
	while True:
		target_set = set()

		browser = scrollDown(browser, 500)
		time.sleep(0.1)

		all_targets = browser.find_elements_by_class_name("u-linkComplex-target")
		for a_target in all_targets:
			target_set.add(a_target.text)

		fo = open('followers.txt', 'a')
		for target in target_set:
			fo.write(target + '\n')
		fo.close()

		print('wrote {} to file'.format(len(target_set)))
	"""



	browser.quit()


if __name__ == '__main__':
	url = "https://twitter.com/mixlamalice/followers/"
	crawl_url(url,False)
