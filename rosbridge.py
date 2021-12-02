from __future__ import print_function
import roslibpy
import roslibpy.actionlib

def startROS_Connect():
    client = roslibpy.Ros(host='localhost', port=9090)
    client.run()

    return client

def ROS_SendGoal(client, x,y,z,robot_name, viewpoint_height, obj_hlw):

    action_client = roslibpy.actionlib.ActionClient(client,'/Custom_Python_Script','robot_handler/posAction')



    #talker_turtle = roslibpy.Topic(client, '/turtle1/cmd_vel', 'geometry_msgs/Twist')
    #talker_robot = roslibpy.Topic(client, '/move_group/cmd_vel', 'geometry_msgs/Pose')
    # service = roslibpy.Service(client, '/add_two_ints', 'beginner_tutorials/AddTwoInts')
    goalMsg = {
        "robot_name" : robot_name,
        "x" : x,
        "y" : y,
        "z" : z,
        "viewpoint_height" : viewpoint_height,
        "obj_height" : obj_hlw[0],
        "obj_length" : obj_hlw[1],
        "obj_width" : obj_hlw[2]
    }
    
    
    goal = roslibpy.actionlib.Goal(action_client, roslibpy.Message(goalMsg))

    goal.on('feedback', lambda f: print(f['robot_moved_str']))
    goal.send()
    result = goal.wait()
    action_client.dispose()
    

    #print('Result: {}'.format(result['x']))
    print(result)
    


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
