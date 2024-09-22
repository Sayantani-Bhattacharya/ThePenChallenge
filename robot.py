from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS # type: ignore
from interbotix_common_modules.common_robot.robot import robot_shutdown, robot_startup # type: ignore
import numpy as np
# import time

def read_numbers_from_file(file_path):
    numbers = []    
    with open(file_path, 'r') as file:
        for line in file:
            # Strip any trailing whitespace (like \n) and split by commas
            values = line.strip().split(',')
            
            # Convert the string values to integers
            numbers.append([float(value) for value in values])
    
    return numbers


def robotControlLoop():

    calierated_R = [[-5.71685913e-01,  6.86574032e-01, -4.49211884e-01],[ 1.54100918e-04,  5.47593691e-01,  8.36744361e-01],[ 8.20472543e-01,  4.78285740e-01, -3.13157401e-01]]
    calierated_t = [ 0.07443959, -0.05168204, -0.11349912]
    # calierated_t = [[ 0.07443959, -0.05168204, -0.11349912],[ 0.07876178, -0.04122026, -0.01662375],[ 0.08496207, -0.03600308, -0.10324968]]

    while(True):
        robot.arm.go_to_home_pose()
        # sleep or timer
        robot.gripper.release()

        # getPenLocaCam : from penDetectionCord.txt
        file_path = 'penDetectionCord.txt'
        penCoordData = read_numbers_from_file(file_path)
        # Print the result
        for row in penCoordData:
            print(row)

        # Target pose
        penCordInR = np.dot(np.array(penCoordData), np.array(calierated_R)) + np.array(calierated_t)
        
        # Current Pose :
        currentState = robot.arm.get_ee_pose()
        currentPose = currentState[0:3,3]

        # currentAngle = np.arctan() - NN
        # currentAngle = robot.arm.capture_joint_positions("waist")

        # Turn at the waist until the end-effector is facing the pen
        a = penCordInR[0,1]-currentPose[1]
        bm = penCordInR[0,0]-currentPose[0]
        waisetMov = np.arctan(penCordInR[0,1]-currentPose[1] / penCordInR[0,0]-currentPose[0])

        # robot.arm.set_single_joint_position("waist", currentAngle + waisetMov) 


        #     elif mode == "b": # relative
#         robot.arm.set_ee_cartesian_trajectory(x=0.2, z=0)



        # Opem Loop control:
        # 1. waist movement
        # 2. height 
        # 3. forwards till pen inside the gripper
        # 4. close the gripper

        robot.arm.set_single_joint_position("waist", waisetMov) 


# home - all joint angles are 0
# bot.arm.set_ee_pose_components(x=0.3, z=0.2)  ->> for absolute positions - relative to base link frame
# bot.arm.set_single_joint_position("waist", np.pi/2.0)



# ################ Cite ##############

# # ex tuotrial : https://github.com/Interbotix/interbotix_ros_manipulators/blob/main/interbotix_ros_xsarms/examples/python_demos/bartender.py

# ################ Cite ##############




# z_coordinate: for test1.
# [0.26623040437698364, 0.2139762043952942, 0.6180000305175781]



# The robot object is what you use to control the robot
robot = InterbotixManipulatorXS("px100", "arm", "gripper")

robot_startup()
mode = 'h'

# Let the user select the position
while mode != 'q':

    robotControlLoop()
    # mode=input("[h]home, [s]sleep, [o]open, [c]close, [u]up, [l]turn left, [r]turn right, [f]orward, [q]uit ")
    # currentState = robot.arm.get_ee_pose()
    # currentPose = currentState[0:3,3]  # camera in real world coords.
    # print(currentPose)

    # if mode == "h":
    #     robot.arm.go_to_home_pose()
    # elif mode == "s":
    #     robot.arm.go_to_sleep_pose()
    # elif mode == "o":
    #     robot.gripper.release()
    # elif mode == "c":
    #     robot.gripper.grasp()
    # elif mode == "l":
        
    #     robot.arm.set_single_joint_position("waist", np.pi/6.0) 
    # elif mode == "r":
    #     robot.arm.set_single_joint_position("waist", -np.pi/6.0)  #turn
    # elif mode == "u":
    #     robot.arm.set_single_joint_position("elbow", np.pi/6.0)   #height
    # elif mode == "f":
    #     # robot.arm.set_ee_cartesian_trajectory(x=0.04, z=0.1)  # not sure what exactly it does.
    #     # robot.arm.set_single_joint_position("wrist_angle", np.pi/6.0)
    #     robot.arm.set_ee_cartesian_trajectory(x = currentPose[0] - 0.04, z=0.0)

robot_shutdown()