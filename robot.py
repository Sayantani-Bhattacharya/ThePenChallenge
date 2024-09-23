from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS # type: ignore
from interbotix_common_modules.common_robot.robot import robot_shutdown, robot_startup # type: ignore
import numpy as np
import time

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

    # calierated_R = [[-5.71685913e-01,  6.86574032e-01, -4.49211884e-01],[ 1.54100918e-04,  5.47593691e-01,  8.36744361e-01],[ 8.20472543e-01,  4.78285740e-01, -3.13157401e-01]]
    # calierated_t = [ 0.07443959, -0.05168204, -0.11349912]

    calierated_R =  [[ 0.17385956,  0.88103482,  0.43994375],[-0.58631386, -0.2663276,   0.76505272],[ 0.79120725, -0.39095685,  0.47025932]]
    calierated_t = [-0.03882705, -0.02950353, -0.0496295 ]
    

    while(True):
        time.sleep(3)
        robot.arm.go_to_sleep_pose()
        # sleep or timer
        robot.gripper.release()

        # getPenLocaCam : from penDetectionCord.txt
        file_path = 'penDetectionCord.txt'
        penCoordData = read_numbers_from_file(file_path)
        # Target pose
        penCordInR = np.dot(np.array(penCoordData), np.array(calierated_R)) + np.array(calierated_t)        
        # Current Pose :
        currentState = robot.arm.get_ee_pose()
        currentPose = currentState[0:3,3]

        # currentAngle = np.arctan() - NN
        # currentAngle = robot.arm.capture_joint_positions("waist")

        # Turn at the waist until the end-effector is facing the pen
        waisetMov = np.arctan(penCordInR[0,1]-currentPose[1] / penCordInR[0,0]-currentPose[0])
        angleOffset = 0.3
        robot.arm.set_single_joint_position("waist", waisetMov + angleOffset)
        time.sleep(2)
        offsetX = 0.06
        offsetZ = 0
        robot.arm.set_ee_cartesian_trajectory(x = currentPose[0] + offsetX , y = 0,  z= currentPose[2] + offsetZ)
        time.sleep(5)
        robot.gripper.grasp()
        break



# home - all joint angles are 0
# bot.arm.set_ee_pose_components(x=0.3, z=0.2)  ->> for absolute positions - relative to base link frame
# bot.arm.set_single_joint_position("waist", np.pi/2.0)



# ################ Cite ##############

# # ex tuotrial : https://github.com/Interbotix/interbotix_ros_manipulators/blob/main/interbotix_ros_xsarms/examples/python_demos/bartender.py

# ################ Cite ##############




# The robot object is what you use to control the robot
robot = InterbotixManipulatorXS("px100", "arm", "gripper")

robot_startup()
mode = 'h'

# Let the user select the position
# while mode != 'q':

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
    
    
    # # elif mode == "l":        
    # #     robot.arm.set_single_joint_position("waist", np.pi/6.0) 
    # # elif mode == "r":
    # #     robot.arm.set_single_joint_position("waist", -np.pi/6.0)  #turn



    # # elif mode == "u":
    # #     robot.arm.set_single_joint_position("elbow", np.pi/6.0)   #height
    # elif mode == "d":
    #     robot.arm.set_single_joint_position("elbow", np.pi/4.0)   #height   

    # elif mode == "u":
    #     robot.arm.set_single_joint_position("shoulder", -np.pi/6.0)


    # # elif mode == "f":
    # #     # robot.arm.set_ee_cartesian_trajectory(x=0.04, z=0.1)  # not sure what exactly it does.
    # #     # robot.arm.set_single_joint_position("wrist_angle", np.pi/6.0)
    #     # robot.arm.set_ee_cartesian_trajectory(x = currentPose[0] - 0.04, z=0.0)

    
    # elif mode == "a":
    #     # robot.arm.set_ee_cartesian_trajectory(x=0.04, z=0.1)  # not sure what exactly it does.
    #     robot.arm.set_single_joint_position("waist", np.pi/2.0)
    # elif mode == "b":
    #     # robot.arm.set_ee_cartesian_trajectory(x=0.04, z=0.1)  # not sure what exactly it does.
    #     robot.arm.set_single_joint_position("waist", -np.pi/2.0)
    # elif mode == "k":
    #     # robot.arm.set_ee_cartesian_trajectory(x=0.04, z=0.1)  # not sure what exactly it does.
    #     robot.arm.set_single_joint_position("waist", np.pi/8.0)
    # elif mode == "l":
    #     # robot.arm.set_ee_cartesian_trajectory(x=0.04, z=0.1)  # not sure what exactly it does.
    #     robot.arm.set_single_joint_position("waist", - np.pi/8.0)



robot_shutdown()