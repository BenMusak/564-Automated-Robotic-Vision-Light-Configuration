"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, jsonify, json
from B_R_Illumination import app
import BRClient as BR
import folderHandler as fh
import imageHandler as ih
slide_value = 10
x_newvalue = 0
y_newvalue = 0
z_newvalue = 120
response = "hello"
folders = []
images =[]
i = 0

LEFT, RIGHT, UP, DOWN, RESET = "left", "right", "up", "down", "reset"
AVAILABLE_COMMANDS = {
    'Left': LEFT,
    'Right': RIGHT,
    'Up': UP,
    'Down': DOWN,
    'Reset': RESET
}


@app.route('/<cmd>')
def controls(cmd=None):
    global x_newvalue, y_newvalue, z_newvalue, slide_value, response, i
    if cmd == 'RIGHT':
        #x_newvalue += int(request.form['volume'])
        print("RIGHT")
    elif cmd == 'LEFT':
        #x_newvalue += -int(request.form['volume'])
        print("LEFT")
    elif cmd == "UP":
        print("UP")
    elif cmd == 'DOWN':
        print("DOWN")
    elif cmd == 'RAISE':
        print("RAISE")
    elif cmd == 'LOWER':
        print("LOWER")
    #response = "Moving {}".format(cmd.capitalize())
    if cmd == 'HOME':
        #response = BR.connect()

        ih.getURLImage("subfolder1", "img", str(i))
        i += 1
        x_newvalue = 0
        y_newvalue = 0
        z_newvalue = 120

    #Save slider position
    if request.form:
        slide_value = request.form['volume']


    # ser.write(camera_command)
    return response




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
