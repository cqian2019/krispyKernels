
import urllib.request, json, ssl

ctxt = ssl._create_unverified_context()
#urlopen("url",context=ctxt) if you get ssl error

#---------------------TICKET MASTER API (Derek)-----------------------------
tmKey = "6OngVrLfArkcPfNuh9GwG3fgAf6HcfQr"
tmId = ""
tmUrl = "https://app.ticketmaster.com/discovery/v2/events.json?latlong={0},{1}&radius=50&segmentName=Music&apikey={2}"

#getEvents(location) returns a list of music events - each event is a dictionary with the event name, genre, date, venue, artist lineup, link/url to event page on ticketmaster, and address

#Example --> [ { 'name': 'Winter Concert', 'genre': 'Alt/Rock', 'date': '11/25/2018', 'venue': 'Stuyvesant High School', 'lineup': ['cheryl', 'derek'], 'url': 'ticketmaster.com/concert', 'address': '345 Chambers St'}, {dict2}, {dict3}..... ]

def getEvents(lat, long):
    newUrl = tmUrl.format(lat, long, tmKey)
    tmJson = urllib.request.urlopen(newUrl, context = ctxt)
    tmData = json.loads(tmJson.read())
    events = tmData["_embedded"]["events"]
    return events #list[ {dict1}, {dict2},.... ]

def getEvent(id):
    newUrl = "https://app.ticketmaster.com/discovery/v2/events/{0}.json?apikey={1}".format(id, tmKey)
    tmJson = urllib.request.urlopen(newUrl, context = ctxt)
    eventDic = json.loads(tmJson.read())
    return eventDic

def getId(event):
    return event["id"]

def getName(event):
    return event["name"] #str

def getDate(event):
    try:
        return event["dates"]["start"]["localDate"] #str
    except:
        return "Date not available"

def getVenue(event):
    try:
        return event["_embedded"]["venues"][0]["name"] #str
    except:
        return "Venue not available"

def getGenre(event):
    try:
        return event["classifications"][0]["genre"]["name"] #str
    except:
        return "Genre not specified"

def getLineup(event):
    lineup = []
    try:
        for attraction in event["_embedded"]["attractions"]:
            lineup.append(attraction["name"])
        return lineup #list[ 'artist1', 'artist2', .... ] #list[ 'artist1', 'artist2', .... ]
    except:
        return "No artists available"

def getUrl(event):
    try:
        return event["url"] #str
    except:
        return "URL not available"

def getAddress(event):
    try:
        info = event["_embedded"]["venues"][0]
        address = info["address"]["line1"] + ", " + info["city"]["name"] + ", " + info["state"]["stateCode"] + ", " + info["postalCode"]
        return address #str
    except:
        return "Address not available"

#---------------------PUBLIC TRANSIT API (Kendrick)-------------------------

#these methods return directions, start and end are geocodes/coordinates
#be sure to break each instruction/direction into a new line

#lines refers to subway lines/transit lines (like A,C,E,1,2,3)
def publicDir(start,end): #via public transit (fastest)
    ptUrl = "https://transit.api.here.com/v3/route.json?mode=fastest;publicTransport&combineChange=true&time=2018-11-23T12%1A-00%1A30&app_id=Sx2msD6eY6kgE7WWcgsZ&app_code=kaJCiwVgQgxN23qD2Rkaew"
    ptUrl += "&dep=" + start + "&arr=" + end
    #print(ptUrl)
    try:
        request=urllib.request.urlopen(ptUrl, context = ctxt)
        raw=request.read()
        jdict=json.loads(raw)
    except:
        return "No directions available"
    #print(jdict)
    route = {}
    directions = ""
    for step in jdict["Res"]["Connections"]["Connection"][0]["Sections"]["Sec"]:
        directions += "From "
        if "Addr" in step["Dep"]:
            directions += "START "
        elif "Stn" in step["Dep"]:
            directions += step["Dep"]["Stn"]["name"] + " "
        if step["Dep"]["Transport"]["mode"] == 20:
            directions += "walk " + str(step["Journey"]["distance"]) + ' meters to '
        else:
            directions += "take the " + step["Dep"]["Transport"]["name"] + " to "
        if "Addr" in step["Arr"]:
            directions += "END"
        elif "Stn" in step["Arr"]:
            directions += step["Arr"]["Stn"]["name"]
        directions += ". "
    route['directions'] = directions
    time = jdict["Res"]["Connections"]["Connection"][0]['duration']
    if 'H' in time:
        route['time'] = (int(time[2:4]) * 60) + int(time[5:7])
    else:
        route['time'] = int(time[2:4])
    lines = []
    for step in jdict["Res"]["Connections"]["Connection"][0]["Sections"]["Sec"]:
        if step["Dep"]["Transport"]["mode"] != 20:
            lines.append(step["Dep"]["Transport"]["name"])
    route['lines'] = lines
    #print(route)
    return route #returns {'directions': 'str', 'time': int, 'lines': ['str','str','str'] }

def drivingDir(start,end): #via driving (fastest)
    ptUrl = "https://route.api.here.com/routing/7.2/calculateroute.json?app_id=Sx2msD6eY6kgE7WWcgsZ&app_code=kaJCiwVgQgxN23qD2Rkaew&mode=fastest;car"
    ptUrl += "&waypoint0=geo!" + start + "&waypoint1=geo!" + end
    try:
        request=urllib.request.urlopen(ptUrl, context = ctxt)
        raw=request.read()
        jdict=json.loads(raw)
    except:
        return "No directions available"
    route = {}
    directions = ""
    for key in jdict['response']['route'][0]['leg'][0]['maneuver']:
        directions += key['instruction'] + " "
    route['time'] = jdict['response']['route'][0]['summary']['travelTime']
    route['distance'] = jdict['response']['route'][0]['summary']['distance']
    #print(route)
    dirList = directions.replace('>','<').split('<')
    directions = ""
    for string in dirList:
        if 'span' not in string:
            directions += string
    route['directions'] = directions
    return route #returns { 'directions': 'str', 'time': int, 'distance': 'int'}

def toGeo(address): #converts address to geocode/coordinates
    ptUrl = "https://geocoder.api.here.com/6.2/geocode.json?app_id=Sx2msD6eY6kgE7WWcgsZ&app_code=kaJCiwVgQgxN23qD2Rkaew&searchtext="
    address = address.replace(" ", "+")
    ptUrl += address
    request=urllib.request.urlopen(ptUrl, context = ctxt)
    raw=request.read()
    jdict=json.loads(raw)
    geocode=[]
    geocode.append(jdict["Response"]["View"][0]["Result"][0]["Location"]["DisplayPosition"]["Latitude"])
    geocode.append(jdict["Response"]["View"][0]["Result"][0]["Location"]["DisplayPosition"]["Longitude"])
    #print(geocode)
    return geocode

def suggest(address): #returns suggestions for a mistyped address
    ptUrl = "http://autocomplete.geocoder.api.here.com/6.2/suggest.json?app_id=Sx2msD6eY6kgE7WWcgsZ&app_code=kaJCiwVgQgxN23qD2Rkaew&beginHighlight=%3Cb%3E&endHighlight=%3C/b%3E&query="
    ptUrl += address.replace(" ", "+")
    #print(ptUrl)
    request=urllib.request.urlopen(ptUrl,context = ctxt)
    raw=request.read()
    jdict=json.loads(raw)
    suggestions = []
    for key in jdict['suggestions']:
        s = ""
        for step in key['address']:
            s += key['address'][step] + " "
        sList = s.replace('>','<').split('<')
        s = ""
        for string in sList:
            if 'b' not in string:
                s += string
        suggestions.append([s])
    #print(suggestions)
    return suggestions #list of suggestions --> ["str","str","str"]


#---------------------THE AUDIO DB API (Simon)------------------------------

adKey = "195003"
adUrl = ""

def getInfo(artist):
    retVal = "http://www.theaudiodb.com/api/v1/json/195003/search.php?s="
    retVal += artist
    readUrl = urllib.request.urlopen(retVal, context = ctxt)
    hiJson = json.loads(readUrl.read())
    info = {}
    try:
        info['bio'] = hiJson['artists'][0]['strBiographyEN']
        info['style'] = hiJson['artists'][0]['strStyle']
        info['genre'] = hiJson['artists'][0]['strGenre']
        info['id'] = hiJson['artists'][0]['idArtist']
        return info #dict of info { 'artist':'str', 'bio':'str', 'style':'str', 'genre':'str', 'id': int }
    except:
        info['bio'] = "Artist information not found."
        return info
        
def getAlbums(artist):
    name = artist.replace(" ", "+")
    url = "https://theaudiodb.com/api/v1/json/195003/searchalbum.php?s="
    url += name
    req = urllib.request.urlopen(url, context = ctxt)
    jdata = json.loads(req.read())
    albumList = []
    try:
        for a in jdata['album']:
            album = {}
            album['name'] = a['strAlbum']
        album['date'] = a['intYearReleased']
        album['id'] = a['idAlbum']
        albumList.append(album)
        return albumList
    except:
        return [""]

def getAlbumId(artist,album):#uses album name
    url = "https://theaudiodb.com/api/v1/json/195003/searchalbum.php?s={0}&a={1}".format(artist,album)
    req = urllib.request.urlopen(url, context=ctxt)
    jdata = json.loads(readUrl.read())
    id = jdata['idAlbum']
    return id

def getTracks(albumId):
    url = "https://theaudiodb.com/api/v1/json/195003/track.php?m=" + albumId
    req = urllib.request.urlopen(url, context=ctxt)
    jdata = json.loads(req.read())
    tracks=[]
    try:
        for t in jdata['track']:
            tracks.append(t['strTrack'])
        return tracks
    except:
        return [""]

def getMvs(artistId):
    url = "https://theaudiodb.com/api/v1/json/195003/mvid.php?i={0}".format(artistId)
    req = urllib.request.urlopen(url, context=ctxt)
    jdata = json.loads(req.read())
    tracks = []
    for t in jdata['mvids']:
        mv = {}
        mv['url'] = t['strMusicVid']
        mv['name'] = t['strTrack']
        tracks.append(mv)
    return tracks


#---------------------------DARK SKY API (Simon)---------------------------
dsKey = "284833a5391e29e9498e6f1adc9c656e"
dsUrl = ""

#returns weather with provided geocode and date
def weather(date,coor):
    return weather #str
