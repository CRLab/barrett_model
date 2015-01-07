#!/usr/bin/env python

import rospy
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import Transform, TransformStamped

pub = None
robot_pose = TransformStamped()
robot_pose.child_frame_id = "bhand/bhand_palm_link"
robot_pose.header.frame_id = "world"
robot_pose.transform.translation.z = 1
robot_pose.transform.rotation.w = 1

def tf_callback(transforms):
    global pub
    global robot_pose
    for transform in transforms.transforms:
        if transform.child_frame_id != "bhand/bhand_palm_link":
            #import IPython; IPython.embed()
            #rospy.loginfo("0 - %s" % transform.child_frame_id)
            pub.publish([transform])
        else:
            pub.publish([robot_pose])
            robot_pose.header.stamp = transform.header.stamp

            #import IPython; IPython.embed()

def pose_callback(transform):
    global pub
    global robot_pose
    #tf = TransformStamped()
    #robot_pose.child_frame_id = "bhand/bhand_palm_link"
    robot_pose.transform = transform
    #robot_pose.header.frame_id = "world"

    #pub.publish([robot_pose])


def listener():
    rospy.init_node('position_tf_server_node')

    global pub
    pub = rospy.Publisher('gdl_tf', TFMessage, queue_size=50)

    rospy.Subscriber("tf", TFMessage, tf_callback)
    rospy.Subscriber("gdl_robot_pose", Transform, pose_callback)
    rospy.spin()


if __name__ == '__main__':
    listener()


#from std_msgs.msg import String
#
#from sensor_msgs.msg import JointState
#
#pub = rospy.Publisher('topic_name', String, queue_size=10)
#rospy.init_node('node_name')
#r = rospy.Rate(10) # 10hz
#while not rospy.is_shutdown():
#   pub.publish("hello world")
#   r.sleep()

