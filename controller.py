class CameraProfile:
    def __init__(self, gain_level, focus_scale, exposure_time_camera, exposure_time_barlight, exposure_time_backlight,
                 flash_color_camera, flash_color_barlight, flash_color_backlight, flash_segment, chromatic_lock, ir_filter):
        self.gain_level = gain_level
        self.focus_scale = focus_scale
        self.exposure_time_camera = exposure_time_camera
        self.exposure_time_barlight = exposure_time_barlight
        self.exposure_time_backlight = exposure_time_backlight
        self.flash_color_camera = flash_color_camera
        self.flash_color_barlight = flash_color_barlight
        self.flash_color_backlight = flash_color_backlight
        self.flash_segment = flash_segment
        self.chromatic_lock = chromatic_lock
        self.ir_filter = ir_filter
