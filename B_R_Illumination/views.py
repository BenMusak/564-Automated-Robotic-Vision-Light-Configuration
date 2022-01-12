"""
Routes and views for the flask application.
"""

from datetime import datetime
from os import error
from flask import Flask, render_template, request, jsonify, json
from B_R_Illumination import app
from flask_socketio import SocketIO, emit, send
import BRClient as BR
import folderHandler as fh
import imageHandler as ih
import rosbridge as rb
import testHandler as th
import os
import route_planner as rp
import OPCUA
import xml.etree.cElementTree as ET
import xmltodict
import json
import re
import numpy as np
import json
import mysql.connector
import threading

response = ""
folders = []
images = []
test_state = False
# Used for stopping the RoboDK threads. We can simulate them using a list, since pointers do not exist in python.
run = [False, 0, 0, 0, 0, 0, 0, 0]
firstrun = False
ROS_Connected = True
socketio = SocketIO(app)

try:
    ros_client = rb.startROS_Connect()
except:
    print("Could not connect to ROS server.")
    ROS_Connected = False

OPCUA_client = OPCUA.connectAsClient("opc.tcp://192.168.87.210:4840")
# try:
# os.remove("camera_route.csv")
# os.remove("lightbar_route.csv")
# except:
# pass


@app.route('/process', methods=['POST'])
def process():
    global x_newvalue, y_newvalue, z_newvalue, slide_value, response, i, run, test_state
    error_msg = ""
    error_state = False

    # Validate the parameter data.
    # rp.plan_camera_route([10,10,0], [1,1,1], True) #This is just for testing, should be used in testHandler.py
    #ih.getURLImage("folder1", "test", "1")
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
        print("Object width = " + obj_width + "  Object length = " +
              obj_length + "  Object height = " + obj_height)
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
        view_pointz = request.form['view_pointz']
        print(" Viewpoint z = " + view_pointz)
    except:
        view_pointz = None

    if view_pointz.isdigit():
        print("Value is all good.")
    else:
        error_msg = error_msg + " Viewpoint z contains invalid charachters or is empty. \n"

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

    if test_name == "":
        error_msg = error_msg + " No test name was given. \n"
    elif os.path.exists("B_R_Illumination/static/XML/" + test_name):
        error_msg = error_msg + " Test name already exist. \n"
    else:
        print("Name is all good.")

    # If data is valid, then begin test. If not or test is already running, then return error message back to the client.
    if error_msg == "" and test_state == False:
        response = "Successfully started the test"
        error_state = False
        test_state = True
        obj_dim = [int(obj_height)/1000, int(obj_length) /
                   1000, int(obj_width)/1000]
        viewPoint = int(view_pointz)/1000
        run[0] = True
        # Here we call the testing loop.
        if ROS_Connected:
            test_state = th.runTesting(OPCUA_client, ros_client, int(
                img_amount), test_name, lightColor, backlight, barlight1, camera, obj_dim, viewPoint, run)
    elif test_state:
        response = "Test is already running."
        error_state = True
    else:
        response = error_msg
        error_state = True
    return jsonify({'output': response, 'error_state': error_state})

# Normal route for returning back to the home-page


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'status.html',
        title='Home Page',
        year=datetime.now().year,
    )

# Route for moving to the folder page.


@app.route('/folders', methods=['GET', 'POST'])
def folder():
    (folders, images) = fh.getSubFolders()

    # We now return the folder page and all the subfolders and filenames.
    return render_template(
        # "test.html",
        "folderViewer.html",
        folders=folders,
        images=images)


# Route for moving to the image-viewer page, which depends on the folder nr. that the user clicks on.
@app.route('/imageViewer/<index>', methods=['GET', 'POST'])
def img(index):
    # We get list of subfolders and images in subfolders.
    (folders, images) = fh.getSubFolders()

    try:
        db = mysql.connector.connect(
            host="localhost", user="andr", password="1212", database="brmysql")

    except:
        print("Could not connect to database.")

    cursor = db.cursor()
    cursor.execute("SELECT * FROM images WHERE run = {}".format(index))

    for (id, img_name, path, run, camera_gainLevel, camera_focusScale, camera_exposureTime, camera_flashColor, camera_chromaticLock, camera_irFilter, camera_x, camera_y, camera_z, camera_yaw, camera_pitch, camera_roll, barLight_exposureTime, barLight_flashColor, barLight_angle, barLight_x, barLight_y, barLight_z, barLight_yaw, barLight_pitch, barLight_roll, backLight_exposureTime, backLight_flashColor, passTest) in cursor:
        settings_list = [img_name, path, run, camera_gainLevel, camera_focusScale, camera_exposureTime, camera_flashColor, camera_chromaticLock, camera_irFilter, camera_x, camera_y, camera_z, camera_yaw, camera_pitch,
                         camera_roll, barLight_exposureTime, barLight_flashColor, barLight_angle, barLight_x, barLight_y, barLight_z, barLight_yaw, barLight_pitch, barLight_roll, backLight_exposureTime, backLight_flashColor, passTest]

    # We now return the image-viewer page and the three necessary variable for determining which subfolder have been chosen.
    return render_template(
        "imageViewer.html",
        folders=folders,
        chosenFolder=index,
        images=images,
        settings_list=settings_list)

# Route for changing parameters and starting tests.


@app.route('/parameters', methods=['GET', 'POST'])
def parameters():

    # We now return the folder page and all the subfolder and filenames.
    return render_template(
        # "test.html",
        "parameters.html"
    )


@app.route('/statusupdate', methods=['GET'])
def statusupdate():

    return jsonify({'Teststatus': run
                    })


@app.route('/createplots', methods=['GET'])
def createplots():
    try:
        cameraRoute = np.loadtxt("camera_route.csv", delimiter=",").tolist()
    except:
        cameraRoute = []
    try:
        lightbarRoute = np.loadtxt(
            "lightbar_route.csv", delimiter=",").tolist()
    except:
        lightbarRoute = []

    return jsonify({'cameraRoute': cameraRoute, 'lightbarRoute': lightbarRoute
                    })


@app.route('/CancelTest', methods=['GET'])
def cancelTest():
    run[0] = False
    return jsonify({
    })
