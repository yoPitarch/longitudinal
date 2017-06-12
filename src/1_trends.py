import datetime, pathlib, yaml, sys
import utils
from collections import defaultdict
import urllib.request
import bs4


if len(sys.argv) < 2 :
	sys.exit("Usage: python3 1_trends.py <config_file>")
else :
	d = utils.loadConfig(sys.argv[1])

url = d["urlTrends"]
pathEvents = d["pathEventToTrack"]


r = urllib.request.urlopen(url)
soup = bs4.BeautifulSoup(r, "lxml")

trend_cards = soup.find_all("div",class_="trend-card")

latest = trend_cards[0]
previous = trend_cards[1:]


sNewest = set()
dTrends = defaultdict(lambda: "none url specified")

# Get the newest
unixTs  = float(latest.h5["data-timestamp"])

sEventRunning = set()

idEvent = 0
path = pathlib.Path(pathEvents)
if path.is_file() :
	with open(pathEvents) as f:
		for l in f :
			sEventRunning.add(l.split("\t")[2])
			idEvent += 1


ts = datetime.datetime.fromtimestamp(unixTs)
cleanDate = str(ts.day)+"-"+str(ts.month)+"-"+str(ts.year)+"_"+str(ts.hour)+":"+str(ts.minute)
for trend in latest.descendants :
	if trend.name == "a" and trend.text not in sEventRunning:
		sNewest.add(trend.text)
		dTrends[trend.text] = trend["href"]




# Check if trends has already previoulsy appeared
for trend_card in previous :
	for trend in trend_card.descendants :
		if trend.name == "a" :
			if trend.text in sNewest :
				sNewest.remove(trend.text)





# Est ce qu'il en reste ?
with open(pathEvents,"a") as fout :
	for trend in sNewest :
		fout.write(cleanDate+"\t"+str(idEvent)+"\t"+trend+"\t"+dTrends[trend].replace("http://twitter.com/search?q=","https://twitter.com/search?f=tweets&q=")+"\n")
		idEvent += 1

