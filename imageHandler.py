import urllib.request
from datetime import datetime
import os


def getURLImage(folder, img_name, img_iteration):
    local_filename = "static/images/" + \
        folder + "/" + img_name + img_iteration + ".jpg"
    img_url = "http://192.168.200.1:8080/jpg?q=100"  # Only http requests work.
    if os.path.exists("static/images/" + folder):
        urllib.request.urlretrieve(img_url, local_filename)
    else:
        os.makedirs("static/images/" + folder)
        urllib.request.urlretrieve(img_url, local_filename)
