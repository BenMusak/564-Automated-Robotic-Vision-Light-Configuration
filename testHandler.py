import numpy as np
import math
import XMLParser as xmlp
import controller as con
import rosbridge as rb
import imageHandler as ih
import route_planner as rp
import OPCUA
import setupParameters as sp
import time


def prepareTesting(OPCUA_client,ros_client, img_amount, foldername, lightcolor, backlight, lightbar, cameralight, obj_hlw, viewpoint):
    #Declaring max and min variables
    gain_max = 4
    gain_min = 0
    exposure_max = 10000
    exposure_min = 0
    #Compute the number of iteration steps for images.
    #If the lightbar is off we have one less loop to iterate trough and iteration steps for images will therefore be calculated differently.
    if lightbar == "off":
        x = (img_amount ** (1/3))
    else:
        x = (img_amount ** (1/4))
    print(x)
    #Compute the iteration steps in gain levels and exposure time.
    gain_steps = (gain_max-gain_min)/x
    exposure_steps = (exposure_max-exposure_min)/x
    #If the lightbar is off, we wont to skip the loop for it,
    #which we can do by setting the light_steps higher than the stop value for np.arange
    if lightbar == "off":
        light_steps = gain_max + 1 #
    else:
        light_steps = gain_steps
    print(gain_steps, exposure_steps)
    
     #TODO: generate route for camera and light. Should be returned as a list of [x,y,z,rotx,roty,rotz], that we can then iterate trough
    if lightbar == "off":
        light_route = []
        light_route.append(1)
    else:
        light_route = rp.plan_light_route(viewpoint, obj_hlw, True, x, x)

    camera_route = rp.plan_camera_route(viewpoint, obj_hlw, True, x, x)

    i = 0
    #Run the double for loop and iterate over the gain and exposure steps.
    for camera_i in camera_route: #TODO: Need to be changed, so that it iterates trough the returned list from plan_camera_route.
        #TODO Step0: Move the UR5 light robot in a safe position, so the UR5 cam can move to new position after.
        rb.ROS_SendGoal(ros_client, 1, -0.16, 0.75, "lightbar_robot", viewpoint, obj_hlw) #Real values should come from route_planner.py
        #TODO Step1: Move UR5 cam robot.
        input()
        print("Sending coordinates", camera_i, " to the camera.")
        rb.ROS_SendGoal(ros_client, camera_i[0],camera_i[1],camera_i[2],"camera_robot", viewpoint, obj_hlw)
        input()
        #cameraarm_setup = con.CameraSetupProfile()
        #TODO Step2:  focus scale.
        #Maybe even receive pose for the robot arm.
        for light_i in light_route: #TODO: Need to be changed, so that it iterates trough the returned list from plan_light_route.
            #TODO Step3: Move UR5 barlight robot and only if variable lightbar == "on.
            if lightbar != "off":
                rb.ROS_SendGoal(ros_client, light_i[0],light_i[1],light_i[2],"lightbar_robot", viewpoint, obj_hlw)
                #lightarm_setup = con.barLightSetupProfile()
            #Move on when movement is confirmed.
            #Maybe even receive pose for the robot arm.
            for gain_i in np.arange(gain_min, gain_max, gain_steps):
                for exposure_i in np.arange(exposure_min, exposure_max, exposure_steps):
                    i = i+1
                    """print("We reached the innr loops")
                    #TODO Step4: Setup XML file and send to PLC with OPCUA

                    if cameralight != "off":
                        cameraprofile = con.CameraProfile()
                    else:
                        cameraprofile = con.CameraProfile()
                        cameraprofile.flash_color_camera = 1
                        cameraprofile.ir_filter = False
                        cameraprofile.focus_scale = 230
                        cameraprofile.chromatic_lock = False
                    cameraprofile.gain_level = int(gain_i)
                    cameraprofile.exposure_time_camera = int(exposure_i)
                    #-0.00021*x^2 + 0.908*x + 4.6845

                    if lightbar != "off":
                        barlightprofile = con.BarLightProfile()
                        barlightprofile.exposure_time = int(exposure_i)
                        barlightprofile.flash_color = 0
                    else:
                        barlightprofile = con.BarLightProfile()
                        barlightprofile.flash_color = 0
                        barlightprofile.exposure_time = 0
                        barlightprofile.angle = 0

                    if backlight != "off":
                        backlightprofile = con.BackLightProfile()
                        backlightprofile.exposure_time = int(exposure_i)
                        backlightprofile.flash_color = 0
                    else: 
                        backlightprofile = con.BackLightProfile()
                        backlightprofile.exposure_time = 0
                        backlightprofile.flash_color = 0

                    #Create XML data.
                    #xmlData = xmlp.profilerToXML(cameraprofile, barlightprofile, backlightprofile)
                    #cameraProfile, barLightProfile1, backlightProfile = sp.setParameters()

                    #TODO Step5: Wait for confirmation from PLC that images was captures successfully.
                    OPCUA.getRootNode(OPCUA_client)
                    OPCUA.setParameters(OPCUA_client, cameraprofile, barlightprofile, backlightprofile)
                    OPCUA.setTrigger(OPCUA_client)
                    print("Triggered camera")
                    
                    time.sleep(3)

                    #TODO Step6: Retrieve image from the cameras URL.
                    ih.getURLImage(foldername, foldername, str(i))
                    #TODO Step7: Log XML data.
                    #Save XML data.
                    #xmlp.parseXMLtoFileAndWrite(xmlData, foldername, foldername, str(i))"""
    print(i)
    test_state = False
    return test_state
    
