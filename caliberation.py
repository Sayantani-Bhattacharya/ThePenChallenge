import numpy as np
from scipy.spatial.transform import Rotation 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plotCaliberation():
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the Camera axes..
    # X-axis
    ax.plot([0, 1], [0, 0], [0, 0], color='blue', linewidth=2, label='CamX-axis')
    # Y-axis
    ax.plot([0, 0], [0, 1], [0, 0], color='green', linewidth=2, label='CamY-axis')
    # Z-axis
    ax.plot([0, 0], [0, 0], [0, 1], color='orange', linewidth=2, label='CamZ-axis')


    # Plot the robot axis.
    # calierated_R = [[-5.71685913e-01,  6.86574032e-01, -4.49211884e-01],[ 1.54100918e-04,  5.47593691e-01,  8.36744361e-01],[ 8.20472543e-01,  4.78285740e-01, -3.13157401e-01]]
    # calierated_t = [ 0.07443959, -0.05168204, -0.11349912]
    calierated_R =  [[ 0.17385956,  0.88103482,  0.43994375],[-0.58631386, -0.2663276,   0.76505272],[ 0.79120725, -0.39095685,  0.47025932]]
    calierated_t = [-0.03882705, -0.02950353, -0.0496295 ]
 
    ax.plot([0 + calierated_t[0], calierated_R[0][0] + calierated_t[0]], [0 + calierated_t[1],  calierated_R[1][0]  + calierated_t[1] ], [0 + calierated_t[2], calierated_R[2][0]  + calierated_t[2]], color='blue', linewidth=5, label='RobX-axis')
    ax.plot([0 + calierated_t[0], calierated_R[0][1] + calierated_t[0]], [0 + calierated_t[1],  calierated_R[1][1]  + calierated_t[1] ], [0 + calierated_t[2], calierated_R[2][1]  + calierated_t[2]], color='green', linewidth=5, label='RobY-axis')
    ax.plot([0 + calierated_t[0], calierated_R[0][2] + calierated_t[0]], [0 + calierated_t[1],  calierated_R[1][2]  + calierated_t[1] ], [0 + calierated_t[2], calierated_R[2][2]  + calierated_t[2]], color='orange', linewidth=5, label='RobY-axis')

    ax.legend()
    plt.show()


def automateCaliberation():
    print("complete later")


######################################################################################################


# robot_cord = [[0.08982101,0,0.07613427]]
# robot_cord.append([-0.14472135,0,0.32086199])
# robot_cord.append([0.08808153,0,0.07038202])

# camera_cord = [[-0.010204939171671867, 0.101206935942173, 0.2980000078678131]]
# camera_cord.append([0.003794589312747121, 0.10286978632211685, 0.2760000228881836])
# camera_cord.append([-0.00152928801253438, -0.12628169357776642, 0.5460000038146973])

#################################################



robot_cord = [[ 0.08982756,-0.00110241,  0.07908429]]
robot_cord.append([0.13036715, 0,        0.07120116])
robot_cord.append([0.21538728, 0,         0.07130984])
robot_cord.append([0.25209558, 0,         0.17397506])
robot_cord.append([0.21970161, 0.12357063, 0.1736486 ])
robot_cord.append([0.20689422, 0.11636714, 0.27123562])
robot_cord.append([0.25045467, 0.00268945, 0.16101702])
robot_cord.append([0.23237201, 0.09375541, 0.16063273])
robot_cord.append([0.25035727, 0.00192025, 0.16140116])
robot_cord.append([0.10981393, 0.04430676, 0.36623814])


camera_cord = [[-0.0526207834482193, -0.04366038739681244, 0.17500001192092896]]
camera_cord.append([-0.07467924803495407, 0.0025479416362941265, 0.24700000882148743])
camera_cord.append([-0.05868932232260704, -0.022276513278484344, 0.1850000023841858])
camera_cord.append([0.033731065690517426, 0.030294518917798996, 0.25699999928474426])
camera_cord.append([0.04735059291124344, -0.023922612890601158, 0.2460000067949295])
camera_cord.append([0.02528553269803524, -0.023953130468726158, 0.22700001299381256])
camera_cord.append([0.016243826597929, 0.044239774346351624, 0.23200000822544098])
camera_cord.append([-0.0028242773842066526, -0.04420863091945648, 0.2550000250339508])
camera_cord.append([-0.06785069406032562, -0.03264877572655678, 0.2150000035762787])
camera_cord.append([-0.01416125986725092, 0.08454883098602295, 0.27000001072883606])

#############################################################

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
 
# Towards centre:
for i in range(len(robot_cord)):
    robot_cord[i][0] = robot_cord[i][0] - centroidR[0]
    robot_cord[i][1] = robot_cord[i][1] - centroidR[1]
    robot_cord[i][2] = robot_cord[i][2] - centroidR[2]

for i in range(len(camera_cord)):
    camera_cord[i][0] = camera_cord[i][0] - centroidC[0]
    camera_cord[i][1] = camera_cord[i][1] - centroidC[1]
    camera_cord[i][2] = camera_cord[i][2] - centroidC[2]

# Find the rotation matrix.
P_centered = robot_cord
Q_centered = camera_cord

# R : Optimal Rotation Matrix
R ,_ = Rotation.align_vectors(np.array(camera_cord), np.array(robot_cord))
R = R.as_matrix()

# Assumung Q as robot and P as camera
t = robot_cord[0] - np.dot(np.array(R ), np.array(camera_cord[0]))


# Verification Way 1
# print("Checkkkkkkk")
# LHS = robot_cord[2]
# RHS = R * camera_cord[2] + t
# f = LHS - RHS
# print(f)

plotCaliberation()


