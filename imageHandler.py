from distutils import errors
import encodings
from ftplib import FTP
import urllib.request
import os


def getURLImage(test_id, img_name, img_iteration):

    session = FTP("85.191.222.184")
    session.login("user", "user")
    session.cwd("/html/")
    if test_id not in session.nlst():
        session.mkd(test_id)
    session.cwd("/html/" + test_id)
    img_url = "http://192.168.200.1:8080/jpg?q=100"
    path, _ = urllib.request.urlretrieve(img_url, "tmpImage.jpg")

    file = open("tmpImage.jpg", 'rb')
    session.storbinary("STOR " + img_name + img_iteration + ".jpg", file)
    file.close()
    os.remove("tmpImage.jpg")
    session.quit()
