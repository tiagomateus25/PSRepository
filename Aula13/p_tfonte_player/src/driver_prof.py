#!/usr/bin/env python3
import copy
import math

import rospy
import tf2_ros
from geometry_msgs.msg import Twist, PoseStamped
import tf2_geometry_msgs  # **Do not use geometry_msgs. Use this instead for PoseStamped


class Driver:

    def __init__(self):

        self.goal = PoseStamped()
        self.goal_active = False

        self.angle = 0
        self.speed = 0

        self.name = rospy.get_name()
        self.name = self.name.strip('/') # remove initial /
        print('My player name is ' + self.name)

        self.publisher_command = rospy.Publisher( '/' + self.name + '/cmd_vel', Twist, queue_size=1)

        self.tf_buffer = tf2_ros.Buffer()
        self.listener = tf2_ros.TransformListener(self.tf_buffer)

        self.timer = rospy.Timer(rospy.Duration(0.1), self.sendCommandCallback)

        self.goal_subscriber = rospy.Subscriber('/move_base_simple/goal', PoseStamped, self.goalReceivedCallback)

    def goalReceivedCallback(self, msg):
        # TODO verify is goal is on odom frame
        print('Received new goal on frame id' + msg.header.frame_id)
        target_frame = self.name + '/odom'
        try:

            self.goal = self.tf_buffer.transform(msg, target_frame, rospy.Duration(1))
            self.goal_active = True
            rospy.logwarn('Setting new goal')
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            goal_active = False
            rospy.logerr('Could not transform goal from ' + msg.header.frame_id + ' to ' + target_frame + '. Will ignore this goal.')

        # print('Received new goal')
        # self.goal = copy.copy(msg)  # store goal
        # self.goal = copy.copy(msg)  # store goal
        # self.goal_active = True

    def driveStraight(self, minumum_speed=0.1, maximum_speed=1.5):
        goal_copy = copy.deepcopy(self.goal)  # make sure we don't change the stamp field of the goal
        goal_copy.header.stamp = rospy.Time.now()

        # goal_tf = tf2_geometry_msgs.PoseStamped()
        # goal_tf.header.stamp = rospy.Time.now()
        # goal_tf.header.frame_id = self.goal.header.frame_id

        print('Transforming pose')
        goal_in_base_link = self.tf_buffer.transform(goal_copy, self.name + '/base_footprint', rospy.Duration(1))
        print('Pose trasnformed')

        x = goal_in_base_link.pose.position.x
        y = goal_in_base_link.pose.position.y

        self.angle = math.atan2(y,x)

        distance_to_goal = math.sqrt(x**2 + y**2)
        self.speed = max(minumum_speed, 0.5 * distance_to_goal)   # limit minimum speed
        self.speed = min(maximum_speed, self.speed)   # limit maximum speed

    def sendCommandCallback(self, event):
        print('Sending twist command')

        if not self.goal_active:  # no goal, no movement
            self.angle = 0
            self.speed = 0
        else:
            self.driveStraight()

        twist = Twist()
        twist.linear.x = self.speed
        twist.angular.z = self.angle
        self.publisher_command.publish(twist)


def main():
    # ---------------------------------------------------
    # INITIALIZATION
    # ---------------------------------------------------

    rospy.init_node('p_moliveira_driver', anonymous=False)

    driver = Driver()
    rospy.spin()

    # ---------------------------------------------------
    # Execution
    # ---------------------------------------------------
    # while not rospy.is_shutdown():
    #
    #     # create a dog message to sent

    # ---------------------------------------------------
    # Termination
    # ---------------------------------------------------


if __name__ == '__main__':
    main()