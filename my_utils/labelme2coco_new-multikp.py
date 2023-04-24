import os
import argparse
import json

import numpy as np
import glob
import PIL.Image
from PIL import ImageDraw
import logging
from labelme.utils.buildKeypointNames import buildKeypointNames, drawKeypoints
from pathlib import Path

import cv2
import numpy as np


class labelme2coco:
    def __init__(self, AllJingluoNames, labelme_json=[], save_json_path="./coco.json", thing_classes=None):
        """
        :param labelme_json: the list of all labelme json file paths
        :param save_json_path: the path to save new json
        """
        self.labelme_json = labelme_json
        self.dir_name = os.path.split(labelme_json[0])[0]
        self.save_json_path = save_json_path
        self.images = []
        self.categories = []
        self.annotations = []
        self.label = []
        self.annID = 1
        self.height = 0
        self.width = 0
        self.thing_classes = thing_classes
        # self.keypointNames = JingluoNames

        self.keypointNames = AllJingluoNames
        self.label = ["leg","hand"] #要检测几个类，在这里添加
        self.scale = 3

    def getaccunames(self, jingluonames, jlnames):
        names = []
        for jlname in jlnames:
            names += jingluonames[jlname]
        return names

    def data_transfer(self):
        for num, json_file in enumerate(self.labelme_json):

            #先将categories 创建好
            for label in self.label:
                self.categories.append(self.category(label))
            with open(json_file, "r") as fp:
                data = json.load(fp)
                self.images.append(self.image(data, num))
                ann = {}
                ann["iscrowd"] = 0

                ann["image_id"] = num

                # ann["category_id"] = 'person'  # self.getcatid(label)
                ann["id"] = self.annID
                keypoints = {}
                # iscorrectted = self.correctNose(data)
                hasKp = False
                shapes = data["shapes"]
                bbox = self.build_bbox(shapes)
                self.build_bboxAnn(ann, bbox)
                for thing_name,jlnames in self.keypointNames.items():
                    # hasKp = False
                    for jlname in jlnames:
                        for shapeindex, shape in enumerate(shapes):
                            label = shape["label"]
                            if label != jlname:
                                continue

                            points = shape["points"]
                            shape_type = shape['shape_type']
                            self.build_ann(ann, keypoints, points,
                                        label, num, shape_type)
                            shapes.pop(shapeindex)
                            if label == jlname:
                                hasKp = True
                                break
                    # assert hasKp
                    # self.annotations.append(self.annotation(points, label, num, shape_type))
                if hasKp:
                    self.make_keypoints(ann, keypoints)
                    self.annotations.append(ann)
                    self.annID += 1
                    img, imgpath = self.readimg(json_file)
                    assert img.shape[1] <2000, "image shape must 720,1280"
                    # img_copy = self.drawAnn(img, ann, self.keypointNames)
                    # imgsmall = cv2.resize(
                    #     img_copy, (img.shape[1] // 2, img.shape[0] // 2))
                    # cv2.imshow("img", imgsmall)
                    # cv2.waitKey(30)
                    # self.saveDrawimg(imgpath, img_copy)
                    print(num, json_file + "  done!")
            # if iscorrectted:
            #     with open(json_file, "w") as fp:
            #         json.dump(data, fp)

        # Sort all text labels so they are in the same order across data splits.
        # self.label.sort()
        
        for annotation in self.annotations:
            annotation["category_id"] = self.getcatid(
                annotation["category_id"])
    def saveDrawimg(self, filePath, drawimg):

        filename = os.path.basename(filePath)
        path = os.path.join('drawimg',filename)
        filedir = os.path.dirname(path)
        if not os.path.exists(filedir):
            os.makedirs(filedir)        
        cv2.imwrite(path, drawimg)

    def getImagePath(self, jsonpath: str):
        imgpath = jsonpath.replace('json', 'jpg')
        return imgpath

    def readimg(self, json_file):
        imgpath = self.getImagePath(json_file)
        img = cv2.imread(imgpath)
        return img, imgpath

    def drawAnn(self, img, ann, AllKpNames):
        kpts = ann["keypoints"]
        bbox = ann["bbox"]
        left_top = (int(bbox[0]), int(bbox[1]))
        right_bottom = (int(bbox[2] + bbox[0]), int(bbox[3] + bbox[1]))
        cv2.rectangle(
            img, left_top, right_bottom, (255, 255, 255))
        npkpts = np.array(kpts)
        npkpts = npkpts.reshape(-1, 3)
        # for kid in range(npkpts.shape[0]):
        #     kpt = npkpts[kid]
        #     x_coord, y_coord, kpt_score = int(kpt[0]), int(
        #         kpt[1]), kpt[2]

        #     r, g, b = 255, 0, 0
        #     cv2.circle(img, (int(x_coord), int(y_coord)),
        #                 3, (int(r), int(g), int(b)), -1)
        #     cv2.putText(img, AllKpNames[kid], (int(x_coord), int(y_coord)), 2, 1, (255, 255, 255) )
        drawKeypoints(img, npkpts, AllKpNames)
        return img

    def build_bboxAnn(self, ann, bbox):
        ann['bbox'] = bbox
        x = ann['bbox'][0]
        y = ann['bbox'][1]
        w = ann['bbox'][2]
        h = ann['bbox'][3]
        ann["area"] = w * h

    def build_bbox(self, shapes):
        for shapeindex, shape in enumerate(shapes):
            label = shape["label"]
            # if label != 'person':
            if label not in self.label:
                continue
            points = shape["points"]
            if points[0][1] > points[1][1]:
                height = points[0][1] - points[1][1]
                points[0][1] = points[0][1] - height
                points[1][1] = points[1][1] + height
            assert len(points) == 2
            assert points[1][0] > points[0][0]
            assert points[1][1] > points[0][1]
            assert len(points) == 2
            bbox = [points[0][0], points[0][1], points[1]
                    [0] - points[0][0], points[1][1] - points[0][1]]
        return bbox

    def image(self, data, num):
        image = {}
        height, width = data['imageHeight'], data['imageWidth']
        image["height"] = height
        image["width"] = width
        image["id"] = num
        # image["file_name"] = os.path.join(self.dir_name, data["imagePath"])
        file_name = data["imagePath"]
        basename = os.path.basename(file_name)
        basenameSplit = basename.split("\\")
        # sptext =  os.path.splitext(file_name)
        # stem = Path(file_name).resolve().stem
        name = basenameSplit[-1]
        image["file_name"] = name
        self.height = height
        self.width = width

        return image

    def category(self, label):
        category = {}
        category["supercategory"] = label
        category["id"] = len(self.categories) + 1
        category["name"] = label
        return category

    def make_keypoints(self, ann, keypoints):
        cnt = len(keypoints)
        ann["num_keypoints"] = cnt
        assert cnt > 0
        annKp = []
        for keyName in self.keypointNames:
            # assert keyName in keypoints
            if keyName in keypoints:
                kp = keypoints[keyName] + [2]
                assert len(kp) == 3

            else:
                kp = [0, 0, 0]
            annKp += kp
        assert len(annKp) == len(self.keypointNames) * 3
        ann["keypoints"] = annKp

    def build_keypoint(self, keypoints, points, label, num, shape_type):
        assert not label in keypoints
        assert len(points) == 1
        keypoints[label] = points[0]

        pass

    def build_ann(self, ann: dict, keypoints: dict, points, label, num, shape_type):
        if shape_type == 'rectangle':
            # assert len(ann) == 0
            assert False
            self.ann_rectangle(ann, points, label, num, shape_type)
        elif shape_type == 'point':

            self.build_keypoint(keypoints, points, label, num, shape_type)
        else:
            logging.warning("shape_type:" + shape_type)
        # print(ann)

    def ann_rectangle(self, annotation, points, label, num, shape_type):
        assert (shape_type == 'rectangle')
        # annotation = {}
        # contour = np.array(points)
        # x = contour[:, 0]
        # y = contour[:, 1]
        area = self.height * self.width
        annotation["bbox"] = list(map(float, self.getbbox(points, shape_type)))
        x = annotation['bbox'][0]
        y = annotation['bbox'][1]
        w = annotation['bbox'][2]
        h = annotation['bbox'][3]
        annotation["area"] = area
        # if shape_type == 'rectangle':
        #     annotation['segmentation'] = [[x, y, x+w, y, x+w, y+h, x, y+h]] # at least 6 points
        # elif shape_type == 'polygon':
        #     points = [np.asarray(points).flatten().tolist()]
        #     annotation['segmentation'] = points

        return annotation

    def getcatid(self, label):
        for category in self.categories:
            if label == category["name"]:
                return category["id"]
        print("label: {} not in categories: {}.".format(label, self.categories))
        exit()
        return 1

    def getbbox(self, points, shape_type):
        polygons = points
        mask = self.polygons_to_mask([self.height, self.width], polygons)
        return self.mask2box(mask)

    def mask2box(self, mask):

        index = np.argwhere(mask == 1)
        rows = index[:, 0]
        clos = index[:, 1]

        left_top_r = np.min(rows)  # y
        left_top_c = np.min(clos)  # x

        right_bottom_r = np.max(rows)
        right_bottom_c = np.max(clos)

        return [
            left_top_c,
            left_top_r,
            right_bottom_c - left_top_c,
            right_bottom_r - left_top_r,
        ]

    def polygons_to_mask(self, img_shape, polygons):
        mask = np.zeros(img_shape, dtype=np.uint8)
        mask = PIL.Image.fromarray(mask)
        xy = list(map(tuple, polygons))
        PIL.ImageDraw.Draw(mask).polygon(xy=xy, outline=1, fill=1)
        mask = np.array(mask, dtype=bool)
        return mask

    def data2coco(self):
        data_coco = {}
        data_coco["images"] = self.images
        data_coco["categories"] = self.categories
        data_coco["annotations"] = self.annotations
        return data_coco

    def __call__(self):
        print("save coco json")
        self.data_transfer()
        print("data2coco")
        self.data_coco = self.data2coco()

        print(self.save_json_path)
        os.makedirs(
            os.path.dirname(os.path.abspath(self.save_json_path)), exist_ok=True
        )
        print("dump jsonfile")
        json.dump(self.data_coco, open(self.save_json_path, "w"), indent=4)
        if self.thing_classes is not None:
            with open(self.thing_classes, 'w') as f:
                f.writelines(map(lambda x: x + '\n', self.label))




if __name__ == "__main__":

    jlname = {"leg":['L-pi-1', 'L-pi-2', 'L-pi-3', 'L-pi-4', 'L-pi-5', 'L-pi-6', 'L-pi-7', 'R-pi-1', 'R-pi-2', 'R-pi-3', 'R-pi-4', 'R-pi-5', 'R-pi-6', 'R-pi-7', 
                'L-wei-24', 'L-wei-25', 'L-wei-26', 'L-wei-27', 'L-wei-28', 'L-wei-29', 'L-wei-30', 'R-wei-24', 'R-wei-25', 'R-wei-26', 'R-wei-27', 'R-wei-28', 'R-wei-29', 'R-wei-30', 
                ],
                "hand":['R-xinbao-5', 'R-xinbao-6', 'R-xinbao-7', 'R-xinbao-8', 'R-xinbao-9', 'L-xinbao-5', 'L-xinbao-6', 'L-xinbao-7', 'L-xinbao-8', 'L-xinbao-9', 
                'L-fei-6', 'L-fei-7', 'L-fei-8', 'R-fei-6', 'R-fei-7', 'R-fei-8'
                ]}

    baseDir = "/911G/data/temp/20221229新加手托脚托新数据/精确标注494套middle_up_nei_changerec_yolo/images/"
    EightModelList = [
        [jlname, 'train'],
        [jlname, 'test'],
        ]


    # 生成8个模型的数据集json文件
    for jlname, dir1 in EightModelList:
        # print(dir1)
        labelme_directory = baseDir + dir1
        labelme_json = glob.glob(os.path.join(labelme_directory, "*.json"))
        output = labelme_directory + ".json"
        labelme2coco(jlname, labelme_json, output)()
