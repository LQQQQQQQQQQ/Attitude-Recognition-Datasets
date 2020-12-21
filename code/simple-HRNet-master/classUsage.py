import cv2
import matplotlib.pyplot as plt
from SimpleHRNet import SimpleHRNet
from misc.visualization import draw_points_and_skeleton, joints_dict, draw_points

model = SimpleHRNet(48, 17, "./weights/pose_hrnet_w48_384x288.pth")
# 这里的文件路径和文件名根据自己要识别的图片来
# image = cv2.imread("C:/Users/QQQ/Desktop/1/278.jpg", cv2.IMREAD_COLOR)
image = cv2.imread("F:/My_Project/python/MathCollege_Project/Mobile_PoseEstimation/Ultralight-SimplePose-master/data/000000123213.jpg", cv2.IMREAD_COLOR)
joints = model.predict(image)
'''
frame = draw_points_and_skeleton(image, joints, joints_dict()['coco']['skeleton'], person_index=15,
                                 points_color_palette='gist_rainbow', skeleton_color_palette='jet',
                                 points_palette_samples=10)  # 添加关键点和骨干
'''

frame = draw_points(image, joints)

cv2.imshow(frame)
print(joints)