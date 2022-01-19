import mysql.connector
import controller as con

database = mysql.connector.connect(
    host="85.191.222.184", user="br_user", password="br_user", database="brVision")
cursor = database.cursor()

test_id = "Ulla"
run = 0
cameraprofile = con.CameraProfile()
barlightprofile = con.BarLightProfile()
backlightprofile = con.BackLightProfile()
lightarm_setup = con.barLightSetupProfile()
cameraarm_setup = con.CameraSetupProfile()

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
                   run) + ".jpg", run, cameraprofile.gain_level, cameraprofile.focus_scale,
                cameraprofile.exposure_time_camera, cameraprofile.flash_color_camera, cameraprofile.chromatic_lock,
                cameraprofile.ir_filter, cameraarm_setup.xPos, cameraarm_setup.yPos, cameraarm_setup.zPos,
                cameraarm_setup.yaw, cameraarm_setup.pitch, cameraarm_setup.roll, barlightprofile.exposure_time,
                barlightprofile.flash_color, barlightprofile.angle, lightarm_setup.xPos, lightarm_setup.yPos,
                lightarm_setup.zPos, lightarm_setup.yaw, lightarm_setup.pitch, lightarm_setup.roll,
                backlightprofile.exposure_time, backlightprofile.flash_color))

database.commit()

cursor.close()
