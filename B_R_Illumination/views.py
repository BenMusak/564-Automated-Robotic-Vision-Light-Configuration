"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request
from B_R_Illumination import app
import BRClient as BR
slide_value = 10
x_newvalue = 0
y_newvalue = 0
z_newvalue = 120
response = "hello"

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
    global x_newvalue, y_newvalue, z_newvalue, slide_value, response
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
        response = BR.connect()
        x_newvalue = 0
        y_newvalue = 0
        z_newvalue = 120

    #Save slider position
    if request.form:
        slide_value = request.form['volume']


    # ser.write(camera_command)
    return response





@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/modes', methods = ['GET', 'POST'])
def modes():
    return render_template(
        "modes.html")

