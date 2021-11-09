"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, jsonify, json
from B_R_Illumination import app
import BRClient as BR
import folderHandler as fh
import imageHandler as ih
import roboDK as rDK
slide_value = 10
x_newvalue = 0
y_newvalue = 0
z_newvalue = 120
response = "hello"
folders = []
images =[]
i = 0


run = [True] # Used for stopping the RoboDK threads.We can simulate them using a list, since pointers do not exist in python.
LEFT, RIGHT, UP, DOWN, RESET = "left", "right", "up", "down", "reset"
AVAILABLE_COMMANDS = {
    'Left': LEFT,
    'Right': RIGHT,
    'Up': UP,
    'Down': DOWN,
    'Reset': RESET
}

#robot, robot1, RDK = rDK.initializeRobot() # This function returns two robot items, so we can control them individually.

#/<cmd>
@app.route('/process', methods=['POST'])
def process():
    global x_newvalue, y_newvalue, z_newvalue, slide_value, response, i, run
    cmd = request.form['name']

    try:
        camera = request.form['camera']
        print("Camera = " + camera)
    except:
        camera = "off"
        print("Camera = " + camera)

    try:
        cameraradio = request.form['cameraradio']
        print("Camera light color = " + cameraradio)
    except:
        if camera != "off":
            print("No color have been chosen for Camera light")

    try:
        barlight1 = request.form['barlight1']
        print("Lightbar = " + barlight1)
    except:
        barlight1 = "off"
        print("Lightbar = " + barlight1)
    
    try:
        barlight1radio = request.form['barlight1radio']
        print("Lightbar = " + barlight1radio)
    except:
        if barlight1 != "off":
            print("No color have been chosen for lightbar")

    try:
        backlight = request.form['backlight']
        print("Backlight = " + backlight)
    except:
        backlight = "off"
        print("Backlight = " + backlight)

    try:
        backlight1radio = request.form['backlightradio']
        print("Backlight color = " + backlight1radio)
    except:
        if backlight != "off":
            print("No color have been chosen for backlight")

    try:
        irfilter = request.form['irfilter']
        print("irfilter = " + irfilter)
    except:
        irfilter = "off"
        print("irfilter = " + irfilter)

    try:
        obj_width = request.form['obj_width']
        obj_length = request.form['obj_length']
        obj_height = request.form['obj_height']
        print("Object width = " + obj_width + "  Object length = " + obj_length + "  Object height = " + obj_height)
    except:
        obj_height = 0
        obj_length = 0
        obj_width = 0
    
    try:
        img_amount = request.form['img_amount']
        print("Image amount = " + img_amount)
    except:
        img_amount = 0

    if cmd == 'RIGHT':
        #x_newvalue += int(request.form['volume'])
        print("RIGHT")
        #rDK.moveRobot(robot1, 75)
        #run[0] = True
        #rDK.startHemisPath(robot1, run, RDK)
    elif cmd == 'LEFT':
        #x_newvalue += -int(request.form['volume'])
        print("LEFT")
        #rDK.moveRobot(robot1, 77)
        #run[0] = False
    elif cmd == "UP":
        print("UP")
        #rDK.moveRobot(robot1, 72)
    elif cmd == 'DOWN':
        print("DOWN")
        #rDK.moveRobot(robot1, 80)
    elif cmd == 'RAISE':
        print("RAISE")
        #rDK.moveRobot(robot1, 113)
    elif cmd == 'LOWER':
        print("LOWER")
        #rDK.moveRobot(robot1, 97)
    #response = "Moving {}".format(cmd.capitalize())
    if cmd == 'HOME':
        #response = BR.connect()
        #rDK.startHemisPath(robot, run, RDK)
        ih.getURLImage("subfolder1", "img", str(i))
        i += 1
        x_newvalue = 0
        y_newvalue = 0
        z_newvalue = 120
    #Save slider position
    #if request.form:
        #slide_value = request.form['volume']
        response = "Successfully moved the robot " + cmd
    # ser.write(camera_command)
    return jsonify({'output' : response})

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

    #We now return the folder page and all the subfolder and filenames.
    return render_template(
        #"test.html",
        "folderViewer.html",
        folders=folders,
        images=images)


#Route for moving to the image-viewer page, which depends on the folder nr. that the user clicks on.
@app.route('/imageViewer/<index>',methods = ['GET', 'POST'])
def img(index):
    (folders, images) = fh.getSubFolders() #We get list of subfolders and images in subfolders.
    
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
