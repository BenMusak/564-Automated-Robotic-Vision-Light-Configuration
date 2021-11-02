# This macro will save a time stamp and robot joints each 50 ms
from math import atan, pi, sqrt
import threading

from robodk.robodk import *
from robolink import *      # API to communicate with RoboDK for simulation and offline/online programming
from robodk import *        # Robotics toolbox for industrial robots
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
    
    RDK_StationList = RDK.getOpenStations()
    RDK_StationNames = []
    # Save all station names in a list.
    for station in RDK_StationList:
        RDK_StationNames.append(station.Name())
    # Loading the RoboDK work station if it is not already loaded.
    if "Work_station" not in RDK_StationNames:
        RDK.AddFile("Work_station.rdk")
    # get a robot
    robot = RDK.Item('UR5_BAR_LIGHT', ITEM_TYPE_ROBOT)
    robot1 = RDK.Item('UR5_CAM', ITEM_TYPE_ROBOT)
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
    return robot, robot1, RDK

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

def startHemisPath(robot, run, RDK):
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

    inspection_center_xyz = [400, 0, 155] # Reference frame (Center of Hemisphere)
    step = 0.5

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
    for x_it in np.arange(max_x, min_x, -0.1):
        for y_it in np.arange(min_y, max_y, step):
            if sqrt(pow(x_it, 2) + pow(y_it, 2)) <= a:
                try:
                    # Computing the x, y and z coordinates of the points in the hemisphere wrt. to the robot frame
                    # (we multiply with 50 just to make the hemisphere a bit larger)
                    z_hemsphe = sqrt(a-pow(x_it,2)-pow(y_it,2))*50+inspection_center_xyz[2]
                    x_hemsphe = x_it*50 + inspection_center_xyz[0] # We add 500 to move the hemisphere a bit away from origon.
                    y_hemsphe = y_it*50 + inspection_center_xyz[1]

                    ## Compute roll, pitch and yaw of the camera with fixed angles wrt. the robot frame.
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
                        print("computiation fail in fixed x angle between camera and inspection object")

                    if y_vect > 0 and z_vect < 0:
                        rot_x = atan(y_vect/(-sqrt(pow(z_vect,2)+pow(x_vect,2))))/pi*180-90
                    elif y_vect < 0 and z_vect < 0:
                        rot_x = -atan((-sqrt(pow(z_vect,2)+pow(x_vect,2)))/y_vect)/pi*180
                    elif y_vect < 0 and z_vect > 0:
                        rot_x = atan(z_vect/y_vect)/pi*180
                    elif y_vect > 0 and z_vect > 0:
                        rot_x = atan(y_vect/z_vect)/pi*180
                    else:
                        print("computiation fail in fixed x angle between camera and inspection object")

                    rot_z = 0
                    rot_y1 = rot_y - 90
                    rot_x1 = 0

                    xyz.append([x_hemsphe,y_hemsphe,z_hemsphe])
                    
                    # Fixed rotation
                    pose_y_rot = transl(x_hemsphe,y_hemsphe,z_hemsphe)*rotz(rot_z*pi/180)*roty(rot_y1*pi/180)*rotx(rot_x1*pi/180)

                    rot_y2 = 0
                    rot_x2 = rot_x + 90

                    pose_final_rot = pose_y_rot * rotx(rot_x2*pi/180)*roty(rot_y2*pi/180)*rotz(rot_z*pi/180)
                    
                    xyzrpw.append(pose_final_rot)
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
    with open('Hemisphere.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        for pos in xyz:
            writer.writerow(pos)

    i = 0
    #tool_cam = RDK.Item("Camera",ITEM_TYPE_TOOL )
    tool_cam = robot.PoseTool()
    frame_cam = RDK.Item("CAM", ITEM_TYPE_FRAME)
    #refframe_cam = frame_cam.PoseFrame()
    #robot.setPoseTool(tool_cam)
    robot.setPoseFrame(frame_cam)
    # We run the for loop, where we send the coordinates to the robot.
    for pos in xyzrpw:

        # Stop the process. Here Run simulates a pointer.
        if run[0] != True:
            break
            print("Ending the loop")
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
        new_robot_position = pos
        #*rotz(rot_x)
        #continue

        # calculate the new robot joints
        new_robot_joints = robot.SolveIK(new_robot_position, tool = tool_cam)

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
        time.sleep(0.01)
        i += 1

thread = threading.Thread(target=startHemisPath)
thread.start()

def homePose(robot, run, RDK):
    #left button
    x_home = 460
    y_home = 0
    z_home = 500
    rot_x_home = 0
    rot_y_home = 0
    rot_z_home = 0

    xyzrpw = (transl(x_home,y_home,z_home)*rotz(rot_z_home*pi/180)*roty(rot_y_home*pi/180)*rotx(rot_x_home*pi/180)) #Hope position pose

    # set which frame is tool frame
    tool_cam = robot.PoseTool()
    frame_cam = RDK.Item("Camera", ITEM_TYPE_FRAME)
    robot.setPoseFrame(frame_cam)

    # get the robot joints
    robot_joints = robot.Joints()

    # get the robot position from the joints (calculate forward kinematics)
    robot_position = robot.SolveFK(robot_joints)

    # get the robot configuration (robot joint state)
    robot_config = robot.JointsConfig(robot_joints)

    # calculate the new robot position
    new_robot_position = xyzrpw

    # calculate the new robot joints
    home_robot_joints = robot.SolveIK(new_robot_position, tool = tool_cam)

    if len(home_robot_joints.tolist()) < 6:
        print("No robot solution!! The new position is too far, out of reach or close to a singularity")

    # calculate the robot configuration for the new joints
    new_robot_config = robot.JointsConfig(home_robot_joints)

    if robot_config[0] != new_robot_config[0] or robot_config[1] != new_robot_config[1] or robot_config[2] != \
            new_robot_config[2]:
        print("Warning!! Robot configuration changed!! This will lead to unextected movements!")
        print(robot_config)
        print(new_robot_config)

    # move the robot joints to the new position
    robot.MoveJ(home_robot_joints)

def homePose2(robot, run, RDK):
    #left button
    x_home = 460
    y_home = 0
    z_home = 500
    rot_x_home = -90
    rot_y_home = -90
    rot_z_home = 0

    xyzrpw = (transl(x_home,y_home,z_home)*rotz(rot_z_home*pi/180)*roty(rot_y_home*pi/180)*rotx(rot_x_home*pi/180)) #Hope position pose

    # set which frame is tool frame
    tool_cam = robot.PoseTool()
    frame_cam = RDK.Item("Camera", ITEM_TYPE_FRAME)
    robot.setPoseFrame(frame_cam)

    # get the robot joints
    robot_joints = robot.Joints()

    # get the robot position from the joints (calculate forward kinematics)
    robot_position = robot.SolveFK(robot_joints)

    # get the robot configuration (robot joint state)
    robot_config = robot.JointsConfig(robot_joints)

    # calculate the new robot position
    new_robot_position = xyzrpw

    # calculate the new robot joints
    home_robot_joints = robot.SolveIK(new_robot_position, tool = tool_cam)

    if len(home_robot_joints.tolist()) < 6:
        print("No robot solution!! The new position is too far, out of reach or close to a singularity")

    # calculate the robot configuration for the new joints
    new_robot_config = robot.JointsConfig(home_robot_joints)

    if robot_config[0] != new_robot_config[0] or robot_config[1] != new_robot_config[1] or robot_config[2] != \
            new_robot_config[2]:
        print("Warning!! Robot configuration changed!! This will lead to unextected movements!")
        print(robot_config)
        print(new_robot_config)

    # move the robot joints to the new position
    robot.MoveJ(home_robot_joints)

def homePose3(robot, run, RDK):
    #left button
    x_home = 460
    y_home = 0
    z_home = 500
    rot_x_home = -90
    rot_y_home = -90
    rot_z_home = 0

    xyzrpw = (transl(x_home,y_home,z_home)*rotx(rot_x_home*pi/180)*roty(rot_y_home*pi/180)*rotz(rot_z_home*pi/180)) #Hope position pose

    # set which frame is tool frame
    tool_cam = robot.PoseTool()
    frame_cam = RDK.Item("Camera", ITEM_TYPE_FRAME)
    robot.setPoseFrame(frame_cam)

    # get the robot joints
    robot_joints = robot.Joints()

    # get the robot position from the joints (calculate forward kinematics)
    robot_position = robot.SolveFK(robot_joints)

    # get the robot configuration (robot joint state)
    robot_config = robot.JointsConfig(robot_joints)

    # calculate the new robot position
    new_robot_position = xyzrpw

    # calculate the new robot joints
    home_robot_joints = robot.SolveIK(new_robot_position, tool = tool_cam)

    if len(home_robot_joints.tolist()) < 6:
        print("No robot solution!! The new position is too far, out of reach or close to a singularity")

    # calculate the robot configuration for the new joints
    new_robot_config = robot.JointsConfig(home_robot_joints)

    if robot_config[0] != new_robot_config[0] or robot_config[1] != new_robot_config[1] or robot_config[2] != \
            new_robot_config[2]:
        print("Warning!! Robot configuration changed!! This will lead to unextected movements!")
        print(robot_config)
        print(new_robot_config)

    # move the robot joints to the new position
    robot.MoveJ(home_robot_joints)