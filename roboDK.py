# This macro will save a time stamp and robot joints each 50 ms
import threading

from robodk.robodk import *
from robolink import *    # API to communicate with RoboDK for simulation and offline/online programming
from robodk import *      # Robotics toolbox for industrial robots
from robolink.robolink import *
from msvcrt import getch
import numpy as np
import csv
import time

def initializeRobot():
    # Enter RoboDK IP and Port
    ROBOT_IP = '192.168.87.100'
    ROBOT_PORT = 30003

    # Start RoboDK API
    RDK = Robolink()
    #RDK.setRunMode(RUNMODE_RUN_ROBOT)

    # get a robot
    robot = RDK.Item('UR5e', ITEM_TYPE_ROBOT)
    if not robot.Valid():
        print("No robot in the station. Load a robot first, then run this program.")
        pause(5)
        raise Exception("No robot in the station!")

    #Uncomment if we want to run on real robot.
    RUN_ON_ROBOT = False


    # Important: by default, the run mode is RUNMODE_SIMULATE
    # If the program is generated offline manually the runmode will be RUNMODE_MAKE_ROBOTPROG,
    # Therefore, we should not run the program on the robot
    if RDK.RunMode() != RUNMODE_SIMULATE:
        RUN_ON_ROBOT = False

    if RUN_ON_ROBOT:
        # Update connection parameters if required:
        # robot.setConnectionParams('192.168.2.35',30000,'/', 'anonymous','')

        # Connect to the robot using default IP
        success = robot.Connect()  # Try to connect once
        # success robot.ConnectSafe() # Try to connect multiple times
        status, status_msg = robot.ConnectedState()
        if status != ROBOTCOM_READY:
            # Stop if the connection did not succeed
            print(status_msg)
            raise Exception("Failed to connect: " + status_msg)

        # This will set to run the API programs on the robot and the simulator (online programming)
        RDK.setRunMode(RUNMODE_RUN_ROBOT)


    print('Using robot: %s' % robot.Name())
    print('Use the arrows (left, right, up, down), Q and A keys to move the robot')
    print('Note: This works on console mode only, you must run the PY file separately')
    return robot

def moveRobot(robot, key):
    speed_ms = 0.300
    speed_rads  = 0.750
    ccel_mss   = 3.000
    accel_radss = 1.200
    blend_radius_m = 0.001
    # define the move increment
    move_speed = 10

    #while True:
        #key = (ord(getch()))
    move_direction = [0, 0, 0]
    # print(key)
    if key == 75:
        print('arrow left (Y-)')
        move_direction = [0, -1, 0]
    elif key == 77:
        print('arrow right (Y+)')
        move_direction = [0, 1, 0]
    elif key == 72:
        print('arrow up (X-)')
        move_direction = [-1, 0, 0]
    elif key == 80:
        print('arrow down (X+)')
        move_direction = [1, 0, 0]
    elif key == 113:
        print('Q (Z+)')
        move_direction = [0, 0, 1]
    elif key == 97:
        print('A (Z-)')
        move_direction = [0, 0, -1]

    # make sure that a movement direction is specified
    #if norm(move_direction) <= 0:
    # calculate the movement in mm according to the movement speed
    xyz_move = mult3(move_direction, move_speed)

    # get the robot joints
    robot_joints = robot.Joints()

    # get the robot position from the joints (calculate forward kinematics)
    robot_position = robot.SolveFK(robot_joints)

    # get the robot configuration (robot joint state)
    robot_config = robot.JointsConfig(robot_joints)

    # calculate the new robot position
    new_robot_position = transl(xyz_move) * robot_position
    #continue

    # calculate the new robot joints
    new_robot_joints = robot.SolveIK(new_robot_position)
    if len(new_robot_joints.tolist()) < 6:
        print("No robot solution!! The new position is too far, out of reach or close to a singularity")
        #continue

    # calculate the robot configuration for the new joints
    new_robot_config = robot.JointsConfig(new_robot_joints)

    if robot_config[0] != new_robot_config[0] or robot_config[1] != new_robot_config[1] or robot_config[2] != \
            new_robot_config[2]:
        print("Warning!! Robot configuration changed!! This will lead to unextected movements!")
        print(robot_config)
        print(new_robot_config)

    # move the robot joints to the new position
    robot.MoveJ(new_robot_joints)
    key = 0

        # robot.MoveL(new_robot_joints)

def startHemisPath(robot):
    # The goal here is to autogenerate a path in the shape of an hemisphere (with the object in the center),
    # that the robot can follow. We can then change the size of the hemisphere to
    # test from different distances. Furthermore, the lights should always point at the object,
    # So in some way we must change the Rotation matrix of the tcp, so that the z-axis always points to
    # the center of the hemisphere.

    a = 5 # Size of hemisphere (half sphere)
    max_x = sqrt(a-pow(0,2)-pow(0,2)) # we find out what the max x-coordinate is (radius)
    max_y = max_x # Since we are dealing with an hemisphere
    min_y = -max_y # Min_x must therefore be the oposite of max_x (asuming that the center of the hemisphere is y=0)
    min_x = -max_x
    xyz = [] # List for only XYZ coordinates.
    xyzrpw = [] # List that contains the XYZ Coordinate and Roll Pitch Yaw Coordinates.
    i = 0 # Used for indexing xyzrpw list.

    base_xyz = [500, 0, 0] # Reference frame (Center of Hemisphere)
    step = 0.1

# Generating the 3D points for an hemisphere
# We iterate over all y-coordinate before we change to new x-coordinate, thereafter
# we also change the polarity of the min_y, max_y and step variables.
# This results in a back and forth movement
# Example: "For the first x-coordinate, the y-coordinates start at negative and end at positive.
# For the second x-coordinate, the y-coordinates start at positive and end at negative."
#
# TODO:
#   - The Z axis of the tcp should always point at the center of the hemisphere.
#       - I have tried to do this by finding the angle between the center of the hemisphere and
#         the point on an arbitrary point on the hemisphere, but so far this can only give me
#         the pitch and yaw angle and not roll. Furthermore, the found pitch and yaw seems to not
#         match with what it is supposed to be.
#
    for x_it in np.arange(min_x, max_x, 0.1):
        for y_it in np.arange(min_y, max_y, step):
            if sqrt(pow(x_it, 2) + pow(y_it, 2)) <= a:
                try:
                    # Computing the x, y and z coordinates
                    # (we multiply with 50 just to make the hemisphere a bit larger)
                    z = sqrt(a-pow(x_it,2)-pow(y_it,2))*50
                    x = x_it*50+500 # We add 500 to move the hemisphere a bit away from origon.
                    y = y_it*50

                    # We now compute the vector coordinates.
                    vec_x = base_xyz[0] - x
                    vec_y = base_xyz[1] - y
                    vec_z = base_xyz[2] - z

                    #We now compute roll, pitch and yaw.
                    r = 0*pi/180 # we have no way of computing roll, so we set it to zero deg.
                    #yaw = np.arcsin(-vec_y)/pi*180 # Another method
                    yaw = 180 - atan2(-vec_y,-vec_x)/pi*180
                    p = atan2(-vec_z,-vec_x)/pi*180
                    xyz.append([x,y,z])
                    # I am not completely sure in which order roll, pitch and yaw should come in
                    xyzrpw.append([x, y, z, p, -90,yaw])
                    print(xyzrpw[i])
                    i += 1
                # Using the double for loop actually results is us trying to find values that exceed
                # the hemipshere, the try except func prevents the program from stopping, when this happens.
                except:
                    print("compute error")
        max_y = -max_y
        min_y = -min_y
        step = -step
    # We now save all the coordinates in a csv file, which can me imported
    # into RoboDK by simply dragging it into the program.
    with open('test.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        for pos in xyz:
            writer.writerow(pos)

    i = 0
    # We run the for loop, where we send the coordinates to the robot.
    for pos in xyzrpw:

        # If you want to see the individual positions in RoboDk, then remove the "#" from
        # the next two lines.
        #frames.append(RDK.AddTarget(str(pos)))
        #frames[i].setPose(xyzrpw_2_pose(pos))

        # get the robot joints
        robot_joints = robot.Joints()

        # get the robot position from the joints (calculate forward kinematics)
        robot_position = robot.SolveFK(robot_joints)

        # get the robot configuration (robot joint state)
        robot_config = robot.JointsConfig(robot_joints)

        # calculate the new robot position
        #new_robot_position = transl(pos)
        #new_robot_position = transl(pos)*rotz(0*pi/180)*roty(rpy[i][1])*
        new_robot_position = xyzrpw_2_pose(pos)
        #continue

        # calculate the new robot joints
        new_robot_joints = robot.SolveIK(new_robot_position)

        if len(new_robot_joints.tolist()) < 6:
            print("No robot solution!! The new position is too far, out of reach or close to a singularity")
            continue

        # calculate the robot configuration for the new joints
        new_robot_config = robot.JointsConfig(new_robot_joints)

        if robot_config[0] != new_robot_config[0] or robot_config[1] != new_robot_config[1] or robot_config[2] != \
                new_robot_config[2]:
            print("Warning!! Robot configuration changed!! This will lead to unextected movements!")
            print(robot_config)
            print(new_robot_config)

        # move the robot joints to the new position
        robot.MoveJ(new_robot_joints)
        time.sleep(0.3)
        i += 1
