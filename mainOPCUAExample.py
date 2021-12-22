import OPCUA
import setupParameters as sp
import XMLParser as XMLP


def main():

    # Connect
    client = OPCUA.connectToClient("opc.tcp://192.168.87.210:4840")

    # Make the profilers with some parameters
    cameraProfile, barLightProfile1, backlightProfile = sp.setParameters()

    # Make xml profiles and save them to a file
    xmlData = XMLP.profilerToXML(cameraProfile, barLightProfile1, backlightProfile)
    XMLP.parseXMLtoFileAndWrite(xmlData)

    # Send the data to PLC over OPC-UA
    OPCUA.getRootNode(client)
    OPCUA.setParameters(client, cameraProfile, barLightProfile1, backlightProfile)
    OPCUA.setTrigger(client)


if __name__ == "__main__":
    main()

