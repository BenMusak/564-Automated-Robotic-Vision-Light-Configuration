import numpy as np
import math
import XMLParser as xmlp
import controller as con
import rosbridge as rb
import imageHandler as ih


def prepareTesting(OPCUA_client,ros_client, img_amount, foldername, lightcolor, backlight, lightbar, cameralight, obj_hlw):
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
    camera_steps = gain_steps
    light_steps = gain_steps
    light_min = gain_min #This will be changed later.
    light_max = gain_max #This will be changed later.
    #If the lightbar is off, we wont to skip the loop for it,
    #which we can do by setting the light_steps higher than the stop value for np.arange
    if lightbar == "off":
        light_steps = gain_max + 1 #
    else:
        light_steps = gain_steps
    print(gain_steps, exposure_steps)
    
     #TODO: generate route for camera and light. Should be returned as a list of [x,y,z,rotx,roty,rotz], that we can then iterate trough

    i = 0
    #Run the double for loop and iterate over the gain and exposure steps.
    for camera_i in np.arange(gain_min, gain_max, camera_steps): #TODO: Need to be changed, so that it iterates trough the returned list from plan_camera_route.
        #TODO Step0: Move the UR5 light robot in a safe position, so the UR5 cam can move to new position after.
        rb.ROS_SendGoal(ros_client, 10,10,10,10,10,10,"lightbar_robot") #Real values should come from route_planner.py
        #TODO Step1: Move UR5 cam robot.
        rb.ROS_SendGoal(ros_client, 10,10,10,10,10,10,"camera_robot")
        cameraarm_setup = con.CameraSetupProfile()
        #TODO Step2:  focus scale.
        #Maybe even receive pose for the robot arm.
        for light_i in np.arange(gain_min, gain_max, light_steps): #TODO: Need to be changed, so that it iterates trough the returned list from plan_light_route.
            #TODO Step3: Move UR5 barlight robot and only if variable lightbar == "on.
            rb.ROS_SendGoal(ros_client, 10,10,10,10,10,10,"lightbar_robot")
            lightarm_setup = con.barLightSetupProfile()
            #Move on when movement is confirmed.
            #Maybe even receive pose for the robot arm.
            for gain_i in np.arange(gain_min, gain_max, gain_steps):
                for exposure_i in np.arange(exposure_min, exposure_max, exposure_steps):
                    i = i+1
                    #TODO Step4: Setup XML file and send to PLC with OPCUA
                    cameraprofile = con.CameraProfile()
                    cameraprofile.gain_level = gain_i
                    cameraprofile.exposure_time_camera = exposure_i

                    barlightprofile = con.BarLightProfile()
                    barlightprofile.exposure_time = exposure_i

                    backlightprofile = con.BackLightProfile()
                    backlightprofile.exposure_time = exposure_i
                    #Create XML data.
                    #xmlData = xmlp.profilerToXML(cameraprofile, barlightprofile, backlightprofile)

                    #TODO Step5: Wait for confirmation from PLC that images was captures successfully.

                    #TODO Step6: Retrieve image from the cameras URL.
                    #ih.getURLImage(foldername, foldername, str(i))
                    #TODO Step7: Log XML data.
                    #Save XML data.
                    #xmlp.parseXMLtoFileAndWrite(xmlData, foldername, foldername, str(i))
    print(i)
    test_state = False
    return test_state
    
