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


def runTesting(OPCUA_client, ros_client, img_amount, test_id, lightcolors, backlight, lightbar, cameralight, obj_hlw, viewpoint, run):
    # Declaring max and min variables
    
    gain_max = 4
    gain_min = 0
    exposure_max = 600
    exposure_min = 100
    center = [0.367, 0.120, 0.154]
    light_bar_failed = False
    # Compute the number of iteration steps for images.
    # If the lightbar is off we have one less loop to iterate trough and iteration steps for images will therefore be calculated differently.
    if lightbar == "off":
        x = (img_amount ** (1/2))
    else:
        x = (img_amount ** (1/3))
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

    # Run the nedsted for loop and iterate over the routes, gain and exposure steps.
    for camera_i in camera_route:
        barlightprofile.angle = 90
        OPCUA.setParameters(OPCUA_client, cameraprofile, barlightprofile, backlightprofile)
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
            delta_x = (cameraarm_setup.xPos - (center[0]))
            delta_y = (cameraarm_setup.yPos - (center[1]))
            delta_z = (cameraarm_setup.zPos - (center[2]+viewpoint))
            distance = sqrt(pow(delta_x, 2)+pow(delta_y, 2)+pow(delta_z, 2))*1000
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
                    for color in lightcolors:
                        if backlight == "on":
                            backlightprofile.flash_color = int(color)
                        else:
                            backlightprofile.flash_color = 0
                        if lightbar == "on":
                            barlightprofile.flash_color = int(color)
                            barlightprofile.angle = 90
                        else:
                            barlightprofile.flash_color = 0
                        if cameralight == "on":
                            cameraprofile.flash_color_camera = int(color)
                            if cameraprofile.flash_color_camera == 100:
                                cameraprofile.ir_filter = 1
                            else:
                                cameraprofile.ir_filter = 0
                        else:
                            cameraprofile.flash_color_camera = 0

                        for exposure_i in np.arange(exposure_min, exposure_max, exposure_steps):
                            if run[0] == False:
                                break
                            run[7] = run[7]+1
                            #print("We reached the innr loops")
                            # TODO Step4: Setup XML file and send to PLC with OPCUA

                            cameraprofile.gain_level = int(1)
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
                            if run[7] == 1:
                                print("Long trigger")
                                OPCUA.setTrigger(OPCUA_client)
                                time.sleep(1)
                                OPCUA.setTrigger(OPCUA_client)
                            else:
                                OPCUA.setTrigger(OPCUA_client)
                                time.sleep(0.1)
                                OPCUA.setTrigger(OPCUA_client)
                            print("Triggered camera")

                            while True:
                                time.sleep(0.1)
                                if OPCUA.readValue(OPCUA_client, "hw.in.camera.imgAcqReady"):
                                    break

                            # TODO Step6: Retrieve image from the cameras URL.
                            ih.getURLImage(test_id, test_id, str(run[7]))

                            # If database table does not exit, create it
                            database = mysql.connector.connect(
                                host="85.191.222.184", user="br_user", password="br_user", database="brVision")
                            cursor = database.cursor()
                            # if not checkTableExists(database, "images"):
                            try:
                                cursor.execute("""CREATE TABLE `images` (
                                `id` int NOT NULL AUTO_INCREMENT, `test_id` varchar(255) DEFAULT NULL, `path` varchar(1024) DEFAULT NULL,
                                `run` smallint unsigned DEFAULT NULL, `camera_gainLevel` int unsigned DEFAULT NULL,
                                `camera_focusScale` int unsigned DEFAULT NULL, `camera_exposureTime` int unsigned DEFAULT NULL,
                                `camera_flashColor` tinyint unsigned DEFAULT NULL, `camera_chromaticLock` tinyint(1) DEFAULT NULL,
                                `camera_irFilter` tinyint(1) DEFAULT NULL, `camera_x` float DEFAULT NULL, `camera_y` float DEFAULT NULL,
                                `camera_z` float DEFAULT NULL, `camera_yaw` float DEFAULT NULL, `camera_pitch` float DEFAULT NULL,
                                `camera_roll` float DEFAULT NULL, `barLight_exposureTime` int unsigned DEFAULT NULL,
                                `barLight_flashColor` int unsigned DEFAULT NULL, `barLight_angle` float DEFAULT NULL, `barLight_x` float DEFAULT NULL,
                                `barLight_y` float DEFAULT NULL, `barLight_z` float DEFAULT NULL, `barLight_yaw` float DEFAULT NULL,
                                `barLight_pitch` float DEFAULT NULL, `barLight_roll` float DEFAULT NULL,
                                `backLight_exposureTime` int unsigned DEFAULT NULL, `backLight_flashColor` int unsigned DEFAULT NULL,
                                `passTest` tinyint(1) DEFAULT 0, PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
                                """)
                            except:
                                print("Table exists, uploading data")

                            # Upload settings to database
                            cursor.execute("""INSERT INTO images (test_id, path, run, camera_gainLevel, camera_focusScale, camera_exposureTime, 
                            camera_flashColor, camera_chromaticLock, camera_irFilter, camera_x, camera_y, camera_z, camera_yaw, camera_pitch, 
                            camera_roll, barLight_exposureTime, barLight_flashColor, barLight_angle, barLight_x, barLight_y, barLight_z, 
                            barLight_yaw, barLight_pitch, barLight_roll, backLight_exposureTime, backLight_flashColor) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                                           (test_id, "/" + test_id + "/" + test_id + str(
                                               run[7]) + ".jpg", run[7], cameraprofile.gain_level, cameraprofile.focus_scale,
                                               cameraprofile.exposure_time_camera, cameraprofile.flash_color_camera, cameraprofile.chromatic_lock,
                                               cameraprofile.ir_filter, cameraarm_setup.xPos, cameraarm_setup.yPos, cameraarm_setup.zPos,
                                               cameraarm_setup.yaw, cameraarm_setup.pitch, cameraarm_setup.roll, barlightprofile.exposure_time,
                                               barlightprofile.flash_color, barlightprofile.angle, lightarm_setup.xPos, lightarm_setup.yPos,
                                               lightarm_setup.zPos, lightarm_setup.yaw, lightarm_setup.pitch, lightarm_setup.roll,
                                               backlightprofile.exposure_time, backlightprofile.flash_color))
                            database.commit()
                            cursor.close()

                        else:
                            print("Robotlightbar failed to move to position.")
        else:
            print("Robotcam failed to move to new position.")
    print(i)
    test_state = False
    return test_state
