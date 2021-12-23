from io import IncrementalNewlineDecoder
from math import atan, atan2, pi, sqrt
import csv
import numpy as np
from robodk.robodk import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pandas

def plan_camera_route(viewPoint, obj_hlw, feedback, step_x, step_y):
    """Computes the X, Y and Z Coordinates for the camera route depending on the viewpoint coordinates and object dimension.
    The route is computed based on the formula for a simple 3D surface, where one dimension (X or Y) is limited.
    Set feedback to True, to see a 3D plot of the route.
    https://academo.org/demos/3d-surface-plotter/?expression=-x*x&xRange=-50%2C%2050&yRange=-50%2C%2050&resolution=25 

    Args:
        viewPoint (List): List that contains X, Y and Z coordinates for the focus point.
        obj_hlw (List): List that contains the height, length and width of the object.
        feedback (Boolean): Boolean for showing 3D plot of route.
    """
    center = [0.367, 0.120, 0.154]
    #Set for loop max and minimum
    max_x = (obj_hlw[1] + 0.1)/2
    max_y = (obj_hlw[2] + 0.1)/2
    min_y = -max_y
    min_x = -max_x
    #Set the length, width and height of the route
    #We add a buffer of value 1, so that the lightbar wont collide with the object.
    c = (obj_hlw[0] + 0.1)
    a = c/pow(max_x,2)
    b = c/pow(max_y,2)
    print("a: ", a)
    print("b: ", b)
    print("c: ", c)

    xyz = []  # List for only XYZ coordinates.
    i = 0  # Used for indexing xyzrpw list.

    #inspection_center_xyz = [0,0,0]
    move_step_x = (max_x-min_x)/(step_x/2)
    move_step_y = (max_y-min_y)/(step_y/2)
    print("move_step: ", move_step_x)
    print("move_step: ", move_step_y)

    # Generating the 3D points for an hemisphere
    # We iterate over all y-coordinate before we change to new x-coordinate, thereafter
    # we also change the polarity of the min_y, max_y and step variables.
    # This results in a back and forth movement
    # Example: "For the first x-coordinate, the y-coordinates start at negative and end at positive.
    # For the second x-coordinate, the y-coordinates start at positive and end at negative."

    for x_it in np.arange(min_x, max_x, move_step_x):
        try:
            # Computing the x, y and z coordinates of the points in the hemisphere wrt. to the robot frame
            # (we multiply with 50 just to make the hemisphere a bit larger)
            z_hemsphe = (-x_it*x_it*a+c) + viewPoint + center[2]
            # We add 500 to move the hemisphere a bit away from origon.
            x_hemsphe = x_it + center[0]
            y_hemsphe = center[1]

            # Compute roll, pitch and yaw of the camera with fixed angles wrt. the robot frame.
            # vectors from camera frame to inspection frame

            xyz.append([x_hemsphe, y_hemsphe, z_hemsphe])

            i += 1
            # Using the double for loop actually results is us trying to find values that exceed
            # the hemipshere, the try except func prevents the program from stopping, when this happens.
        except:
            print("compute error")
    
    for y_it in np.arange(min_y, max_y, move_step_y):
        try:
            # Computing the x, y and z coordinates of the points in the hemisphere wrt. to the robot frame
            # (we multiply with 50 just to make the hemisphere a bit larger)
            z_hemsphe = (-y_it*y_it*b+c) + viewPoint + center[2]
            # We add 500 to move the hemisphere a bit away from origon.
            x_hemsphe = 0 + center[0]
            y_hemsphe = y_it + center[1]

            # Compute roll, pitch and yaw of the camera with fixed angles wrt. the robot frame.
            # vectors from camera frame to inspection frame
            xyz.append([x_hemsphe, y_hemsphe, z_hemsphe])

            i += 1
            # Using the double for loop actually results is us trying to find values that exceed
            # the hemipshere, the try except func prevents the program from stopping, when this happens.
        except:
            print("compute error")
        max_y = -max_y
        min_y = -min_y
        step_y = -step_y

    print("Number of points in camera route: ",len(xyz))
    with open('camera_route.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        for pos in xyz:
            writer.writerow(pos)

    print("path generated", len(xyz))

    #If we want feedback, we can show the 3D path plot. 
    if feedback:
        DataAll1D = np.loadtxt("camera_route.csv", delimiter=",")
        X = DataAll1D[:,0]
        Y = DataAll1D[:,1]
        Z = DataAll1D[:,2]
        fig = plt.figure()
        ax = plt.axes(projection ='3d')
        ax.plot3D(X, Y, Z, 'green')
        ax.scatter(X,Y,Z, 'blue')
        #Remember to close this for continuing the code.
        plt.show()
    return xyz


def plan_light_route(viewPoint, obj_hlw, feedback, step_x, step_y):
    """Computes the X, Y and Z Coordinates for the lightbar route depending on the viewpoint coordinates and object dimension.
    The route is computed based on the formula for a Ellipsoid.

    Args:
        viewPoint (List): List that contains X, Y and Z coordinates for the focus point.
        obj_hlw (List): List that contains the height, length and width of the object.
        feedback (Boolean): Boolean for whether extended feedback should be shown.
    """
    #Set the length, width and height of the Ellipsoid.
    #We add a buffer of value 1, so that the lightbar wont collide with the object.
    center = [0.367, 0.120, 0.154]
    a = (obj_hlw[1] + 0.3)/2
    b = (obj_hlw[2] + 0.3)/2
    c = (obj_hlw[0] + 0.3)/2
    #Set for loop max and minimum
    max_x = a
    max_y = b
    min_y = -max_y
    min_x = -max_x

    xyz = []  # List for only XYZ coordinates.
    rpy = []  # List for inly Roll, Pitch and Yaw.
    i = 0  # Used for indexing xyzrpw list.

    # Focus point for the light bar.

    move_step_x = (max_x-min_x)/(sqrt(step_x)+1)
    move_step_y = (max_y-min_y)/(sqrt(step_y)+1)
    print("move_step: ", move_step_x)
    print("move_step: ", move_step_y)
    # Generating the 3D points for an hemisphere
    # We iterate over all y-coordinate before we change to new x-coordinate, thereafter
    # we also change the polarity of the min_y, max_y and step variables.
    # This results in a back and forth movement
    # Example: "For the first x-coordinate, the y-coordinates start at negative and end at positive.
    # For the second x-coordinate, the y-coordinates start at positive and end at negative."
    for x_it in np.arange(max_x, min_x, -move_step_x):
        for y_it in np.arange(min_y, max_y, move_step_y):
            try:
                # Computing the x, y and z coordinates of the points in the ellipsoid, to the robot frame
                # (we multiply with 50 just to make the hemisphere a bit larger)
                # The focus point for the light bar is also added to the coordinates.

                #First we compute the height (z), by having isolated z in the ellipsoid forula.
                #This results in a fraction, so for easier view the computation is split up:
                numerator = ((pow(a,2)*pow(b,2))-(pow(b,2)*pow(x_it,2))-(pow(a,2)*pow(y_it,2)))
                denominator = (pow(a,2)*pow(b,2))
                z_ellipsoid = c*sqrt(numerator/denominator)+viewPoint + center[2]
                #We can now compute the other coordinates.
                x_ellipsoid = x_it + center[0]
                y_ellipsoid = y_it + center[1]

                xyz.append([x_ellipsoid, y_ellipsoid, z_ellipsoid])

                i += 1
                # Using the double for loop actually results in us trying to find values that exceed
                # the ellipsoid, the try except func prevents the program from stopping, when this happens.
            except:
                if feedback:
                    print("compute error")
        #We change the polarity of the for loop, so that we get a nice zig-zag pattern.
        max_y = -max_y
        min_y = -min_y
        move_step_y = -move_step_y

    #Save X, Y and Z coordinates as a csv file.
    print("Number of points in light bar route: ",len(xyz))
    with open('lightbar_route.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        for pos in xyz:
            writer.writerow(pos)

    print("path generated")
    
    #If we want feedback, we can show the 3D path plot. 
    if feedback:
        DataAll1D = np.loadtxt("lightbar_route.csv", delimiter=",")
        X = DataAll1D[:,0]
        Y = DataAll1D[:,1]
        Z = DataAll1D[:,2]
        fig = plt.figure()
        ax = plt.axes(projection ='3d')
        ax.plot3D(X, Y, Z, 'green')
        ax.scatter(X,Y,Z, 'blue')
        #Remember to close this for continuing the code.
        plt.show()

    return xyz


