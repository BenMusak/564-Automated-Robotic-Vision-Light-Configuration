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
import testHandler as th
import os
import route_planner as rp
import OPCUA
#import roboDK as rDK

response = ""
folders = []
images =[]
test_state = False
run = [True] # Used for stopping the RoboDK threads.We can simulate them using a list, since pointers do not exist in python.
firstrun = False

#ros_client = rb.startROS_Connect()
#OPCUA_client = OPCUA.connectToClient("opc.tcp://192.168.87.210:4840")

@app.route('/process', methods=['POST'])
def process():
    global x_newvalue, y_newvalue, z_newvalue, slide_value, response, i, run, test_state
    error_msg = ""
    error_state = False

    # Validate the parameter data.   
    rp.plan_camera_route([0,0,0], [15,1,1], True) #This is just for testing, should be used in testHandler.py
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

    try:
        test_name = request.form['test_name']
    except:
        test_name = None
    
    if test_name =="":
        error_msg = error_msg + " No test name was given. \n"
    elif os.path.exists("B_R_Illumination/static/XML/" + test_name):
        error_msg = error_msg + " Test name already exist. \n"
    else:
        print("Name is all good.")

    #rb.startROS_Connect()
    #response = BR.connect()
    #ih.getURLImage("subfolder1", "img", str(i))

    #If data is valid, then begin test. If not or test is already running, then return error message back to the client.
    if error_msg =="" and test_state == False:
        print("No errors")
        response = "Successfully started the test"
        error_state = False
        test_state = True
        obj_dim = [obj_height, obj_length, obj_width]
        #Here we call the testing loop.
        #test_state = th.prepareTesting(OPCUA_client, ros_client, int(img_amount), test_name, lightColor, backlight, barlight1, camera, obj_dim) 
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
