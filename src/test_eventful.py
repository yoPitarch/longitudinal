import eventful
import pprint


oAuthKey = "7ebc34ffb193f0299b2a"
oAuthSecret = "7b1826e48cbeb399964b"
api = eventful.API('Lsd22Kqg2fhGr7Ld',)



# If you need to log in:
#api.login('yopitarch', 'delphine')

events = api.call('/events/search', date='Today', page_size=100, mature="secure", change_multi_day_start=True)
for event in events['events']['event']:
	#print(event.keys())
	print("[",event["title"],"]")
	if "url" in event :
		print("\turl =>", event["url"])
	if "venue_name" in event :
		print("\tvenue =>", event["venue_name"])
	print("\tFrom",event["start_time"], "to", event["stop_time"])
	for k in event :
		if k.endswith("_count"):
			print("\t"+k,"=>",event[k])
