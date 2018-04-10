import urllib
import requests
from io import StringIO
import image
import webbrowser
import requests
import json
import EZ_Cal

proxy = "127.0.0.1:8080"
proxies = {"http": proxy, "https": proxy}
sesion = requests.Session()
sesion.proxies = proxies

def get_dist_btw_act(filename_wo_extension, units, origin, dest):  
# assemble the URL
	origin = get_currloc()
	url2  =  "https://maps.googleapis.com/maps/api/distancematrix/json?" # base URL, append query params, separated by &
	url2 += "units="+units  #measurement type
	url2 += "&origins="+origin  #starting point
	url2 += "&destinations="+dest #destination
	url2 += "&key=AIzaSyBw_1vex3rpNM6E8ce09Cx_WBcSHebrcGE" #API Key
	response = urllib.urlopen(url2)
	data = json.loads(response.read())
	with open('data.json', 'w') as outfile:
    		json.dump(data['rows'], outfile)
	return data['rows'][0]


def get_currloc():
	send_url = 'http://freegeoip.net/json'
	r = requests.get(send_url)
	j = json.loads(r.text)
	lat = j['latitude']
	lon = j['longitude']
	currloc = str(lat)+","+str(lon)
	return currloc
	#x = raw_input("Enter Starting Point: ")
	#y = raw_input("Enter Ending Point: ")
	#webbrowser.open(get_dist_btw_act("test", units="imperial", origin=currloc, dest="15607 Hexham Terrace, Upper Marlboro, MD, 20774"))

def main():
	calendar_data = EZ_Cal.main()
	travel_time = get_dist_btw_act("test", "imperial", "blah", calendar_data.get('loc')[0])
	#webbrowser.open(url) #use to open in browser

	firstevent_traveldur = travel_time['elements'][0]
	all_data = firstevent_traveldur.copy()
	all_data.update(calendar_data)

	dist = all_data.get('distance')
	dur = all_data.get('loc')
	print(all_data)

if __name__ == '__main__':
    main()