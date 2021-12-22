class CameraProfile:
    def __init__(self, gain_level=0, focus_scale=0, exposure_time_camera=0, flash_color_camera=0, chromatic_lock=0,
                 ir_filter=0):
        self.gain_level = gain_level
        self.focus_scale = focus_scale
        self.exposure_time_camera = exposure_time_camera
        self.flash_color_camera = flash_color_camera
        self.chromatic_lock = chromatic_lock
        self.ir_filter = ir_filter


class BarLightProfile:
    def __init__(self, exposure_time=0, flash_color=0, angle=0):
        self.exposure_time = exposure_time
        self.flash_color = flash_color
        self.angle = angle


class BackLightProfile:
    def __init__(self, exposure_time=0, flash_color=0):
        self.exposure_time = exposure_time
        self.flash_color = flash_color

class CameraSetupProfile:
    def __init__(self, xPos=0, yPos=0, zPos=0, yaw=0, pitch=0, roll=0):
        self.xPos = xPos
        self.yPos = yPos
        self.zPos = zPos
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll

class barLightSetupProfile:
    def __init__(self, xPos=0, yPos=0, zPos=0, yaw=0, pitch=0, roll=0):
        self.xPos = xPos
        self.yPos = yPos
        self.zPos = zPos
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll