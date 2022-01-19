from distutils import errors
import encodings
from ftplib import FTP
from multiprocessing.connection import wait
import urllib.request
import os
import time
import OPCUA
#from PIL import Image
from exif import Image

def getURLImage(test_id, img_name, img_iteration, OPCUA_client):
    attempts = 0
    while attempts < 3:
        try:
            session = FTP("85.191.222.184")
            session.login("user", "user")
            session.cwd("/html/")
            if test_id not in session.nlst():
                session.mkd(test_id)
            session.cwd("/html/" + test_id)
            img_url = "http://192.168.200.1:8080/jpg?q=100"
            #img_url = "http://85.191.222.184/Peter/cam.jpg"
            #img_url = "http://www.zoomify.com/assets/thumbnails/thmbExpressLg.jpg"
            path, _ = urllib.request.urlretrieve(img_url, "tmpImage.jpg")
            OPCUA.readValue(OPCUA_client, "hw.in.nettime")
            with open('tmpImage.jpg', 'rb') as image_file:
                    my_image = Image(image_file)
            print(my_image.has_exif)
            file = open("tmpImage.jpg", 'rb')
            session.storbinary("STOR " + img_name + img_iteration + ".jpg", file)
            file.close()
            os.remove("tmpImage.jpg")
            session.quit()
            break
        except Exception as e:
            print(e)
            time.sleep(0.1)
            attempts += 1
