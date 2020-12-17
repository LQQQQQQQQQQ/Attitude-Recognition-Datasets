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
    # 根目录
    # parser.add_argument("-r", "--root_path", default="/home/andy/workspace/ccpd_300x300", help="path of root directory")
    parser.add_argument("-r", "--root_path", default="test1/ccpd_300x300", help="path of root directory")
    # 三个文件夹：train, val, test
    parser.add_argument("-p", "--phase_folder", default=["ccpd_base_coco"], help="datasets path of [train, val, test]")

    # 判断是否有关键点
    parser.add_argument("-po", "--have_points", default=True, help="if have points we will deal with it!")

    return parser.parse_args()

def MainProcessing(args):
    '''main process source code.'''
    annotations = {}                    # annotations dictionary, which will dump to json format file.
    root_path = args.root_path          # "test1/ccpd_300x300"
    phase_folder = args.phase_folder    # "ccpd_base_coco"

    # coco annotations info.
    annotations["info"] = {
        "description": "customer dataset format convert to COCO format",
        "url": "http://cocodataset.org",
        "version": "1.0",
        "year": 2020,
        "contributor": "andy.wei",
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
                "name": clsname
            }
        )
        for catdict in annotations["categories"]:
            if "lpr" == catdict["name"] and args.have_points:
                catdict["keypoints"] = ["top_left", "top_right", "bottom_right", "bottom_left"]     # 关键点
                catdict["skeleton"] = [[]]                                                          # 骨架

    for phase in phase_folder:
        annotations["images"] = []
        annotations["annotations"] = []
        label_path = os.path.join(root_path, phase+".txt")
        filename_mapping_path = os.path.join(root_path, phase + "_filename_mapping" + ".txt")
        images_folder = os.path.join(root_path, phase)          # 图片文件夹

        fd = open(label_path, "w")
        for f in os.listdir(images_folder):
            # ff = os.path.join(images_folder, f)
            infos = f.split("-")                                # 这段代码有问题
            pbs = []
            if len(infos) != 7:
                assert "Error!"
            for info in infos:
                if info:
                    pbs.append(info)
            bboxtemp = pbs[2].split("_")
            bbox = bboxtemp[0].split("&") + bboxtemp[1].split("&")
            pointstemp = pbs[3].split("_")
            points = pointstemp[0].split("&") + pointstemp[1].split("&") + pointstemp[2].split("&") + pointstemp[3].split("&")
            bbox = [int(b) for b in bbox]
            points = [int(p) for p in points]
            line = f + " " + str(bbox[0]) + "," + str(bbox[1]) + "," + str(bbox[2]) + "," + str(bbox[3]) \
                   + " " + str(points[4]) + "," + str(points[5]) + "," + str(points[6]) + "," + str(points[7]) \
                   + "," + str(points[0]) + "," + str(points[1]) + "," + str(points[2]) + "," + str(points[3]) \
                   + " " + "0"
            fd.write(line+"\n")
        fd.close()

        if os.path.isfile(label_path) and os.path.exists(images_folder):
            print("convert datasets {} to coco format!".format(phase))
            fd = open(label_path, "r")
            fd_w = open(filename_mapping_path, "w")
            step = 0
            for id, line in enumerate(fd.readlines()):
                if line:
                    label_info = line.split()

                    image_name = label_info[0]                              # 图片名
                    bbox = [int(x) for x in label_info[1].split(",")]       # 标注框 bbox
                    cls = int(label_info[-1])                               # 类别编号，这里为 0

                    filename = os.path.join(images_folder, image_name)      # 图片文件
                    img = cv2.imread(filename)
                    height, width, _ = img.shape                            # 读取图片大小
                    x1 = bbox[0]
                    y1 = bbox[1]                                            # bbox 中心点
                    bw = bbox[2] - bbox[0]                                  # 右侧内边距
                    bh = bbox[3] - bbox[1]                                  # 上册内边距

                    # coco annotations images.
                    file_name = 'COCO_' + phase + '_' + str(id).zfill(12) + '.jpg'  # annotation["images"] 下 “file_name” 的值
                    newfilename = os.path.join(images_folder, file_name)
                    os.rename(filename, newfilename)                                # 将 filename 改为 newfilename

                    filename_mapping = file_name + " " + image_name + "\n"          # 将图片新的名字和原有名字写到映射文件（train_filename_mapping.txt）中
                    fd_w.write(filename_mapping)

                    annotations["images"].append(
                        {
                            "license": 1,
                            "file_name": file_name,
                            "coco_url": "",
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
                            "category_id": cls+1,       # 类别编号，对于人体关键点检测任务，他只有一个类别，所以恒为 1
                            "segmentation": [[]],
                            "area": bw * bh,            # 这个计算有点问题？？？？？？？？？？？？？？
                            "bbox": [x1, y1, bw, bh],
                            "iscrowd": 0,               # 目标是否被遮盖，默认为0
                        }
                    )
                    if args.have_points:
                        v = 2                           # v 字段表示关键点属性，0表示未标注，1表示已标注但不可见，2表示已标注且可见
                        catdict = annotations["annotations"][id]
                        if "lpr" == __CLASS__[catdict["category_id"]]:
                            points = [int(p) for p in label_info[2].split(",")]
                            catdict["keypoints"] = [points[0], points[1], v, points[2], points[3], v, points[4], points[5], v, points[6], points[7], v]
                            catdict["num_keypoints"] = 4

                    step += 1
                    if step % 100 == 0:
                        print("processing {} ...".format(step))
            fd.close()
            fd_w.close()
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