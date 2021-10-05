import urllib.request
from datetime import datetime



def getURLImage(folder, img_name, img_iteration):

    #local_filename = "D:/OneDrive/Robotics/PycharmProjects/564-Automated-Robotic-Vision-Light-Configuration/B_R_Illumination/static/images/subfolder1/img.jpg"
    local_filename = "B_R_Illumination/static/images/" + folder + "/" + img_name + img_iteration + ".jpg" 
    img_url = "http://www.zoomify.com/assets/thumbnails/thmbExpressLg.jpg" #Only http requests work.
    urllib.request.urlretrieve(img_url, local_filename)



    
    