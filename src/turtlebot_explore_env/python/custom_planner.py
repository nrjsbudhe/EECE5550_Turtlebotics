#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist

cmd_pub = None
MoveStartTime = None
MoveEndTime = None
MoveDuration = rospy.Duration(20)
SpinDuration = rospy.Duration(0)

def get_command(msg):
    global MoveStartTime, MoveEndTime
    if rospy.Time.now() >= MoveEndTime:
        # replace motion command with a spin.
        msg_new  = Twist()
        msg_new.linear.x = 0
        msg_new.angular.z = 0.3142 
        SpinStartTime = rospy.Time.now()
        SpinEndTime = SpinStartTime + SpinDuration
        while rospy.Time.now() <= SpinEndTime:
            # perform a full 360deg spin in place.
            print("Rotating to search for tags.")
            cmd_pub.publish(msg_new)
            rospy.sleep(0.1)
        MoveStartTime = rospy.Time.now()
        MoveEndTime = MoveStartTime + MoveDuration
    else:
        # Use plan generated by explore_lite
        cmd_pub.publish(msg)


def main():

    global cmd_pub, MoveStartTime, MoveEndTime

    rospy.init_node('cmd_interrupt_node')

    MoveStartTime = rospy.Time.now()
    MoveEndTime = MoveStartTime + MoveDuration

    # create publisher for cmd_vel.
    cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

    # subscribe to command sent by motion planner.
    rospy.Subscriber('/cmd_vel_intermediary', Twist, get_command, queue_size=1)

    rospy.spin()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
