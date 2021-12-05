import xml.etree.cElementTree as ET
import os

def parseXMLtoString(data):
    stringData = ET.tostring(data).decode("utf-8")
    return stringData


def parseXMLtoStringfileAndWrite(data, folder, img_name, img_iteration):
    stringData = ET.tostring(data).decode("utf-8")
    file = open("B_R_Illumination/static/txt/" + folder + "/" + img_name + img_iteration + ".txt" )
    file.write(stringData)
    print("Done writing to file")


def parseXMLtoFileAndWrite(data, folder, img_name, img_iteration):
    elementData = ET.ElementTree(data)

    if os.path.exists("B_R_Illumination/static/XML/" + folder):
        elementData.write("B_R_Illumination/static/XML/" + folder + "/" + img_name + img_iteration + ".xml")
    else:
        os.makedirs("B_R_Illumination/static/XML/" + folder)
        elementData.write("B_R_Illumination/static/XML/" + folder + "/" + img_name + img_iteration + ".xml")
    #print("Done writing to file")


def profilerToXML(camera_profile, bar_profile, back_profile, camera_pos_profile, bar_pos_profile):
    data = ET.Element("Profiles")

    # Camera
    cameraProfile = ET.SubElement(data, "CameraProfile")
    gainC = ET.SubElement(cameraProfile, "gain")
    focusSC = ET.SubElement(cameraProfile, "focus")
    exposureC = ET.SubElement(cameraProfile, "exp_time")
    flash_cc = ET.SubElement(cameraProfile, "flash_c")
    chromaticL = ET.SubElement(cameraProfile, "chrom_L")
    irFilter = ET.SubElement(cameraProfile, "ir")
    # Set
    gainC.text = str(camera_profile.gain_level)
    focusSC.text = str(camera_profile.focus_scale)
    exposureC.text = str(camera_profile.exposure_time_camera)
    flash_cc.text = str(camera_profile.flash_color_camera)
    chromaticL.text = str(camera_profile.chromatic_lock)
    irFilter.text = str(camera_profile.ir_filter)

    # Bar light
    barLightProfile = ET.SubElement(data, "barLightProfile")
    exposureB = ET.SubElement(barLightProfile, "exp_time")
    flash_cB = ET.SubElement(barLightProfile, "flash_c")
    angleB = ET.SubElement(barLightProfile, "angle")
    # Set
    exposureB.text = str(bar_profile.exposure_time)
    flash_cB.text = str(bar_profile.flash_color)
    angleB.text = str(bar_profile.angle)

    # Backlight
    backlightProfile = ET.SubElement(data, "backlightProfile")
    exposureBa = ET.SubElement(backlightProfile, "exp_time")
    flash_cBa = ET.SubElement(backlightProfile, "flash_c")
    # Set
    exposureBa.text = str(back_profile.exposure_time)
    flash_cBa.text = str(back_profile.flash_color)

        # Camera
    cameraProfile = ET.SubElement(data, "CameraPosProfile")
    xPos = ET.SubElement(cameraProfile, "xPos")
    zPos = ET.SubElement(cameraProfile, "yPos")
    yPos = ET.SubElement(cameraProfile, "zPos")
    yaw = ET.SubElement(cameraProfile, "yaw")
    pitch = ET.SubElement(cameraProfile, "pitch")
    roll = ET.SubElement(cameraProfile, "roll")
    # Set
    xPos.text = str(camera_pos_profile.xPos)
    yPos.text = str(camera_pos_profile.yPos)
    zPos.text = str(camera_pos_profile.zPos)
    yaw.text = str(camera_pos_profile.yaw)
    pitch.text = str(camera_pos_profile.pitch)
    roll.text = str(camera_pos_profile.roll)

    # Bar light
    barLightProfile = ET.SubElement(data, "barLightPosProfile")
    xPos = ET.SubElement(barLightProfile, "xPos")
    zPos = ET.SubElement(barLightProfile, "yPos")
    yPos = ET.SubElement(barLightProfile, "zPos")
    yaw = ET.SubElement(barLightProfile, "yaw")
    pitch = ET.SubElement(barLightProfile, "pitch")
    roll = ET.SubElement(barLightProfile, "roll")
    # Set
    xPos.text = str(bar_pos_profile.xPos)
    yPos.text = str(bar_pos_profile.yPos)
    zPos.text = str(bar_pos_profile.zPos)
    yaw.text = str(bar_pos_profile.yaw)
    pitch.text = str(bar_pos_profile.pitch)
    roll.text = str(bar_pos_profile.roll)

    #print("Created xml element: ")

    #ET.dump(data)

    return data


def setupProfilerToXml(camera_pos_profile, bar_pos_profile):
    data = ET.Element("Position_Profiles")

    # Camera
    cameraProfile = ET.SubElement(data, "CameraPosProfile")
    xPos = ET.SubElement(cameraProfile, "xPos")
    zPos = ET.SubElement(cameraProfile, "yPos")
    yPos = ET.SubElement(cameraProfile, "zPos")
    yaw = ET.SubElement(cameraProfile, "yaw")
    pitch = ET.SubElement(cameraProfile, "pitch")
    roll = ET.SubElement(cameraProfile, "roll")
    # Set
    xPos.text = str(camera_pos_profile.xPos)
    yPos.text = str(camera_pos_profile.yPos)
    zPos.text = str(camera_pos_profile.zPos)
    yaw.text = str(camera_pos_profile.yaw)
    pitch.text = str(camera_pos_profile.pitch)
    roll.text = str(camera_pos_profile.roll)

    # Bar light
    barLightProfile = ET.SubElement(data, "barLightPosProfile")
    xPos = ET.SubElement(barLightProfile, "xPos")
    zPos = ET.SubElement(barLightProfile, "yPos")
    yPos = ET.SubElement(barLightProfile, "zPos")
    yaw = ET.SubElement(barLightProfile, "yaw")
    pitch = ET.SubElement(barLightProfile, "pitch")
    roll = ET.SubElement(barLightProfile, "roll")
    # Set
    xPos.text = str(bar_pos_profile.xPos)
    yPos.text = str(bar_pos_profile.yPos)
    zPos.text = str(bar_pos_profile.zPos)
    yaw.text = str(bar_pos_profile.yaw)
    pitch.text = str(bar_pos_profile.pitch)
    roll.text = str(bar_pos_profile.roll)

    return data
