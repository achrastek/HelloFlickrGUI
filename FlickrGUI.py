from tkinter import *
import urllib.request
import requests
import json
import shutil
from PIL import Image

# A very simple application which searches Flickr for cat pictures and displays the first picture in a GUI
# Uses tkinter for the GUI
# Uses pillow ( a PIL fork ) to convert the jgp returned from Flickr to a GIF for tkinter


class Flickr(Frame):


    def __init__(self):

        Frame.__init__(self)
        self.grid()

        #Add a label to GUI
        self._label = Label(self, text="Here is a picture of a cat")
        self._label.grid()

        #Sample Flickr search URL build from
        #https://www.flickr.com/services/api/explore/flickr.photos.search
        #Search for cat pictures, modify to search for whatever tag you want
        flickerSearchURL = 'https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=ef7824dd34a32463d9e68c038579525e&text=cat&format=json&nojsoncallback=1'

        #Search flickr for cat pictures
        flickrResponse = urllib.request.urlopen(flickerSearchURL)
        #get json back
        flickrResponseJSONString = flickrResponse.read().decode('UTF-8')
        flickrResponseJson = json.loads(flickrResponseJSONString)
        #Get first json object ('photos') which contains another json object ('photo') which is an json array; each
        # element represents one photo. Take element 1
        firstResponsePhoto = flickrResponseJson['photos']['photo'][0]
        #Extract thwe secret, server, id and farm; which you need to construct another URL to request a specific photo
        #https://farm{farm-id}.staticflickr.com/{server-id}/{id}_{secret}.jpg

        secret = firstResponsePhoto['secret']
        id = firstResponsePhoto['id']
        server = firstResponsePhoto['server']
        farm = firstResponsePhoto['farm']

        print(firstResponsePhoto)  #Just checking we get the JSON we expect
        #TODO add error handing

        fetchPhotoURL = 'https://farm%s.staticflickr.com/%s/%s_%s_m.jpg' % (farm, server, id, secret)
        print(fetchPhotoURL)   #Again, just checking

        #Reference: http://stackoverflow.com/questions/13137817/how-to-download-image-using-requests

        catPicFileName = 'cat.jpg'
        catPicFileGif = 'cat.gif'

        #Read the response and save it as a .jpg. Use shutil to copy the stream of bytes into a file
        #What does 'with' mean? http://preshing.com/20110920/the-python-with-statement-by-example/
        resp = requests.get(fetchPhotoURL, stream=True)
        with open(catPicFileName, 'wb') as out_file:
            shutil.copyfileobj(resp.raw, out_file)
        del resp


        #Flickr returns a jpg. Tkinter displays gif. Use pillow to convert the JPG to GIF
        #Reference https://pillow.readthedocs.org/handbook/tutorial.html

        Image.open(catPicFileName).save(catPicFileGif)

        #Add PictureImage to GUI
        self._catPic = PhotoImage(file=catPicFileGif)
        self._catPicLabel = Label(self, image=self._catPic)
        self._catPicLabel.grid()


    #Fetches weather from openweatherapi, extracts temp from json
    #not used at all in this application but I wrote this to practice fetching data from an API.
    def getWeather(self):

        #Example 2 - fetch JSON from openweathermap
        weatherurl = 'http://api.openweathermap.org/data/2.5/weather?q=London,uk'
        #Make request, get response
        weatherResponse = urllib.request.urlopen(weatherurl)
        #Read response into JSON string

        wresponseJson = weatherResponse.read().decode('utf-8')
        #Reference http://stackoverflow.com/questions/23049767/parsing-http-response-in-python

        print(wresponseJson)
        #Load JSON string into JSON parser - now can be used in a dictionary-like way
        parsed_json = json.loads(wresponseJson)
        #Reference http://docs.python-guide.org/en/latest/scenarios/json/
        #What's the temp in London?

        tempInKelvin = parsed_json['main']['temp']
        tempInCelcius = int(tempInKelvin) - 273
        print(tempInCelcius)


def main():

    Flickr().mainloop()

main()