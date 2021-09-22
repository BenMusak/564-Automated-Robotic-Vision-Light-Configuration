"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request
from B_R_Illumination import app
slide_value = 10
x_newvalue = 0
y_newvalue = 0
z_newvalue = 120
@app.route('/', methods = ['GET', 'POST'])
def controls():
    global x_newvalue, y_newvalue, z_newvalue, slide_value
    if 'RIGHT' in request.form:
        x_newvalue += int(request.form['volume'])
        print("RIGHT")
    elif 'LEFT' in request.form:
        x_newvalue += -int(request.form['volume'])
        print("LEFT")
    elif 'UP' in request.form:
        print("UP")
    elif 'DOWN' in request.form:
        print("DOWN")
    elif 'RAISE' in request.form:
        print("RAISE")
    elif 'LOWER' in request.form:
        print("LOWER")
    elif 'HOME' in request.form:
        x_newvalue = 0
        y_newvalue = 0
        z_newvalue = 120

    #Save slider position
    if request.form:
        slide_value = request.form['volume']

    #Update webpage
    return render_template(
        "index.html",
        x_value = x_newvalue,
        y_value = y_newvalue,
        z_value = z_newvalue,
        value = slide_value)

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

