import yaml,sys
from collections import defaultdict


def loadConfig(path) :
	with open(path, 'r') as stream:
		try:
			return yaml.load(stream)
		except yaml.YAMLError as exc:
			print(exc)
			sys.exit("[ERROR] Invalid configuration file!!")


def loadTracked(path) :
	s = set()
	info = {}
	with open(path,'r') as fin :
		for l in fin:
			tl = l.strip().split("\t")
			s.add(tl[1])
			info[tl[1]] =  {
				"name": tl[2],
				"dateStart": tl[0],
				"url": tl[3]
			}
	return s,info

def loadDone(path):
	s = set()
	with open(path,'r') as fin :
		for l in fin:
			s.add(l.strip())
	return s


def loadLatest(path, s) :
	d = defaultdict(int)
	for e in s :
		d[e] = 0

	with open(path,"r") as f :
		for l in f :
			tl = l.strip().split("\t")
			d[tl[0]] = int(tl[1])
	return d


def parseTweet(tw) :
	print("------------------------------------------------")
	print(tw)
	res = {}
	print(tw.text)
	id = tw.get_attribute("data-tweet-id")
	screenName = tw.get_attribute("data-screen-name")
	time = tw.find_element_by_class_name("js-relative-timestamp")
	ts = time.get_attribute("data-time")
	textElement = tw.find_element_by_class_name("tweet-text")
	txt = textElement.text.replace("\n", " ")
	links = textElement.find_elements_by_tag_name("a")

	llinks = []
	for link in links :
		if "hashtag" not in link.get_attribute("href") :
			llinks.append(link.get_attribute("href"))

	res = {
		"id":id,
		"screenName" : screenName,
		"time":ts,
		"text" : txt,
		"links":llinks
	}

	return res

def getTimeTweet(tw) :
	time = tw.find_element_by_class_name("js-relative-timestamp")
	ts = time.get_attribute("data-time")
	return int(ts)