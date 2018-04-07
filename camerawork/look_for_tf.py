#!/usr/bin/env python  
import rospy
import sys
import math
import tf2_ros
import tf
import geometry_msgs.msg
import turtlesim.srv

if __name__ == '__main__':
    if len(sys.argv) == 3:
        base = sys.argv[1]
        child = sys.argv[2]
        print 'parent: ', base
        print 'child:', child
        raw_input('press any key to start')
    else:
        base = raw_input("look up tf from parent frame:")
        if len(base) == 0: a = 'world'
        child = raw_input("to child frame:")
        if len(child) == 0: b = 'ar_marker_1'

    rospy.init_node('tf2_listener')

    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)
    n = 0

    rate = rospy.Rate(30.0)
    while not rospy.is_shutdown():
        try:
            trans = tfBuffer.lookup_transform( base,child, rospy.Time())
            n = n + 1
            rpy = tf.transformations.euler_from_quaternion(
            [trans.transform.rotation.x, trans.transform.rotation.y,
             trans.transform.rotation.z, trans.transform.rotation.w])
            print 'n:', n
            print 'trans.x: ', (trans.transform.translation.x * 100)
            print 'trans.y: ', (trans.transform.translation.y * 100)
            print 'trans.z: ', (trans.transform.translation.z * 100)
            print 'roll: ', (rpy[0] * 180 / 3.14)
            print 'pitch: ', (rpy[1] * 180 / 3.14)
            print 'yaw: ', (rpy[2] * 180 / 3.14)
            if n % 10 == 0:
# second approach
                tfBuffer.clear()
                
#             tfBuffer = tf2_ros.Buffer()
#             listener = tf2_ros.TransformListener(tfBuffer)
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            #print e
            rate.sleep()
            continue



        rate.sleep()
