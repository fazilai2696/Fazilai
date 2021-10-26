Instructions to run the code
Clone this in your catkin_workspace/src folder

Pre-requisites
ROS installed
Python
Gazebo with turtlebot

Step 1: Launch empty world in Gazebo with turtlebot3
roslaunch turtlebot3_gazebo turtlebot3_empty_world.launch

Step 2: Play rosbag (unzip the bag before use)
rosbag play Project.bag

Step 3: Run vr_teleop.py script
rosrun leap_motion vr_teleop.py
