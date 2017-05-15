#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import platform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time,sys


browser = ""

def correct_url(url):
	if not url.startswith("http://") and not url.startswith("https://"):
		url = "http://" + url
	return url




def scrollDown():

	global browser

	print(browser.title)

	i = 0

	#sys.exit()
	while True:
		print("i", i)
		elemsCount = browser.execute_script("return document.querySelectorAll('.ProfileCard-screennameLink').length")
		print("c", elemsCount)

		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(1)
		elemsCount = browser.execute_script("return document.querySelectorAll('.ProfileCard-screennameLink').length")
		print("c (new)", elemsCount)

		# element = WebDriverWait(browser, 20).until(
		#	EC.presence_of_element_located((By.XPATH,
		#		"//*[contains(@class,'GridTimeline-items')]/li[contains(@class,'stream-item')]["+str(elemsCount+1)+"]")))
		try:
			WebDriverWait(browser, 20).until(
				lambda x: x.find_element_by_xpath(
					"//*[contains(@class,'ProfileCard-screennameLink')][" + str(
						elemsCount + 1) + "]"))
		except:
			break

		i += 1
		browser.get_screenshot_as_file("test03_2_" + str(i) + ".jpg")



def crawl_url(url, run_headless=True):

	global browser

	if run_headless:
		display = Display(visible=0, size=(1024, 768))
		display.start()

	url = correct_url(url)
	browser = webdriver.PhantomJS(PHANTOMJS_PATH)
	browser.set_window_size(1024, 768)
	#browser = webdriver.Safari()
	#browser = webdriver.Chrome("./phantomjs/bin/chromedriver")
	browser.get(url)

	username = browser.find_element_by_class_name("js-username-field")
	password = browser.find_element_by_class_name("js-password-field")

	username.send_keys("pitYo")
	time.sleep(1)
	password.send_keys("delphine")

	browser.find_element_by_css_selector("button.submit.btn.primary-btn").click()
	scrollDown()


	target_set = set()

	all_targets = browser.find_elements_by_class_name("ProfileCard-screennameLink")
	for a_target in all_targets:
		target_set.add(a_target.text)

	with open("followers.txt", "w") as f :
		for target in target_set:
			f.write(target + '\n')


	browser.quit()


if __name__ == '__main__':

	if platform.system() == "Darwin" :
		PHANTOMJS_PATH = "./phantomjs/bin/phantomjs"
	else :
		PHANTOMJS_PATH = "./phantomjs/bin/phantomjs_linux_198"

	url = "https://twitter.com/mixlamalice/followers/"
	crawl_url(url,run_headless=False)
