import numpy as np
import math
import controller as con
import rosbridge as rb
import imageHandler as ih
import route_planner as rp
import OPCUA
import setupParameters as sp
import time
from math import sqrt
import mysql.connector


def checkTableExists(dbcon, tablename) -> bool:
    cursor = dbcon.cursor()
    cursor.execute("""
    SELECT * FROM information_schema.tables WHERE table_name = '{}'
    """.format(tablename))
    if cursor.fetchone()[0] == 1:
        cursor.close()
        return True

    cursor.close()
    return False


def get_color_nr(argument):
    switcher = {
        "Red": 1,
        "Blue": 3,
        "White": 99,
        "IR": 100
    }
    return switcher.get(argument, 0)  # Return 0 if chosen color does no exist.


def runTesting(OPCUA_client, ros_client, img_amount, foldername, lightcolor, backlight, lightbar, cameralight, obj_hlw, viewpoint, run):
    # Declaring max and min variables
    gain_max = 4
    gain_min = 0
    exposure_max = 1000
    exposure_min = 0
    center = [0.367, 0.120, 0.154]
    light_bar_failed = False
    # Compute the number of iteration steps for images.
    # If the lightbar is off we have one less loop to iterate trough and iteration steps for images will therefore be calculated differently.
    if lightbar == "off":
        x = (img_amount ** (1/3))
    else:
        x = (img_amount ** (1/4))
    print("Number of steps for each loop = ", x)
    # Convert the iteration steps to gain levels and exposure time.
    gain_steps = (gain_max-gain_min)/x
    exposure_steps = (exposure_max-exposure_min)/x

    # If the lightbar is off we dont need to move the lightbar robotarm. We therefore skip the loop.
    if lightbar == "off":
        light_route = []
        light_route.append(1)
    else:
        light_route = rp.plan_light_route(viewpoint, obj_hlw, False, x, x)

    # Camera route need to run no matter what.
    camera_route = rp.plan_camera_route(viewpoint, obj_hlw, False, x, x)

    i = 0  # Just for keeping count of total iteration steps.

    # Setup profiles for parameters that are not iterated trough.
    cameraprofile = con.CameraProfile()
    barlightprofile = con.BarLightProfile()
    backlightprofile = con.BackLightProfile()
    lightarm_setup = con.barLightSetupProfile()
    cameraarm_setup = con.CameraSetupProfile()

    if backlight == "on":
        backlightprofile.flash_color = get_color_nr(lightcolor)
    else:
        backlightprofile.flash_color = 0
    if lightbar == "on":
        barlightprofile.flash_color = get_color_nr(lightcolor)
        barlightprofile.angle = 90
    else:
        barlightprofile.flash_color = 0
    if cameralight == "on":
        cameraprofile.flash_color_camera = get_color_nr(lightcolor)
        if cameraprofile.flash_color_camera == 100:
            cameraprofile.ir_filter = 1
    else:
        cameraprofile.flash_color_camera = 0

    # Run the nedsted for loop and iterate over the routes, gain and exposure steps.
    for camera_i in camera_route:
        # Move UR5 light to homing position.
        rb.ROS_SendGoal(ros_client, 1, -0.16, 0.75,
                        "lightbar_robot", viewpoint, obj_hlw)
        # input()
        print("Sending coordinates", camera_i, " to the camera.")
        run[1] = camera_i[0]
        run[2] = camera_i[1]
        run[3] = camera_i[2]
        # Move UR5 cam.
        UR5_cam_data = rb.ROS_SendGoal(
            ros_client, camera_i[0], camera_i[1], camera_i[2], "camera_robot", viewpoint, obj_hlw)
        if run[0] == False:
            break
        if UR5_cam_data["status"]:
            cameraarm_setup.xPos = UR5_cam_data["x"]
            cameraarm_setup.yPos = UR5_cam_data["y"]
            cameraarm_setup.zPos = UR5_cam_data["z"]
            cameraarm_setup.yaw = UR5_cam_data["rotx"]
            cameraarm_setup.pitch = UR5_cam_data["roty"]
            cameraarm_setup.roll = UR5_cam_data["rotz"]
            # Computing the distance between object and camera lens.
            delta_x = (cameraarm_setup.xPos - (center[0]+obj_hlw[2]))
            delta_y = (cameraarm_setup.yPos - (center[1]+obj_hlw[1]))
            delta_z = (cameraarm_setup.zPos - (center[2]+viewpoint))
            distance = sqrt(pow(delta_x, 2)+pow(delta_y, 2)+pow(delta_z, 2))
            # Computing the focus. Normally this would be equal to distance, but this camera is not calibrated,
            # so we need to compensate with the following formula:
            cameraprofile.focus_scale = int(-0.00021 *
                                            pow(distance, 2) + 0.908*distance + 4.6845)
            # TODO: Need to be changed, so that it iterates trough the returned list from plan_light_route.
            for light_i in light_route:
                if lightbar == "on":
                    if run[0] == False:
                        break
                    run[4] = light_i[0]
                    run[5] = light_i[1]
                    run[6] = light_i[2]
                    UR5_light_data = rb.ROS_SendGoal(
                        ros_client, light_i[0], light_i[1], light_i[2], "lightbar_robot", viewpoint, obj_hlw)
                    if UR5_light_data["status"]:
                        lightarm_setup.xPos = UR5_light_data["x"]
                        lightarm_setup.yPos = UR5_light_data["y"]
                        lightarm_setup.zPos = UR5_light_data["z"]
                        lightarm_setup.yaw = UR5_light_data["rotx"]
                        lightarm_setup.pitch = UR5_light_data["roty"]
                        lightarm_setup.roll = UR5_light_data["rotz"]
                        light_bar_failed = False
                    else:
                        light_bar_failed = True

                # Move on when movement is confirmed.
                # Maybe even receive pose for the robot arm.
                if light_bar_failed == False:
                    for gain_i in np.arange(gain_min, gain_max, gain_steps):
                        for exposure_i in np.arange(exposure_min, exposure_max, exposure_steps):
                            if run[0] == False:
                                break
                            run[7] = run[7]+1
                            #print("We reached the innr loops")
                            # TODO Step4: Setup XML file and send to PLC with OPCUA

                            cameraprofile.gain_level = int(gain_i)
                            cameraprofile.chromatic_lock = 1
                            cameraprofile.exposure_time_camera = int(
                                exposure_i)

                            if lightbar == "on":
                                barlightprofile.exposure_time = int(exposure_i)

                            if backlight == "on":
                                backlightprofile.exposure_time = int(
                                    exposure_i)

                            # TODO Step5: Wait for confirmation from PLC that images was captures successfully.
                            OPCUA.getRootNode(OPCUA_client)
                            OPCUA.setParameters(
                                OPCUA_client, cameraprofile, barlightprofile, backlightprofile)
                            OPCUA.setTrigger(OPCUA_client)
                            print("Triggered camera")

                            time.sleep((exposure_i*(pow(10, -6)))*14)
                            # print((exposure_i*(pow(10,-6)))*14)
                            # TODO Step6: Retrieve image from the cameras URL.
                            ih.getURLImage(foldername, foldername, str(run[7]))

                            # If database table does not exit, create it
                            database = mysql.connector.connect(
                                host="localhost", user="andr", password="1212", database="brmysql")
                            cursor = database.cursor()
                            if not checkTableExists(database, "images"):
                                cursor.execute("""CREATE TABLE images (id INT AUTO_INCREMENT PRIMARY KEY, img_name VARCHAR(255), path VARCHAR(1024), 
                                run SMALLINT UNSIGNED, camera_gainLevel TINYINT UNSIGNED, camera_focusScale INT UNSIGNED, 
                                camera_exposureTime SMALLINT UNSIGNED, camera_flashColor TINYINT UNSIGNED, camera_chromaticLock BOOLEAN, 
                                camera_irFilter BOOLEAN, camera_x INT, camera_y INT, camera_z INT, camera_yaw SMALLINT, camera_pitch SMALLINT, 
                                camera_roll SMALLINT, barLight_exposureTime INT UNSIGNED, barLight_flashColor TINYINT UNSIGNED, barLight_angle SMALLINT, 
                                barLight_x INT, barLight_y INT, barLight_z INT, barLight_yaw SMALLINT, barLight_pitch SMALLINT, barLight_roll SMALLINT, 
                                backLight_exposureTime INT UNSIGNED, backLight_flashColor TINYINT UNSIGNED, passTest BOOLEAN)""")

                            # Upload settings to database
                            cursor.execute("""INSERT INTO images (test_id, path, run, camera_gainLevel, camera_focusScale, camera_exposureTime, 
                                           camera_flashColor, camera_chromaticLock, camera_irFilter, camera_x, camera_y, camera_z, camera_yaw, camera_pitch, 
                                           camera_roll, barLight_exposureTime, barLight_flashColor, barLight_angle, barLight_x, barLight_y, barLight_z, 
                                           barLight_yaw, barLight_pitch, barLight_roll, backLight_exposureTime, backLight_flashColor) VALUES (
                                           {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, 
                                           {})""".format(foldername, "B_R_Illumination/static/images/" + foldername + "/" + foldername + str(
                                run[7]) + ".jpg", run[7],
                                cameraprofile.gain_level, cameraprofile.focus_scale, cameraprofile.exposure_time_camera, cameraprofile.flash_color_camera,
                                cameraprofile.chromatic_lock, cameraprofile.ir_filter, cameraarm_setup.xPos, cameraarm_setup.yPos, cameraarm_setup.zPos,
                                cameraarm_setup.yaw, cameraarm_setup.pitch, cameraarm_setup.roll, barlightprofile.exposure_time, barlightprofile.flash_color,
                                barlightprofile.angle, lightarm_setup.xPos, lightarm_setup.yPos, lightarm_setup.zPos, lightarm_setup.yaw, lightarm_setup.pitch,
                                lightarm_setup.roll, backlightprofile.exposure_time, backlightprofile.flash_color))
                            cursor.close()

                        else:
                            print("Robotlightbar failed to move to position.")
        else:
            print("Robotcam failed to move to new position.")
    print(i)
    test_state = False
    return test_state
