import time,sys, os
import utils
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.keys import  Keys
from selenium.webdriver.support.wait import WebDriverWait

if len(sys.argv) < 2 :
	sys.exit("Usage: python3 1_trends.py <config_file>")
else :
	d = utils.loadConfig(sys.argv[1])

pathPhantomjs = d["pathPhantomjs"]
pathEventToTrack = d["pathEventToTrack"]
pathLatestTweetPerEvent = d["pathLatestTweetPerEvent"]
pathDoneEvent = d["pathDoneEvent"]






tracked,info = utils.loadTracked(pathEventToTrack)
done = utils.loadDone(pathDoneEvent)



toScrap = tracked - done
latestTs = utils.loadLatest(pathLatestTweetPerEvent,toScrap)



for idEvent in toScrap :
	eventName = info[idEvent]["name"]
	url = info[idEvent]["url"]

	print(url)
	browser = webdriver.PhantomJS(pathPhantomjs,service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
	#browser = webdriver.Safari()
	browser.get(url)
	body = browser.find_element_by_tag_name("body")
	i = 0
	#browser.get_screenshot_as_file("test03_2_" + str(i) + ".jpg")
	while True:
		print("i", i)
		time.sleep(2)
		elemsCount = browser.execute_script("return document.querySelectorAll('.stream-items > li.stream-item').length")
		# print "c", elemsCount

		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		# element = WebDriverWait(browser, 20).until(
		#	EC.presence_of_element_located((By.XPATH,
		#		"//*[contains(@class,'GridTimeline-items')]/li[contains(@class,'stream-item')]["+str(elemsCount+1)+"]")))
		try:
			WebDriverWait(browser, 10).until(
				lambda x: x.find_element_by_xpath(
					"//*[contains(@class,'stream-items')]/li[contains(@class,'stream-item')][" + str(elemsCount + 1) + "]/div"))

			latest = browser.find_element_by_xpath("//*[contains(@class,'stream-items')]/li[contains(@class,'stream-item')][" + str(elemsCount + 1) + "]/div")
			tw = utils.getTimeTweet(latest)
			if tw < latestTs[idEvent] :
				break

		except:
			break

		i += 1





	divs = browser.find_elements_by_class_name("js-stream-tweet")
	for tw in divs :
		print(utils.parseTweet(tw))
	browser.quit()





	sys.exit()
