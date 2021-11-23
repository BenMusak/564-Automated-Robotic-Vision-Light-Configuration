import controller as ct

def setParameters():
    # Profiles
    cameraProfile = ct.CameraProfile()
    barLightProfile1 = ct.BarLightProfile()
    backlightProfile = ct.BackLightProfile()

    # Camera
    cameraProfile.flash_color_camera = 1
    cameraProfile.exposure_time_camera = 1747
    cameraProfile.ir_filter = False
    cameraProfile.gain_level = 1
    cameraProfile.focus_scale = 230
    cameraProfile.chromatic_lock = False

    # Bar Light
    barLightProfile1.flash_color = 1
    barLightProfile1.exposure_time = 1747
    barLightProfile1.angle = 50

    # Backlight
    backlightProfile.exposure_time = 1747
    backlightProfile.flash_color = 1

    return cameraProfile, barLightProfile1, backlightProfile
