import numpy as np
from scipy.spatial.transform import Rotation 
# from sklearn.utils.extmath import orthogonal_procrustes


robot_cord = [[0.08982101,0,0.07613427]]
robot_cord.append([-0.14472135,0,0.32086199])
robot_cord.append([0.08808153,0,0.07038202])

camera_cord = [[-0.010204939171671867, 0.101206935942173, 0.2980000078678131]]
camera_cord.append([0.003794589312747121, 0.10286978632211685, 0.2760000228881836])
camera_cord.append([-0.00152928801253438, -0.12628169357776642, 0.5460000038146973])

# print(robot_cord[0])
sum = [0,0,0]
centroidR = {}
# centroid of all there
for i in range(len(robot_cord)):
    sum[0] += robot_cord[i][0]
    sum[1] += robot_cord[i][1]
    sum[2] += robot_cord[i][2]
centroidR[0] = sum[0] / len(robot_cord)
centroidR[1] = sum[1] / len(robot_cord)
centroidR[2] = sum[2] / len(robot_cord)

sum = [0,0,0]
centroidC = {}
for i in range(len(camera_cord)):
    sum[0] += camera_cord[i][0]
    sum[1] += camera_cord[i][1]
    sum[2] += camera_cord[i][2]

centroidC[0] = sum[0] / len(robot_cord)
centroidC[1] = sum[1] / len(robot_cord)
centroidC[2] = sum[2] / len(robot_cord)

# print(centroidC)
# print(centroidR)
 
# Towards centre:
for i in range(len(robot_cord)):
    robot_cord[i][0] = robot_cord[i][0] - centroidR[0]
    robot_cord[i][1] = robot_cord[i][1] - centroidR[1]
    robot_cord[i][2] = robot_cord[i][2] - centroidR[2]

for i in range(len(camera_cord)):
    camera_cord[i][0] = camera_cord[i][0] - centroidC[0]
    camera_cord[i][1] = camera_cord[i][1] - centroidC[1]
    camera_cord[i][2] = camera_cord[i][2] - centroidC[2]

print(camera_cord)
print(robot_cord)

# Find the rotation matrix.
P_centered = robot_cord
Q_centered = camera_cord

R ,_ = Rotation.align_vectors(np.array(camera_cord), np.array(robot_cord))
R = R.as_matrix()

print("Optimal Rotation Matrix:\n")  
print(R)

# assumung Q as robot and P as camera

t = robot_cord[0] - R * camera_cord[0]
print("T value : git ")
print(t)


# print("Checkkkkkkk")
# LHS = robot_cord[2]
# RHS = R * camera_cord[2] + t
# f = LHS - RHS
# print(f)