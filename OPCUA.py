from opcua import Client
from opcua import ua


def connectToClient(ip):
    client = Client(ip)
    try:
        print("Trying to connect to client...")
        client.connect()
        print("Successfully connected")
        return client
    except Exception as e:
        print(e)
        return None


def getRootNode(client):
    # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
    root = client.get_root_node()
    print("Objects node is: ", root)

    return root


def readValue(client, pvName):
    # get a specific node knowing its node id
    var = client.get_node("ns=6;s=::Program:"+pvName)

    value = var.get_value()  # get value of node as a python builtin
    print("readValue="+str(value))


def setParameters(client, cameraProfile, barLightProfile1, backlightProfile):

    # Set a specific node knowing its node id

    # Camera
    var = client.get_node("ns=6;s=::Program:hmi.input.par.camera.flashColor")
    dv = ua.DataValue(ua.Variant(cameraProfile.flash_color_camera, ua.VariantType.Int16))
    dv.ServerTimestamp = None
    dv.SourceTimestamp = None
    var.set_value(dv)  # set node value using explicit data type

    var = client.get_node("ns=6;s=::Program:hmi.input.par.camera.exposureTime")
    dv = ua.DataValue(ua.Variant(cameraProfile.exposure_time_camera, ua.VariantType.Int16))
    dv.ServerTimestamp = None
    dv.SourceTimestamp = None
    var.set_value(dv)  # set node value using explicit data type

    var = client.get_node("ns=6;s=::Program:hmi.input.par.camera.focusScale")
    dv = ua.DataValue(ua.Variant(cameraProfile.focus_scale, ua.VariantType.Int16))
    dv.ServerTimestamp = None
    dv.SourceTimestamp = None
    var.set_value(dv)  # set node value using explicit data type

    var = client.get_node("ns=6;s=::Program:hmi.input.par.camera.gainLevel")
    dv = ua.DataValue(ua.Variant(cameraProfile.gain_level, ua.VariantType.Int16))
    dv.ServerTimestamp = None
    dv.SourceTimestamp = None
    var.set_value(dv)  # set node value using explicit data type

    var = client.get_node("ns=6;s=::Program:hmi.input.par.camera.irFilter")
    dv = ua.DataValue(ua.Variant(cameraProfile.ir_filter, ua.VariantType.Int16))
    dv.ServerTimestamp = None
    dv.SourceTimestamp = None
    var.set_value(dv)  # set node value using explicit data type

    var = client.get_node("ns=6;s=::Program:hmi.input.par.camera.chromaticLock")
    dv = ua.DataValue(ua.Variant(cameraProfile.chromatic_lock, ua.VariantType.Int16))
    dv.ServerTimestamp = None
    dv.SourceTimestamp = None
    var.set_value(dv)  # set node value using explicit data type

    # Bar light
    var = client.get_node("ns=6;s=::Program:hmi.input.par.barlight[0].flashColor")
    dv = ua.DataValue(ua.Variant(barLightProfile1.flash_color, ua.VariantType.Int16))
    dv.ServerTimestamp = None
    dv.SourceTimestamp = None
    var.set_value(dv)  # set node value using explicit data type

    var = client.get_node("ns=6;s=::Program:hmi.input.par.barlight[0].exposureTime")
    dv = ua.DataValue(ua.Variant(barLightProfile1.exposure_time, ua.VariantType.Int16))
    dv.ServerTimestamp = None
    dv.SourceTimestamp = None
    var.set_value(dv)  # set node value using explicit data type

    var = client.get_node("ns=6;s=::Program:hmi.input.par.barlight[0].angle")
    dv = ua.DataValue(ua.Variant(barLightProfile1.angle, ua.VariantType.Int16))
    dv.ServerTimestamp = None
    dv.SourceTimestamp = None
    var.set_value(dv)  # set node value using explicit data type

    # Backlight
    var = client.get_node("ns=6;s=::Program:hmi.input.par.backlight.exposureTime")
    dv = ua.DataValue(ua.Variant(backlightProfile.exposure_time, ua.VariantType.Int16))
    dv.ServerTimestamp = None
    dv.SourceTimestamp = None
    var.set_value(dv)  # set node value using explicit data type

    var = client.get_node("ns=6;s=::Program:hmi.input.par.backlight.flashColor")
    dv = ua.DataValue(ua.Variant(backlightProfile.flash_color, ua.VariantType.Int16))
    dv.ServerTimestamp = None
    dv.SourceTimestamp = None
    var.set_value(dv)  # set node value using explicit data type


def setTrigger(client):
    # get a specific node knowing its node id
    var = client.get_node("ns=6;s=::Program:hmi.input.trigger")
    dv = ua.DataValue(ua.Variant(True, ua.VariantType.Boolean))
    dv.ServerTimestamp = None
    dv.SourceTimestamp = None
    var.set_value(dv)  # set node value using explicit data type

