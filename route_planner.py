from io import IncrementalNewlineDecoder
from math import atan, atan2, pi, sqrt
import csv
import numpy as np
from robodk.robodk import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pandas

def plan_camera_route(viewPoint, obj_hlw, feedback):
    """Computes the X, Y and Z Coordinates for the camera route depending on the viewpoint coordinates and object dimension.
    The route is computed based on the formula for a simple 3D surface, where one dimension (X or Y) is limited.
    Set feedback to True, to see a 3D plot of the route.
    https://academo.org/demos/3d-surface-plotter/?expression=-x*x&xRange=-50%2C%2050&yRange=-50%2C%2050&resolution=25 

    Args:
        viewPoint (List): List that contains X, Y and Z coordinates for the focus point.
        obj_hlw (List): List that contains the height, length and width of the object.
        feedback (Boolean): Boolean for showing 3D plot of route.
    """
    #Set the length, width and height of the route
    #We add a buffer of value 1, so that the lightbar wont collide with the object.
    a = obj_hlw[1] +1
    b = obj_hlw[2] + 1
    c = obj_hlw[0] + 1
    #Set for loop max and minimum
    max_x = c/pow(a,2)
    max_y = c/pow(b,2)
    min_y = -max_y
    min_x = -max_x

    xyz = []  # List for only XYZ coordinates.
    rpy = []  # List for inly Roll, Pitch and Yaw.
    i = 0  # Used for indexing xyzrpw list.

    # Focus point for the light bar.
    inspection_center_xyz = viewPoint

    #
    step_x = -0.1
    step_y = 0.1
    # Generating the 3D points for an hemisphere
    # We iterate over all y-coordinate before we change to new x-coordinate, thereafter
    # we also change the polarity of the min_y, max_y and step variables.
    # This results in a back and forth movement
    # Example: "For the first x-coordinate, the y-coordinates start at negative and end at positive.
    # For the second x-coordinate, the y-coordinates start at positive and end at negative."

    for x_it in np.arange(max_x, min_x, step_x):
        try:
            # Computing the x, y and z coordinates of the points in the hemisphere wrt. to the robot frame
            # (we multiply with 50 just to make the hemisphere a bit larger)
            z_hemsphe = (-x_it*x_it*a+c)*50 + inspection_center_xyz[2]
            # We add 500 to move the hemisphere a bit away from origon.
            x_hemsphe = x_it*50 + inspection_center_xyz[0]
            y_hemsphe = inspection_center_xyz[1]

            # Compute roll, pitch and yaw of the camera with fixed angles wrt. the robot frame.
            # vectors from camera frame to inspection frame
            x_vect = inspection_center_xyz[0] - x_hemsphe
            y_vect = inspection_center_xyz[1] - y_hemsphe
            z_vect = inspection_center_xyz[2] - z_hemsphe

            if x_vect < 0 and z_vect > 0:
                rot_y = atan(z_vect/x_vect)/pi*180
            elif x_vect > 0 and z_vect > 0:
                rot_y = atan(x_vect/z_vect)/pi*180
            elif x_vect > 0 and z_vect < 0:
                rot_y = -atan(z_vect/x_vect)/pi*180+180
            elif x_vect < 0 and z_vect < 0:
                rot_y = atan(x_vect/z_vect)/pi*180+270
            else:
                print(
                    "computiation fail in y angle between camera and inspection object")

            if y_vect > 0 and z_vect < 0:
                rot_x = atan(y_vect/(sqrt(pow(z_vect, 2)+pow(x_vect, 2))))/pi*180-90
            elif y_vect < 0 and z_vect < 0:
                rot_x = - atan((sqrt(pow(z_vect, 2)+pow(x_vect, 2)))/y_vect)/pi*180-180
            elif y_vect < 0 and z_vect > 0:
                rot_x = atan(z_vect/y_vect)/pi*180
            elif y_vect > 0 and z_vect > 0:
                rot_x = atan(y_vect/z_vect)/pi*180
            else:
                print(
                    "computiation fail in x angle between camera and inspection object")

            pathPoints = transl(
                x_hemsphe, y_hemsphe, z_hemsphe)*rotz(0*pi/180)*roty(0*pi/180)*rotx(0*pi/180)

            xyz.append(
                [pathPoints[0, 3], pathPoints[1, 3], pathPoints[2, 3]])

            # Fixed rotation
            rot_y1 = rot_y - 90

            # Euler rotation
            rot_x2 = rot_x + 90
            
            rpy.append([rot_x2,rot_y1,0])

            i += 1
            # Using the double for loop actually results is us trying to find values that exceed
            # the hemipshere, the try except func prevents the program from stopping, when this happens.
        except:
            print("compute error")
    
    for y_it in np.arange(min_y, max_y, step_y):
        try:
            # Computing the x, y and z coordinates of the points in the hemisphere wrt. to the robot frame
            # (we multiply with 50 just to make the hemisphere a bit larger)
            z_hemsphe = (-y_it*y_it*a+c)*50 + inspection_center_xyz[2]
            # We add 500 to move the hemisphere a bit away from origon.
            x_hemsphe = inspection_center_xyz[0]
            y_hemsphe = y_it*50 + inspection_center_xyz[1]

            # Compute roll, pitch and yaw of the camera with fixed angles wrt. the robot frame.
            # vectors from camera frame to inspection frame
            x_vect = inspection_center_xyz[0] - x_hemsphe
            y_vect = inspection_center_xyz[1] - y_hemsphe
            z_vect = inspection_center_xyz[2] - z_hemsphe

            if x_vect < 0 and z_vect > 0:
                rot_y = atan(z_vect/x_vect)/pi*180
            elif x_vect > 0 and z_vect > 0:
                rot_y = atan(x_vect/z_vect)/pi*180
            elif x_vect > 0 and z_vect < 0:
                rot_y = -atan(z_vect/x_vect)/pi*180+180
            elif x_vect < 0 and z_vect < 0:
                rot_y = atan(x_vect/z_vect)/pi*180+270
            else:
                print(
                    "computiation fail in y angle between camera and inspection object")

            if y_vect > 0 and z_vect < 0:
                rot_x = atan(y_vect/(sqrt(pow(z_vect, 2)+pow(x_vect, 2))))/pi*180-90
            elif y_vect < 0 and z_vect < 0:
                rot_x = - atan((sqrt(pow(z_vect, 2)+pow(x_vect, 2)))/y_vect)/pi*180-180
            elif y_vect < 0 and z_vect > 0:
                rot_x = atan(z_vect/y_vect)/pi*180
            elif y_vect > 0 and z_vect > 0:
                rot_x = atan(y_vect/z_vect)/pi*180
            else:
                print(
                    "computiation fail in x angle between camera and inspection object")

            pathPoints = transl(
                x_hemsphe, y_hemsphe, z_hemsphe)*rotz(0*pi/180)*roty(0*pi/180)*rotx(0*pi/180)

            xyz.append(
                [pathPoints[0, 3], pathPoints[1, 3], pathPoints[2, 3]])

            # Fixed rotation
            rot_y1 = rot_y - 90

            # Euler rotation
            rot_x2 = rot_x + 90
            
            rpy.append([rot_x2,rot_y1,0])

            i += 1
            # Using the double for loop actually results is us trying to find values that exceed
            # the hemipshere, the try except func prevents the program from stopping, when this happens.
        except:
            print("compute error")
        max_y = -max_y
        min_y = -min_y
        step_y = -step_y

    print("Number of points in hemossphere: ",len(xyz))
    with open('Hemisphere.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        for pos in xyz:
            writer.writerow(pos)

    print("path generated", len(xyz))

    #Save X, Y and Z coordinates as a csv file.
    print("Number of points in hemossphere: ",len(xyz))

    #If we want feedback, we can show the 3D path plot. 
    if feedback:
        DataAll1D = np.loadtxt("Hemisphere.csv", delimiter=",")
        X = DataAll1D[:,0]
        Y = DataAll1D[:,1]
        Z = DataAll1D[:,2]
        fig = plt.figure()
        ax = plt.axes(projection ='3d')
        ax.plot3D(X, Y, Z, 'green')
        #Remember to close this for continuing the code.
        plt.show()

    """for i in range(len(xyz)):
        x = xyz[i][0] * 0.001
        y = xyz[i][1] * 0.001
        z = xyz[i][2] * 0.001
        rx = -np.deg2rad(rpy[i][0])
        ry = np.deg2rad(rpy[i][1])
        rz = np.deg2rad(rpy[i][2])"""


def plan_light_route(viewPoint, obj_hlw, feedback):
    """Computes the X, Y and Z Coordinates for the lightbar route depending on the viewpoint coordinates and object dimension.
    The route is computed based on the formula for a Ellipsoid.

    Args:
        viewPoint (List): List that contains X, Y and Z coordinates for the focus point.
        obj_hlw (List): List that contains the height, length and width of the object.
        feedback (Boolean): Boolean for whether extended feedback should be shown.
    """
    #Set the length, width and height of the Ellipsoid.
    #We add a buffer of value 1, so that the lightbar wont collide with the object.
    a = obj_hlw[1] + 1
    b = obj_hlw[2] + 1
    c = obj_hlw[0] + 1
    #Set for loop max and minimum
    max_x = a
    max_y = b
    min_y = -max_y
    min_x = -max_x

    xyz = []  # List for only XYZ coordinates.
    rpy = []  # List for inly Roll, Pitch and Yaw.
    i = 0  # Used for indexing xyzrpw list.

    # Focus point for the light bar.
    inspection_center_xyz = viewPoint

    #
    step_x = -0.1
    step_y = 0.1

    # Generating the 3D points for an hemisphere
    # We iterate over all y-coordinate before we change to new x-coordinate, thereafter
    # we also change the polarity of the min_y, max_y and step variables.
    # This results in a back and forth movement
    # Example: "For the first x-coordinate, the y-coordinates start at negative and end at positive.
    # For the second x-coordinate, the y-coordinates start at positive and end at negative."
    for x_it in np.arange(max_x, min_x, step_x):
        for y_it in np.arange(min_y, max_y, step_y):
            try:
                # Computing the x, y and z coordinates of the points in the ellipsoid, to the robot frame
                # (we multiply with 50 just to make the hemisphere a bit larger)
                # The focus point for the light bar is also added to the coordinates.

                #First we compute the height (z), by having isolated z in the ellipsoid forula.
                #This results in a fraction, so for easier view the computation is split up:
                numerator = ((pow(a,2)*pow(b,2))-(pow(b,2)*pow(x_it,2))-(pow(a,2)*pow(y_it,2)))
                denominator = (pow(a,2)*pow(b,2))
                z_ellipsoid = c*sqrt(numerator/denominator)*50+inspection_center_xyz[2]
                #We can now compute the other coordinates.
                x_ellipsoid = x_it*50 + inspection_center_xyz[0]
                y_ellipsoid = y_it*50 + inspection_center_xyz[1]

                
                # vectors from camera frame to inspection frame
                x_vect = inspection_center_xyz[0] - x_ellipsoid
                y_vect = inspection_center_xyz[1] - y_ellipsoid
                z_vect = inspection_center_xyz[2] - z_ellipsoid

                # Compute roll, pitch and yaw of the camera with fixed angles wrt. the robot frame.
                if x_vect < 0 and z_vect > 0:
                    rot_y = atan(z_vect/x_vect)/pi*180
                elif x_vect > 0 and z_vect > 0:
                    rot_y = atan(x_vect/z_vect)/pi*180
                elif x_vect > 0 and z_vect < 0:
                    rot_y = -atan(z_vect/x_vect)/pi*180+180
                elif x_vect < 0 and z_vect < 0:
                    rot_y = atan(x_vect/z_vect)/pi*180+270
                else:
                    print(
                        "computiation fail in y angle between camera and inspection object")

                if y_vect > 0 and z_vect < 0:
                    rot_x = atan(y_vect/(sqrt(pow(z_vect, 2)+pow(x_vect, 2))))/pi*180-90
                elif y_vect < 0 and z_vect < 0:
                    rot_x = - atan((sqrt(pow(z_vect, 2)+pow(x_vect, 2)))/y_vect)/pi*180-180
                elif y_vect < 0 and z_vect > 0:
                    rot_x = atan(z_vect/y_vect)/pi*180
                elif y_vect > 0 and z_vect > 0:
                    rot_x = atan(y_vect/z_vect)/pi*180
                else:
                    print(
                        "computiation fail in x angle between camera and inspection object")

                #Compute the translation and rotation matrix.
                pathPoints = transl(
                    x_ellipsoid, y_ellipsoid, z_ellipsoid)*rotz(0*pi/180)*roty(0*pi/180)*rotx(0*pi/180)

                xyz.append(
                    [pathPoints[0, 3], pathPoints[1, 3], pathPoints[2, 3]])

                # Fixed rotation
                rot_y1 = rot_y - 90

                # Euler rotation
                rot_x2 = rot_x + 90
                
                rpy.append([rot_x2,rot_y1,0])

                i += 1
                # Using the double for loop actually results in us trying to find values that exceed
                # the ellipsoid, the try except func prevents the program from stopping, when this happens.
            except:
                if feedback:
                    print("compute error")
        #We change the polarity of the for loop, so that we get a nice zig-zag pattern.
        max_y = -max_y
        min_y = -min_y
        step_y = -step_y

    #Save X, Y and Z coordinates as a csv file.
    print("Number of points in hemossphere: ",len(xyz))
    with open('Ellipsoid.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        for pos in xyz:
            writer.writerow(pos)

    print("path generated")
    
    #If we want feedback, we can show the 3D path plot. 
    if feedback:
        DataAll1D = np.loadtxt("Ellipsoid.csv", delimiter=",")
        X = DataAll1D[:,0]
        Y = DataAll1D[:,1]
        Z = DataAll1D[:,2]
        fig = plt.figure()
        ax = plt.axes(projection ='3d')
        ax.plot3D(X, Y, Z, 'green')
        #Remember to close this for continuing the code.
        plt.show()


    """for i in range(len(xyz)):
        x = xyz[i][0] * 0.001
        y = xyz[i][1] * 0.001
        z = xyz[i][2] * 0.001
        rx = -np.deg2rad(rpy[i][0])
        ry = np.deg2rad(rpy[i][1])
        rz = np.deg2rad(rpy[i][2])"""

    # TODO: Return the xyz and rpy lists, so that we can use them in testHandler.py


