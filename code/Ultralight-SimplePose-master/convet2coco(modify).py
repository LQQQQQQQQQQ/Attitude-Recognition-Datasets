# *_* : coding: utf-8 *_*

"""
将数据转换成想要的 coco 数据的 json 格式
需要：文件名 标注框 关键点 类别

datasets process for object detection project.
for convert customer dataset format to coco data format,
"""

import traceback
import argparse
import datetime
import json
import cv2
import os

__CLASS__ = ['__background__', 'lpr']   # class dictionary, background must be in first index.

def argparser():
    parser = argparse.ArgumentParser("define argument parser for pycococreator!")

    # 输出的 json 文件名（train 或者 val 或者 test）
    parser.add_argument("-p", "--phase_folder", default=["train"], help="datasets path of [train, val, test]")

    # 根目录
    # parser.add_argument("-r", "--root_path", default="test1/ccpd_300x300", help="path of root directory")
    parser.add_argument("-r", "--root_path", default="anno_process/", help="path of root directory")

    # 判断是否有关键点
    parser.add_argument("-po", "--have_points", default=True, help="if have points we will deal with it!")

    # 图片文件夹
    parser.add_argument("-im", "--images", default="images", help="folder of images")

    # 标注文件路径
    parser.add_argument("-anno", "--annotations", default="anno.txt", help="file of annotations")

    return parser.parse_args()

def MainProcessing(args):
    '''main process source code.'''
    annotations = {}                                                # annotations dictionary, which will dump to json format file.
    phase_folder = args.phase_folder                                # ["test"]
    root_path = os.path.join(args.root_path, phase_folder[0])          # anno_process/train 或者 anno_process/val
    images_folder = os.path.join(root_path, args.images)            # 图片文件夹 "anno_process/train/images"

    '''
    if not os.path.exists(images_folder):
        os.mkdir(images_folder)                                     # 如果没有图片文件夹则创建   
    '''

    anno_path = os.path.join(root_path, args.annotations)           # 标注文件路径 "anno_process/train/anno.txt"

    # coco annotations info.
    annotations["info"] = {
        "description": "customer dataset format convert to COCO format",
        "url": "http://cocodataset.org",
        "version": "1.0",
        "year": 2020,
        "contributor": "lqqq",
        "date_created": "2020"
    }
    # coco annotations licenses.
    annotations["licenses"] = [{
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        "id": 1,
        "name": "Apache License 2.0"
    }]
    # coco annotations categories.
    annotations["categories"] = []
    for cls, clsname in enumerate(__CLASS__):
        if clsname == '__background__':
            continue
        annotations["categories"].append(
            {
                "supercategory": "person",
                "id": cls,
                "name": 'person',
                "keypoints": ["nose", "left_eye", "right_eye", "left_ear", "right_ear",
                                        "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
                                        "left_wrist", "right_wrist", "left_hip", "right_hip", "left_knee",
                                        "right_knee", "left_ankle", "right_ankle"],  # 关键点

                "skeleton": [[16, 14], [14, 12], [17, 15], [15, 13], [12, 13], [6, 12],
                               [7, 13], [6, 7], [6, 8], [7, 9], [8, 10], [9, 11], [2, 3],
                               [1, 2], [1, 3], [2, 4], [3, 5], [4, 6], [5, 7]]  # 骨架
            }
        )

    '''
        for catdict in annotations["categories"]:
            if "lpr" == catdict["name"] and args.have_points:
                catdict["keypoints"] = ["nose", "left_eye", "right_eye", "left_ear", "right_ear",
                                        "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
                                        "left_wrist", "right_wrist", "left_hip", "right_hip", "left_knee",
                                        "right_knee", "left_ankle", "right_ankle"]                          # 关键点
                catdict["skeleton"] = [[16, 14], [14, 12],[17, 15],[15, 13],[12, 13],[6, 12],
                                       [7, 13],[6, 7],[6, 8],[7, 9],[8, 10],[9, 11],[2, 3],
                                       [1, 2],[1, 3],[2, 4],[3, 5],[4, 6],[5, 7]]                           # 骨架
    '''

    for phase in phase_folder:
        annotations["images"] = []
        annotations["annotations"] = []

        if os.path.isfile(anno_path) and os.path.exists(images_folder):
            print("convert datasets {} to coco format!".format(phase))
            fd = open(anno_path, "r")
            # fd_w = open(filename_mapping_path, "w")
            step = 0
            for id, line in enumerate(fd.readlines()):
                if line:
                    label_info = line.split()

                    image_name = label_info[0]                              # 图片名
                    bbox = [int(x) for x in label_info[1].split(",")]       # 标注框 bbox
                    # cls = int(label_info[-1])                             # 类别编号，这里为 0

                    filename = os.path.join(images_folder, image_name)      # 图片文件
                    img = cv2.imread(filename)
                    height, width, _ = img.shape                            # 读取图片大小
                    x1 = bbox[0]
                    y1 = bbox[1]                                            # bbox 中心点
                    # bw = bbox[2] - bbox[0]                                # 右侧内边距
                    # bh = bbox[3] - bbox[1]                                # 上册内边距
                    bw = bbox[2]                                            # 宽 w
                    bh = bbox[3]                                            # 高 h

                    # coco annotations images.
                    # file_name = 'COCO_' + phase + '_' + str(id).zfill(12) + '.jpg'  # annotation["images"] 下 “file_name” 的值
                    file_name = str(image_name)                                       # annotation["images"] 下 “file_name” 的值

                    # newfilename = os.path.join(images_folder, file_name)
                    # os.rename(filename, newfilename)                                # 将 filename 改为 newfilename
                    # filename_mapping = file_name + " " + image_name + "\n"          # 将图片新的名字和原有名字写到映射文件（train_filename_mapping.txt）中
                    # fd_w.write(filename_mapping)

                    annotations["images"].append(
                        {
                            "license": 1,
                            "file_name": file_name,
                            "coco_url": "http://images.cocodataset.org/" + phase_folder[0] + "2017/" + file_name,  #  "http://images.cocodataset.org/train2017/hjw004.jpg"
                            "height": height,
                            "width": width,
                            "date_captured": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            "flickr_url": "",
                            "id": id
                        }
                    )
                    # coco annotations annotations.
                    annotations["annotations"].append(
                        {
                            "id": id,
                            "image_id": id,
                            "category_id": 1,           # 类别编号，对于人体关键点检测任务，他只有一个类别，所以恒为 1
                            "segmentation": [[]],
                            "area": 1,                  # 这个 area 是图像分割的东西，置为 1 就行
                            "bbox": [x1, y1, bw, bh],
                            "iscrowd": 0,               # 目标是否被遮盖，默认为0
                        }
                    )
                    if args.have_points:
                        v = 2                           # v 字段表示关键点属性，0表示未标注，1表示已标注但不可见，2表示已标注且可见
                        catdict = annotations["annotations"][id]
                        if "lpr" == __CLASS__[catdict["category_id"]]:
                            # points = [int(p) for p in label_info[2].split(",")]
                            points = label_info[2].split(",")[:-1]                  # [:-1]是为了去掉尾部空格
                            # print(points)
                            # print(len(points))
                            pp =[]
                            for i in range(0, len(points), 2):
                                pp.append(int(points[i]))
                                pp.append(int(points[i + 1]))
                                pp.append(2)
                            # catdict["keypoints"] = [points[0], points[1], v, points[2], points[3], v, points[4]]
                            catdict["keypoints"] = pp

                            catdict["num_keypoints"] = int(len(points) / 2)      # 一般是 17

                    step += 1
                    if step % 100 == 0:
                        print("processing {} ...".format(step))
            fd.close()
            # fd_w.close()
        else:
            print("WARNNING: file path incomplete, please check!")

        json_path = os.path.join(root_path, phase+".json")
        with open(json_path, "w") as f:
            json.dump(annotations, f)


if __name__ == "__main__":
    print("beginning to convert customer format to coco format!")
    args = argparser()
    try:
        MainProcessing(args)
    except Exception as e:
        traceback.print_exc()
    print("successful to convert customer format to coco format")
