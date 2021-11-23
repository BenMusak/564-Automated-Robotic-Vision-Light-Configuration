import xml.etree.ElementTree as ET


def parseXMLtoString(data):
    stringData = ET.tostring(data).decode("utf-8")
    return stringData


def parseXMLtoStringfileAndWrite(data):
    stringData = ET.tostring(data).decode("utf-8")
    file = open("test_converted.txt", "w")
    file.write(stringData)
    print("Done writing to file")


def parseXMLtoFileAndWrite(data):
    elementData = ET.ElementTree(data)
    elementData.write("test_converted.xml")
    print("Done writing to file")


def cameraProfilerToXML(camera_profile, bar_profile, back_profile):
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
    exposureC.text = str(back_profile.exposure_time)
    flash_cBa.text = str(back_profile.flash_color)

    print("Created xml element: ")

    ET.dump(data)

    return data
