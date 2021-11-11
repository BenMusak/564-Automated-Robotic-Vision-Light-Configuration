import roslibpy
import time
import numpy as np

def startROS_Connect():
    client = roslibpy.Ros(host='localhost', port=9090)
    client.run()
    
    #talker_turtle = roslibpy.Topic(client, '/turtle1/cmd_vel', 'geometry_msgs/Twist')
    #talker_robot = roslibpy.Topic(client, '/move_group/cmd_vel', 'geometry_msgs/Pose')
    service = roslibpy.Service(client, '/add_two_ints', 'beginner_tutorials/AddTwoInts')
    sumint = {
        "a" : 5,
        "b" : 5
    }
    
    request = roslibpy.ServiceRequest(sumint)
    Twist = {
        "linear" : {"x": 100.0, "y" : 0.0, "z": 0.0},
        "angular" : {"x": 0.0, "y": 0.0, "z": 100.5}
    }
    Pose = {
        "orientation" :{"x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0},
        "position" : {"x": 0.4, "y":0.1, "z": 0.4}
    }

    print('Calling service...')
    result = service.call(request)
    print('Service response: {}'.format(result))

    client.terminate()

    #while client.is_connected:
        #msg = roslibpy.Message(Twist)
        #talker.publish(roslibpy.Message({'linear' : vec3}))
        #talker_robot.publish(roslibpy.Message(msg))
        #print('Sending message...')
        #time.sleep(1)


    #message = roslibpy.Message()
    #topic = roslibpy.Topic(ros,custom_topic,message)
    #publisher = Topic(ros,/custom_topic, std_msgs/ String)

    #talker_robot.unadvertise()
    #service = roslibpy.Service(client, '/rosout/get_loggers', 'roscpp/GetLoggers')
    #request = roslibpy.ServiceRequest()


    #print('Calling service...')
    #result = service.call(request)
    #print('Service response: {}'.format(result['loggers']))

    client.terminate()
