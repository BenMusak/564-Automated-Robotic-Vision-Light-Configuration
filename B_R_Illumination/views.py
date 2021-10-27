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

robot, robot1, RDK = rDK.initializeRobot() # This function returns two robot items, so we can control them individually.
#/<cmd>
@app.route('/process', methods=['POST'])
def process():
    global x_newvalue, y_newvalue, z_newvalue, slide_value, response, i, run
    cmd = request.form['name']
    if cmd == 'RIGHT':
        #x_newvalue += int(request.form['volume'])
        print("RIGHT")
        #rDK.moveRobot(robot1, 75)
        run[0] = True
        rDK.startHemisPath(robot1, run)
    elif cmd == 'LEFT':
        #x_newvalue += -int(request.form['volume'])
        print("LEFT")
        #rDK.moveRobot(robot1, 77)
        run[0] = False
    elif cmd == "UP":
        print("UP")
        rDK.moveRobot(robot1, 72)
    elif cmd == 'DOWN':
        print("DOWN")
        rDK.moveRobot(robot1, 80)
    elif cmd == 'RAISE':
        print("RAISE")
        rDK.moveRobot(robot1, 113)
    elif cmd == 'LOWER':
        print("LOWER")
        rDK.moveRobot(robot1, 97)
    #response = "Moving {}".format(cmd.capitalize())
    if cmd == 'HOME':
        #response = BR.connect()
        rDK.startHemisPath(robot, run)
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
