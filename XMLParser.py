import xml.etree.ElementTree as ET


def parseXMLtoString(data):
    stringData = ET.tostring(data).decode("utf-8")
    return stringData


def parseXMLtoStringfileAndWrite(data):
    stringData = ET.tostring(data).decode("utf-8")
    file = open("test_converted.txt", "w")
    file.write(stringData)
    print("Done writing to file")


def RFIDProfilerToXML(camera_profile):
    data = ET.Element("CameraSettings")

    # gain_level, focus_scale, exposure_time_camera, exposure_time_barlight, exposure_time_backlight,
    # flash_color_camera, flash_color_barlight, flash_color_backlight, chromatic_lock, ir_filter

    # Define
    gain = ET.SubElement(data, "gain")
    focusS = ET.SubElement(data, "focus")
    exposureC = ET.SubElement(data, "exp_time_c")
    exposureBar = ET.SubElement(data, "exp_time_bar")
    exposureBack = ET.SubElement(data, "exp_time_back")
    flash_cc = ET.SubElement(data, "flash_c_c")
    flash_cbar = ET.SubElement(data, "flash_c_b")
    flash_cback = ET.SubElement(data, "flash_c_b")
    flash_seg = ET.SubElement(data, "flash_seg")
    chromaticL = ET.SubElement(data, "chrom_L")
    irFilter = ET.SubElement(data, "ir")

    # Set
    gain.text = str(camera_profile.gain_level)
    focusS.text = str(camera_profile.focus_scale)
    exposureC.text = str(camera_profile.exposure_time_camera)
    exposureBar.text = str(camera_profile.exposure_time_barlight)
    exposureBack.text = str(camera_profile.exposure_time_backlight)
    flash_cc.text = str(camera_profile.flash_color_camera)
    flash_cbar.text = str(camera_profile.flash_color_barlight)
    flash_cback.text = str(camera_profile.flash_color_backlight)
    flash_seg.text = str(camera_profile.flash_segment)
    chromaticL.text = str(camera_profile.chromatic_lock)
    irFilter.text = str(camera_profile.ir_filter)

    print("Created xml element: ")

    ET.dump(data)

    return data
