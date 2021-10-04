import urllib.request
from PIL import Image
import PIL

def getURLImage():

    local_filename = "static/images/css/img1.jpg"
    local_filename, headers = urllib.request.urlretrieve("https://192.168.200.1:8080/jpg?q=2")

    