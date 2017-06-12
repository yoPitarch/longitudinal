import datetime
from collections import defaultdict
import urllib.request
import bs4


url = "https://trends24.in/united-states/new-york/"
pathEvents = "../out/trends.txt"


r = urllib.request.urlopen(url)
soup = bs4.BeautifulSoup(r, "lxml")

trend_cards = soup.find_all("div",class_="trend-card")

latest = trend_cards[0]
previous = trend_cards[1:]


sNewest = set()
dTrends = defaultdict(lambda: "none url specified")

# Get the newest
unixTs  = float(latest.h5["data-timestamp"])

ts = datetime.datetime.fromtimestamp(unixTs)
cleanDate = str(ts.day)+"-"+str(ts.month)+"-"+str(ts.year)+"_"+str(ts.hour)+":"+str(ts.minute)
print(ts.month," ", ts.day, " ")
for trend in latest.descendants :
	if trend.name == "a":
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
		fout.write(cleanDate+"\t"+trend+"\t"+dTrends[trend]+"\n")

