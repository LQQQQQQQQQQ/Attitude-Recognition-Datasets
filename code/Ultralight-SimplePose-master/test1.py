import os
'''
path1 = "test1/ccpd_300x300/anno_test"
for f in os.listdir(path1):
    print(f)
    path2 = os.path.join(path1, str(f))
    fo = open(path2)
    line = fo.readline()

    arr = line.split(" ")
    print(arr)
    print("-----------------")

    if len(arr) > 1:
        bbox_temp = arr[1].split("_")
        bbox = bbox_temp[0].split("&") + bbox_temp[1].split("&")
        points_temp = arr[2].split("_")
        points = points_temp[0].split("&") + points_temp[1].split("&") + points_temp[2].split("&") + points_temp[3].split("&")
        print(bbox)
        print(points)
    print("-----------------")
'''
path = "out.txt"

fo = open(path)
lines = fo.readlines()

for line in lines:
    arr = line.split(" ")
    if len(arr) > 1:
        bbox_temp = arr[1].split(",")
        # bbox = bbox_temp[0].split("&") + bbox_temp[1].split("&")
        points_temp = arr[2].split(",")[:-1]
        points = []
        # points = points_temp[0].split("&") + points_temp[1].split("&") + points_temp[2].split("&") + points_temp[3].split("&")
        for i in range(0, len(points_temp) - 2):
            points.append(points_temp[i])
            points.append(points_temp[i + 1])
            points.append(2)

        print(arr[0])
        print(bbox_temp)
        print(points_temp)
        print(len(points_temp))
        print(points)
    print("-----------------")