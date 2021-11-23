"""
Routes and views for the flask application.
"""

from datetime import datetime
from os import error
from flask import render_template, request, jsonify, json
from B_R_Illumination import app
import BRClient as BR
import folderHandler as fh
import imageHandler as ih
import rosbridge as rb
#import roboDK as rDK

response = ""
folders = []
images =[]
test_state = False
run = [True] # Used for stopping the RoboDK threads.We can simulate them using a list, since pointers do not exist in python.

@app.route('/process', methods=['POST'])
def process():
    global x_newvalue, y_newvalue, z_newvalue, slide_value, response, i, run, test_state
    error_msg = ""
    error_state = False

    rb.startROS_Connect()
    
    try:
        camera = request.form['camera']
        print("Camera = " + camera)
    except:
        camera = "off"
        print("Camera = " + camera)

    try:
        barlight1 = request.form['barlight1']
        print("Lightbar = " + barlight1)
    except:
        barlight1 = "off"
        print("Lightbar = " + barlight1)
    
    try:
        backlight = request.form['backlight']
        print("Backlight = " + backlight)
    except:
        backlight = "off"
        print("Backlight = " + backlight)

    if backlight == "on" or barlight1 == "on" or camera == "on":
        try:
            lightColor = request.form['lightradio']
            print("The light color = " + lightColor)
        except:
            if backlight != "off":
                error_msg = error_msg + " No color have been chosen for the light. \n"
    else:
        lightColor = "off"
        print("The color = " + lightColor)

    try:
        obj_width = request.form['obj_width']
        obj_length = request.form['obj_length']
        obj_height = request.form['obj_height']
        print("Object width = " + obj_width + "  Object length = " + obj_length + "  Object height = " + obj_height)
    except:
        obj_height = None
        obj_length = None
        obj_width = None
    
    if obj_height.isdigit():
        print("Value is all good.")
    else:
        error_msg = error_msg + " Height contains invalid charachters or is empty. \n"
    if obj_length.isdigit():
        print("Value is all good.")
    else:
        error_msg = error_msg + " Length contains invalid charachters or is empty. \n"
    if obj_width.isdigit():
        print("Value is all good.")
    else:
        error_msg = error_msg + " Width contains invalid charachters or is empty. \n"
    
    try:
        img_amount = request.form['img_amount']
        print("Image amount = " + img_amount)
    except:
        img_amount = None
    
    if img_amount.isdigit():
        print("Value is all good.")
    else:
        error_msg = error_msg + " Image amount contains invalid charachters or is empty. \n"
    
    #rb.startROS_Connect()
    #response = BR.connect()
    #ih.getURLImage("subfolder1", "img", str(i))
    if error_msg =="" and test_state == False:
        print("No errors")
        response = "Successfully started the test"
        error_state = False
        test_state = True
    elif test_state:
        response = "Test is already running."
        error_state = True
    else:
        response = error_msg
        error_state = True
    return jsonify({'output' : response, 'error_state' : error_state})

#Normal route for returning back to the home-page
@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

#Route for moving to the folder page.
@app.route('/folders', methods = ['GET', 'POST'])
def folder():
    (folders, images) = fh.getSubFolders()

    #We now return the folder page and all the subfolders and filenames.
    return render_template(
        #"test.html",
        "folderViewer.html",
        folders=folders,
        images=images)


#Route for moving to the image-viewer page, which depends on the folder nr. that the user clicks on.
@app.route('/imageViewer/<index>',methods = ['GET', 'POST'])
def img(index):
    (folders, images) = fh.getSubFolders() #We get list of subfolders and images in subfolders.
    print(folders, images)
    #We now return the image-viewer page and the three necessary variable for determining which subfolder have been chosen.
    return render_template(
        "imageViewer.html",
        folders=folders,
        chosenFolder=index,
        images=images)

#Route for changing parameters and starting tests.
@app.route('/parameters', methods = ['GET', 'POST'])
def parameters():

    #We now return the folder page and all the subfolder and filenames.
    return render_template(
        #"test.html",
        "parameters.html"
        )
