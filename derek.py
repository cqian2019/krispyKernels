import urllib.request, json, ssl

ctxt = ssl._create_unverified_context()
#urlopen("url",context=ctxt) if you get ssl error

#---------------------TICKET MASTER API (Derek)-----------------------------

tmKey = "6OngVrLfArkcPfNuh9GwG3fgAf6HcfQr"
tmId = ""
tmUrl = "https://app.ticketmaster.com/discovery/v2/events.json?latlong={0},{1}&segmentName=Music&apikey={2}"

#getEvents(location) returns a list of music events - each event is a dictionary with the event name, genre, date, venue, artist lineup, link/url to event page on ticketmaster, and address

#Example --> [ { 'name': 'Winter Concert', 'genre': 'Alt/Rock', 'date': '11/25/2018', 'venue': 'Stuyvesant High School', 'lineup': ['cheryl', 'derek'], 'url': 'ticketmaster.com/concert', 'address': '345 Chambers St'}, {dict2}, {dict3}..... ]

def getEvents(lat, long):
    newUrl = tmUrl.format(lat, long, tmKey)
    tmJson = urllib.request.urlopen(newUrl)
    tmData = json.loads(tmJson.read())
    events = tmData["_embedded"]["events"]
    return events #list[ {dict1}, {dict2},.... ]

def getName(event):
    return event["name"] #str

def getDate(event):
    return event["dates"]["start"]["localDate"] #str

def getVenue(event):
    return event["_embedded"]["venues"][0]["name"] #str

def getGenre(event):
    return event["classifications"][0]["genre"]["name"] #str

def getLineup(event):
    lineup = []
    for attraction in event["_embedded"]["attractions"]:
        lineup.append(attraction["name"])
    return lineup #list[ 'artist1', 'artist2', .... ]

def getUrl(event):
    return event["url"] #str

def getAddress(event):
    info = event["_embedded"]["venues"][0]
    address = info["address"]["line1"] + ", " + info["city"]["name"] + ", " + info["state"]["stateCode"] + ", " + info["postalCode"]
    return address #str

events = getEvents(40.737976, -73.880127)

print(getName(events[0]))
print(getDate(events[0]))
print(getVenue(events[0]))
print(getGenre(events[0]))
print(getLineup(events[0]))
print(getUrl(events[0]))
print(getAddress(events[0]))
