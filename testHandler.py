import numpy as np
import math
import XMLParser as xmlp
import controller as con

def prepareTesting(img_amount, foldername):
    #Declaring max and min variables
    gain_max = 4
    gain_min = 0
    exposure_max = 10000
    exposure_min = 0
    #Compute the number of iteration steps for images.
    x = math.sqrt(img_amount)
    #print(x)
    #Compute the iteration steps in gain levels and exposure time.
    gain_steps = (gain_max-gain_min)/(img_amount/x)
    exposure_steps = (exposure_max-exposure_min)/(img_amount/x)
    #print(gain_steps, exposure_steps)
    i = 0
    #Run the double for loop and iterate over the gain and exposure steps.
    for gain_i in np.arange(gain_min, gain_max, gain_steps):
        for exposure_i in np.arange(exposure_min, exposure_max, exposure_steps):
            i = i+1
            cameraprofile = con.CameraProfile()
            cameraprofile.gain_level = gain_i
            cameraprofile.exposure_time_camera = exposure_i

            barlightprofile = con.BarLightProfile()
            barlightprofile.exposure_time = exposure_i

            backlightprofile = con.BackLightProfile()
            backlightprofile.exposure_time = exposure_i

            #Create XML data.
            xmlData = xmlp.cameraProfilerToXML(cameraprofile, barlightprofile, backlightprofile)
            #Save XML data.
            xmlp.parseXMLtoFileAndWrite(xmlData, foldername, foldername, str(i))

    test_state = False
    return test_state
    
