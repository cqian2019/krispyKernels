
import urllib.request, json, ssl

ctxt = ssl._create_unverified_context()
#urlopen("url",context=ctxt) if you get ssl error

#---------------------TICKET MASTER API (Derek)-----------------------------

tmKey = ""
tmId = ""
tmUrl = ""

#getEvents(location) returns a list of music events - each event is a dictionary with the event name, genre, date, venue, artist lineup, link/url to event page on ticketmaster, and address

#Example --> [ { 'name': 'Winter Concert', 'genre': 'Alt/Rock', 'date': '11/25/2018', 'venue': 'Stuyvesant High School', 'lineup': ['cheryl', 'derek'], 'url': 'ticketmaster.com/concert', 'address': '345 Chambers St'}, {dict2}, {dict3}..... ]

def getEvents(location):
    return events #list[ {dict1}, {dict2},.... ]

def getName(event):
    return name #str

def getDate(event):
    return date #str

def getVenue(event):
    return venue #str

def getGenre(event):
    return genre #str

def getLineup(event):
    return lineup #list[ 'artist1', 'artist2', .... ]

def getUrl(event):
    return url #str

def getAddress(event):
    return address #str




#---------------------PUBLIC TRANSIT API (Kendrick)-------------------------

ptKey = ""
ptId = ""
ptUrl = "" 

#these methods return directions, start and end are geocodes/coordinates
#be sure to break each instruction/direction into a new line

#lines refers to subway lines/transit lines (like A,C,E,1,2,3)
def publicDir(start,end): #via public transit (fastest)
    return route #returns {'directions': 'str', 'time': int, 'lines': ['str','str','str'] }

def drivingDir(start,end): #via driving (fastest)
    return route #returns { 'directions': 'str', 'time': int, 'distance': 'int'}

def toGeo(address): #converts address to geocode/coordinates
    return geocode

def suggest(address): #returns suggestions for a mistyped address
    return suggestions #list of suggestions --> ["str","str","str"]


#---------------------THE AUDIO DB API (Simon)------------------------------

adKey = "195003"
adUrl = ""

def info(artist):
    return info #dict of info { 'artist':'str', 'bio':'str', 'style':'str', 'genre':'str', 'id': int }

def albums(artist):#uses artist id
    return albums #dict --> [{'name':'str', 'date':'str', 'id':int}, {dict1}, {dict2}]

def tracks(album):#uses album id
    return tracks #list --> ['track1','track2','track3']

#---------------------------DARK SKY API (Simon)---------------------------
dsKey = ""
dsUrl = ""

#returns weather with provided geocode and date
def weather(date,coor):
    return weather #str
