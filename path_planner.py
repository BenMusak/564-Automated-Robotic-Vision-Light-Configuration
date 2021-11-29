from math import atan, atan2, pi, sqrt
import csv
import numpy as np
from robodk.robodk import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pandas

def plan_camera_route(viewPoint):
    # The goal here is to autogenerate a path in the shape of an hemisphere (with the object in the center),
    # that the robot can follow. We can then change the size of the hemisphere to
    # test from different distances. Furthermore, the lights should always point at the object,
    # So in some way we must change the Rotation matrix of the tcp, so that the z-axis always points to
    # the center of the hemisphere.

    a = 5  # Size of hemisphere (half sphere)
    # we find out what the max x-coordinate is (radius)
    max_x = sqrt(a-pow(0, 2)-pow(0, 2))
    max_y = max_x  # Since we are dealing with an hemisphere
    # Min_x must therefore be the oposite of max_x (asuming that the center of the hemisphere is y=0)
    min_y = -max_y
    min_x = -max_x
    xyz = []  # List for only XYZ coordinates.
    # List that contains the XYZ Coordinate and Roll Pitch Yaw Coordinates.
    i = 0  # Used for indexing xyzrpw list.

    # Reference frame (Center of Hemisphere)
    #[500, 160, 155]
    inspection_center_xyz = viewPoint
    step = 0.5

    rpy = []

    # Generating the 3D points for an hemisphere
    # We iterate over all y-coordinate before we change to new x-coordinate, thereafter
    # we also change the polarity of the min_y, max_y and step variables.
    # This results in a back and forth movement
    # Example: "For the first x-coordinate, the y-coordinates start at negative and end at positive.
    # For the second x-coordinate, the y-coordinates start at positive and end at negative."

    for x_it in np.arange(max_x, min_x, -0.1):
        for y_it in np.arange(min_y, max_y, step):
            if sqrt(pow(x_it, 2) + pow(y_it, 2)) <= a:
                try:
                  # Computing the x, y and z coordinates of the points in the hemisphere wrt. to the robot frame
                  # (we multiply with 50 just to make the hemisphere a bit larger)
                  z_hemsphe = sqrt(a-pow(x_it,2)-pow(y_it,2))*50+inspection_center_xyz[2]
                  # We add 500 to move the hemisphere a bit away from origon.
                  x_hemsphe = x_it*50 + inspection_center_xyz[0]
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
        step = -step

    print("Number of points in hemossphere: ",len(xyz))
    with open('Hemisphere.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        for pos in xyz:
            writer.writerow(pos)

    print("path generated", len(xyz))
    
    for i in range(len(xyz)):
        x = xyz[i][0] * 0.001
        y = xyz[i][1] * 0.001
        z = xyz[i][2] * 0.001
        rx = -np.deg2rad(rpy[i][0])
        ry = np.deg2rad(rpy[i][1])
        rz = np.deg2rad(rpy[i][2])


def plan_light_route(viewPoint, obj_hlw):
    # The goal here is to autogenerate a path in the shape of an hemisphere (with the object in the center),
    # that the robot can follow. We can then change the size of the hemisphere to
    # test from different distances. Furthermore, the lights should always point at the object,
    # So in some way we must change the Rotation matrix of the tcp, so that the z-axis always points to
    # the center of the hemisphere.

    #a = 5  # Size of hemisphere (half sphere)
    # we find out what the max x-coordinate is (radius)
    a = obj_hlw[1]
    b = obj_hlw[2]
    c = obj_hlw[0]
    max_x = a+5
    max_y = b+5  # Since we are dealing with an hemisphere
    # Min_x must therefore be the oposite of max_x (asuming that the center of the hemisphere is y=0)
    min_y = -max_y
    min_x = -max_x
    xyz = []  # List for only XYZ coordinates.
    # List that contains the XYZ Coordinate and Roll Pitch Yaw Coordinates.
    i = 0  # Used for indexing xyzrpw list.

    # Reference frame (Center of Hemisphere)
    #[500, 160, 155]
    inspection_center_xyz = viewPoint
    step = 0.1

    rpy = []

    # Generating the 3D points for an hemisphere
    # We iterate over all y-coordinate before we change to new x-coordinate, thereafter
    # we also change the polarity of the min_y, max_y and step variables.
    # This results in a back and forth movement
    # Example: "For the first x-coordinate, the y-coordinates start at negative and end at positive.
    # For the second x-coordinate, the y-coordinates start at positive and end at negative."
    for x_it in np.arange(max_x, min_x, -0.1):
        #for y_it in np.arange(min_y, max_y, step):
            #if sqrt(pow(x_it, 2)/pow(a,2) + pow(y_it, 2)/pow(b,2)) :
        try:
            y_it = (b*sqrt(pow(a,2)-pow(x_it,2)))/a
            # Computing the x, y and z coordinates of the points in the hemisphere wrt. to the robot frame
            # (we multiply with 50 just to make the hemisphere a bit larger)
            #z_hemsphe = sqrt(a-pow(x_it,2)-pow(y_it,2))*50+inspection_center_xyz[2]
            top = ((pow(a,2)*pow(b,2))-(pow(b,2)*pow(x_it,2))-(pow(a,2)*pow(y_it,2)))
            bund = (pow(a,2)*pow(b,2))

            z_ellipsoid = c*sqrt(top/bund) * 50
            # We add 500 to move the hemisphere a bit away from origon.
            x_ellipsoid = x_it*50 + inspection_center_xyz[0]
            y_ellipsoid = y_it*50 + inspection_center_xyz[1]

            # Compute roll, pitch and yaw of the camera with fixed angles wrt. the robot frame.
            # vectors from camera frame to inspection frame
            x_vect = inspection_center_xyz[0] - x_ellipsoid
            y_vect = inspection_center_xyz[1] - y_ellipsoid
            z_vect = inspection_center_xyz[2] - z_ellipsoid

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
                x_ellipsoid, y_ellipsoid, z_ellipsoid)*rotz(0*pi/180)*roty(0*pi/180)*rotx(0*pi/180)

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
        #max_y = -max_y
        #min_y = -min_y
        #step = -step

    print("Number of points in hemossphere: ",len(xyz))
    with open('Ellipsoid.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        for pos in xyz:
            writer.writerow(pos)

    print("path generated", len(xyz))
    
    DataAll1D = np.loadtxt("Ellipsoid.csv", delimiter=",")

    # create 2d x,y grid (both X and Y will be 2d)
    X, Y = np.meshgrid(DataAll1D[:,0], DataAll1D[:,1])

    # repeat Z to make it a 2d grid
    Z = np.tile(DataAll1D[:,2], (len(DataAll1D[:,2]), 1))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(X, Y, Z)

    plt.show()


    """for i in range(len(xyz)):
        x = xyz[i][0] * 0.001
        y = xyz[i][1] * 0.001
        z = xyz[i][2] * 0.001
        rx = -np.deg2rad(rpy[i][0])
        ry = np.deg2rad(rpy[i][1])
        rz = np.deg2rad(rpy[i][2])"""
