#!/usr/bin/env python
# this is the node1

import rospy, tf, tf2_ros, geometry_msgs.msg, std_msgs.msg, std_srvs.srv, time, subprocess
import simple_robotino_messages.srv


robotino_state = 'coarse'

def target_callback(data):
    global  robotino_state
    robotino_state = data.data

def interaction_complete_response(data):
    global interaction_complete
    interaction_complete = True

class waypoint(object):
    def __init__(self, ix, iy, iomg, is_accurate):
        self.x = ix
        self.y = iy
        self.theta = iomg
        self.isaccurate = is_accurate

    def distance_squared(self, x, y):
        return (self.x - x)** 2 + (self.y - y) ** 2

rospy.init_node("robotino_target_select")
rospy.Subscriber('robotino_state', std_msgs.msg.String , target_callback)
targetpub = rospy.Publisher('target_location', geometry_msgs.msg.Pose2D)
rospy.ServiceProxy('interaction_complete', std_srvs.srv.Empty, interaction_complete_response)

tfBuffer = tf2_ros.Buffer()
listener = tf2_ros.TransformListener(tfBuffer)
robotino_frame_name = rospy.get_param('~robotino_name','robotino')
rate = rospy.Rate(5)
currentpose = []


waypoints = [waypoint(1,1,90,False), waypoint(3,3,180,True)]
current_wp_index = 0
while not rospy.is_shutdown():
    rate.sleep()
    try:
        trans = tfBuffer.lookup_transform(robotino_frame_name, 'world', rospy.Time())
        n = n + 1
        runawaycount = 35
        currentpose[0] = trans.transform.translation.x
        currentpose[1] = trans.transform.translation.y
        currentpose[2] = (tf.transformations.euler_from_quaternion(
            [trans.transform.rotation.x, trans.transform.rotation.y,
             trans.transform.rotation.z, trans.transform.rotation.w])[2]) * 180 / 3.14

        if n % 10 == 0:
            tfBuffer = tf2_ros.Buffer()
            listener = tf2_ros.TransformListener(tfBuffer)

    except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
        print 'ignored: ', e
        runawaycount = runawaycount - 1

    if runawaycount <= 0: rospy.logerr('node 1 cannot find robotino coordinate!')

    if robotino_state == 'coarse':


            if waypoint[current_wp_index].distance_squared(currentpose[0], currentpose[1]) < 0.01 \
                    and -10 < waypoint[current_wp_index].theta - currentpose[2] < 10     :

                if waypoint[current_wp_index].isaccurate == False :

                    current_wp_index = current_wp_index + 1

                else:
                    # process camera selection, etc
                    # actually, camera selection will be done on finding specific markers
                    # here nothing is done
                    pass
            # also look for accurate markers


    if robotino_state == 'accurate':

        if waypoint[current_wp_index].distance_squared(currentpose[0], currentpose[1]) < 0.025 \
                and 7 < waypoint[current_wp_index].theta - currentpose[2] < 7:
            robotino_state == 'wait'



    if robotino_state == 'wait':
        if interaction_complete: # % wait for external interactions completion: give new waypoint
            interaction_complete = False
            robotino_state = 'coarse'
            # process camera selections, ...

            current_wp_index = current_wp_index + 1
            if current_wp_index > len(waypoints): current_wp_index = 0



    # % publish waypoint here
    if robotino_state != 'wait':
        targetmsg = geometry_msgs.msg.Pose2D()
        targetmsg.x = waypoints[current_wp_index].x
        targetmsg.y = waypoints[current_wp_index].y
        targetmsg.theta = waypoints[current_wp_index].theta
        targetpub.publish()
    # ######

###########################################################
'''
    if robotino_state == 'accu':
        try:
            trans = tfBuffer.lookup_transform(robotino_frame_name, 'world', rospy.Time())
            n = n + 1
            runawaycount = 70
            currentpose[0] = trans.transform.translation.x
            currentpose[1] = trans.transform.translation.y
            #currentpose[2] = (tf.transformations.euler_from_quaternion(
            #    [trans.transform.rotation.x, trans.transform.rotation.y,
            #     trans.transform.rotation.z, trans.transform.rotation.w])[2]) * 180 / 3.14


            if n % 10 == 0:
                tfBuffer = tf2_ros.Buffer()
                listener = tf2_ros.TransformListener(tfBuffer)

        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            print 'ignored: ', e
            runawaycount = runawaycount - 1
'''