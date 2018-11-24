import urllib.request, json, ssl

ctxt = ssl._create_unverified_context()
#urlopen("url",context=ctxt) if you get ssl error

#---------------------THE AUDIO DB API (Simon)------------------------------

adKey = "195003"
adUrl = ""

def info(artist):
    retVal = "theaudiodb.com/api/v1/json/195003/search.php?s="
    #retstr += artist
    retVal += "coldplay"
    return retstr #dict of info { 'artist':'str', 'bio':'str', 'style':'str', 'genre':'str', 'id': int }

def albums(artist):#uses artist id
    retVal = "https://theaudiodb.com/api/v1/json/195003/album.php?i="
    #retstr += artist
    retVal += "111239"
    return retVal #dict --> [{'name':'str', 'date':'str', 'id':int}, {dict1}, {dict2}]

def tracks(album):#uses album id
    retVal = "https://theaudiodb.com/api/v1/json/195003/track.php?m="
    # retVal += album
    retVal += 2205903
    return retVal #list --> ['track1','track2','track3']

#---------------------------DARK SKY API (Simon)---------------------------
dsKey = "284833a5391e29e9498e6f1adc9c656e"
dsUrl = ""

#returns weather with provided geocode and date
def weather(date,coor):
    retVal = "https://api.darksky.net/forecast/284833a5391e29e9498e6f1adc9c656e/37.8267,-122.4233"
    coor = 
    return weather #str
