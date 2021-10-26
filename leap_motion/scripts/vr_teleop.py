#!/usr/bin/python
import rospy 
from leap_motion.msg import leap 
from leap_motion.msg import leapros 
from geometry_msgs.msg import Twist 


teleop_topic = '/cmd_vel_mux/input/teleop' 

vel_pub=rospy.Publisher('/cmd_vel', Twist, queue_size=1)
 
 
low_speed = -0.15
stop_speed = 0 
high_speed = 0.15
 
low_turn = -0.15
stop_turn = 0 
high_turn = 0.15
 
pitch_low_range = -15
pitch_high_range = 15
 
roll_low_range = -60
roll_high_range = 60


def listener():
    global pub 
    rospy.init_node('leap_sub', anonymous=True) 
    rospy.Subscriber("leapmotion/data", leapros, callback_ros) 
    pub = rospy.Publisher(teleop_topic, Twist, queue_size=1) 
 
    rospy.spin() 
 
 
def callback_ros(data):
    global pub 
 
    msg = leapros() 
    msg = data 
     
    yaw = msg.ypr.x 
    pitch = msg.ypr.y 
    roll = msg.ypr.z 

    #print([yaw, pitch, roll])

    #emergency stop
    x = msg.palmpos.x
    y = msg.palmpos.y
    z = msg.palmpos.z

    #print([x,y,z])

 
 
    twist = Twist()

    twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
    twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0

    if(pitch<pitch_low_range):
        speed = -0.01*pitch
        if speed > high_speed:
            speed = high_speed
        twist.linear.x = speed
        twist.angular.z = 0
        print("Going forward")
    elif(pitch>pitch_high_range):
        speed = -0.01*pitch
        if speed < low_speed:
            speed = low_speed
        twist.linear.x = speed
        twist.angular.z = 0
        print("Going reverse")


    if(roll>roll_high_range and pitch<(pitch_low_range/2)):
        twist.linear.x = 0
        turn_speed = -0.0025*roll
        if turn_speed < low_turn:
            turn_speed = low_turn
        twist.angular.z = turn_speed
        print("Turning right")
    elif(roll<roll_low_range and pitch<(pitch_low_range/2)):
        twist.linear.x = 0
        turn_speed = -0.0025*roll
        if turn_speed > high_turn:
            turn_speed = high_turn
        twist.angular.z = turn_speed
        print("Turning left")


    if(y<40):
        print("Emergency stop\n")
        twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
        vel_pub.publish(twist)


    #pub.publish(twist)
    vel_pub.publish(twist)


if __name__ == '__main__': 
        listener() 

   
