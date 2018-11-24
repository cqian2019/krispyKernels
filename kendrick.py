import urllib.request, requests, json, ssl

ctxt = ssl._create_unverified_context()
#urlopen("url",context=ctxt) if you get ssl error
#---------------------PUBLIC TRANSIT API (Kendrick)-------------------------

#these methods return directions, start and end are geocodes/coordinates
#be sure to break each instruction/direction into a new line

#lines refers to subway lines/transit lines (like A,C,E,1,2,3)
def publicDir(start,end): #via public transit (fastest)
    ptUrl = "https://transit.api.here.com/v3/route.json?mode=fastest;publicTransport&combineChange=true&time=2018-11-23T12%1A-00%1A30&app_id=Sx2msD6eY6kgE7WWcgsZ&app_code=kaJCiwVgQgxN23qD2Rkaew"
    ptUrl += "&dep=" + start + "&arr=" + end
    print(ptUrl)
    request=urllib.request.urlopen(ptUrl)
    raw=request.read()
    jdict=json.loads(raw)
    print(jdict)
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
    print(route)
    return route #returns {'directions': 'str', 'time': int, 'lines': ['str','str','str'] }

def drivingDir(start,end): #via driving (fastest)
    ptUrl = "https://route.api.here.com/routing/7.2/calculateroute.json?app_id=Sx2msD6eY6kgE7WWcgsZ&app_code=kaJCiwVgQgxN23qD2Rkaew&mode=fastest;car"
    ptUrl += "&waypoint0=geo!" + start + "&waypoint1=geo!" + end
    request=urllib.request.urlopen(ptUrl)
    raw=request.read()
    jdict=json.loads(raw)
    route = {}
    directions = ""
    for key in jdict['response']['route'][0]['leg'][0]['maneuver']:
        directions += key['instruction']
    route['directions'] = directions
    route['time'] = jdict['response']['route'][0]['summary']['travelTime']
    route['distance'] = jdict['response']['route'][0]['summary']['distance']
    print(route)
    return route #returns { 'directions': 'str', 'time': int, 'distance': 'int'}

def toGeo(address): #converts address to geocode/coordinates
    ptUrl = "https://geocoder.api.here.com/6.2/geocode.json?app_id=Sx2msD6eY6kgE7WWcgsZ&app_code=kaJCiwVgQgxN23qD2Rkaew&searchtext="
    address = address.replace(" ", "+")
    ptUrl += address
    request=urllib.request.urlopen(ptUrl)
    raw=request.read()
    jdict=json.loads(raw)
    geocode = "" + str(jdict["Response"]["View"][0]["Result"][0]["Location"]["DisplayPosition"]["Latitude"]) + "," + str(jdict["Response"]["View"][0]["Result"][0]["Location"]["DisplayPosition"]["Longitude"])
    print(geocode)
    return geocode

def suggest(address): #returns suggestions for a mistyped address
    ptUrl = "http://autocomplete.geocoder.api.here.com/6.2/suggest.json?app_id=Sx2msD6eY6kgE7WWcgsZ&app_code=kaJCiwVgQgxN23qD2Rkaew&beginHighlight=%3Cb%3E&endHighlight=%3C/b%3E&query="
    ptUrl += address.replace(" ", "+")
    print(ptUrl)
    request=urllib.request.urlopen(ptUrl)
    raw=request.read()
    jdict=json.loads(raw)
    suggestions = []
    for key in jdict['suggestions']:
        s = ""
        for step in key['address']:
            s += key['address'][step] + " "
        suggestions.append([s])
    print(suggestions)
    return suggestions #list of suggestions --> ["str","str","str"]

publicDir("40.613521,-73.99830299999996","40.7173116,-74.0144598")
drivingDir("40.613521,-73.99830299999996","40.7173116,-74.0144598")
toGeo("1734 76th Street Brooklyn NY")
suggest("Uk Ye 7")
