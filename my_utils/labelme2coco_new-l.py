import os
import argparse
import json

import numpy as np
import glob
import PIL.Image
from PIL import ImageDraw
import logging
# from labelme.utils.buildKeypointNames import buildKeypointNames, drawKeypoints
from pathlib import Path

import cv2
import numpy as np


class labelme2coco(object):
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
        self.thingNames = ["person"]
        self.label = self.thingNames
        self.save_json()
        self.scale = 3

    def getaccunames(self, jingluonames, jlnames):
        names = []
        for jlname in jlnames:
            names += jingluonames[jlname]
        return names

    def data_transfer(self):
        for num, json_file in enumerate(self.labelme_json):
            with open(json_file, "r") as fp:
                data = json.load(fp)
                self.images.append(self.image(data, num))
                ann = {}
                ann["iscrowd"] = 0

                ann["image_id"] = num

                ann["category_id"] = 'person'  # self.getcatid(label)
                ann["id"] = self.annID
                keypoints = {}
                # iscorrectted = self.correctNose(data)
                hasKp = False
                shapes = data["shapes"]
                bbox = self.build_bbox(shapes)
                self.build_bboxAnn(ann, bbox)
                for jlname in self.keypointNames:
                    # hasKp = False
                    for shapeindex, shape in enumerate(shapes):
                        label = shape["label"]
                        if label != jlname:
                            continue

                        # if label not in self.label:
                        #     self.label.append(label)
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
        self.label.sort()
        for label in self.label:
            self.categories.append(self.category(label))
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
        # drawKeypoints(img, npkpts, AllKpNames)
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
            if label != 'person':
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
        # for category in self.categories:
        #     if label == category["name"]:
        #         return category["id"]
        # print("label: {} not in categories: {}.".format(label, self.categories))
        # exit()
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

    def save_json(self):
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
    # 肝 左侧
    jl_gan_left = ['L-gan-1', 'L-gan-2', 'R-gan-3', 'R-gan-4', 'R-gan-5',
                   'R-gan-6', 'R-gan-7', 'R-gan-8', 'R-gan-9', 'L-gan-16']
    # 肝 右侧
    jl_gan_right = ['R-gan-1', 'R-gan-2', 'L-gan-3', 'L-gan-4', 'L-gan-5',
                    'L-gan-6', 'L-gan-7', 'L-gan-8', 'L-gan-9', 'R-gan-16']

    # 心包
    jl_xingbao = ['R-xinbao-1', 'R-xinbao-2', 'R-xinbao-3', 'R-xinbao-4', 'R-xinbao-5', 'R-xinbao-6',
                  'R-xinbao-7', 'R-xinbao-8', 'R-xinbao-9',
                  'L-xinbao-1', 'L-xinbao-2', 'L-xinbao-3', 'L-xinbao-4', 'L-xinbao-5', 'L-xinbao-6',
                  'L-xinbao-7', 'L-xinbao-8', 'L-xinbao-9']

    # 肺经
    jl_fei = ['L-fei-1', 'L-fei-2', 'L-fei-3', 'L-fei-4', 'L-fei-5', 'L-fei-6', 'L-fei-7', 'L-fei-8',
              'R-fei-1', 'R-fei-2', 'R-fei-3', 'R-fei-4', 'R-fei-5', 'R-fei-6', 'R-fei-7', 'R-fei-8']

    # 大肠
    jl_dachang = ['R-dachang-1', 'R-dachang-2', 'R-dachang-3', 'R-dachang-4', 'R-dachang-5', 'R-dachang-6', 'R-dachang-20', 'R-dachang-7', 'R-dachang-8',
                  'L-dachang-1', 'L-dachang-2', 'L-dachang-3', 'L-dachang-4', 'L-dachang-5', 'L-dachang-6', 'L-dachang-20', 'L-dachang-7', 'L-dachang-8']

    # 脾经 左侧
    jl_pi_left = ['R-pi-1', 'R-pi-2', 'R-pi-3', 'R-pi-4',
                  'R-pi-5', 'R-pi-6', 'R-pi-7', 'R-pi-8', 'L-pi-13', 'L-pi-14']

    # 脾经 右侧
    jl_pi_right = ['L-pi-1', 'L-pi-2', 'L-pi-3', 'L-pi-4',
                   'L-pi-5', 'L-pi-6', 'L-pi-7', 'L-pi-8', 'R-pi-13', 'R-pi-14']

    # 脾经 中间
    jl_pi_middle = ['L-pi-9', 'L-pi-10', 'L-pi-11', 'L-pi-12', 'L-pi-15', 'L-pi-16', 'L-pi-17', 'L-pi-18', 'L-pi-19',
                    'R-pi-9', 'R-pi-10', 'R-pi-11', 'R-pi-12', 'R-pi-15', 'R-pi-16', 'R-pi-17', 'R-pi-18', 'R-pi-19',
                    'R-gan-10', 'R-gan-11', 'R-gan-12', 'R-gan-13', 'R-gan-14', 'R-gan-15', 'R-gan-17', 'R-gan-18',
                    'L-gan-10', 'L-gan-11', 'L-gan-12', 'L-gan-13', 'L-gan-14', 'L-gan-15', 'L-gan-17', 'L-gan-18']

    # 胃经
    jl_wei_middle = ['L-wei-15', 'L-wei-16', 'L-wei-17', 'L-wei-18', 'L-wei-19', 'L-wei-20', 'L-wei-21', 'L-wei-22',
                     'L-wei-23',
                     'L-wei-24', 'L-wei-25', 'L-wei-26', 'L-wei-27', 'L-wei-28', 'L-wei-29', 'L-wei-30', 'R-wei-15',
                     'R-wei-16', 'R-wei-17', 'R-wei-18', 'R-wei-19', 'R-wei-20', 'R-wei-21', 'R-wei-22', 'R-wei-23',
                     'R-wei-24', 'R-wei-25', 'R-wei-26', 'R-wei-27', 'R-wei-28', 'R-wei-29', 'R-wei-30']
    # jl_wei_right=['R-wei-15', 'R-wei-16','R-wei-17','R-wei-18','R-wei-19','R-wei-20', 'R-wei-21','R-wei-22','R-wei-23',
    #     'R-wei-24','R-wei-25','R-wei-26','R-wei-27','R-wei-28', 'R-wei-29','R-wei-30']

    # 心经
    jl_xin_left = ['L-xin-1', 'L-xin-2',
                   'L-xin-3', 'L-xin-4', 'L-xin-5', 'L-xin-6']
    jl_xin_right = ['R-xin-1', 'R-xin-2',
                    'R-xin-3', 'R-xin-4', 'R-xin-5', 'R-xin-6']

    # 三焦经
    jl_sanjiao = ['L-sanjiao-1', 'L-sanjiao-2', 'L-sanjiao-3', 'L-sanjiao-4', 'L-sanjiao-5',
                  'L-sanjiao-6', 'L-sanjiao-7','L-sanjiao-8','L-sanjiao-9', 'R-sanjiao-1', 'R-sanjiao-2', 'R-sanjiao-3', 'R-sanjiao-4',
                  'R-sanjiao-5','R-sanjiao-6', 'R-sanjiao-7', 'R-sanjiao-8', 'R-sanjiao-9']

    # 小肠
    jl_xiaochang = ['L-xiaochang-1', 'L-xiaochang-2', 'L-xiaochang-3', 'L-xiaochang-4', 'L-xiaochang-20', 'L-xiaochang-5',
                    'L-xiaochang-6', 'L-xiaochang-7', 'L-xiaochang-8', 'L-xiaochang-9', 'L-xiaochang-10',
                    'L-xiaochang-11', 'L-xiaochang-12',
                    'R-xiaochang-1', 'R-xiaochang-2', 'R-xiaochang-3', 'R-xiaochang-4', 'R-xiaochang-20', 'R-xiaochang-5',
                    'R-xiaochang-6', 'R-xiaochang-7', 'R-xiaochang-8', 'R-xiaochang-9', 'R-xiaochang-10',
                    'R-xiaochang-11', 'R-xiaochang-12']

    # 膀胱
    jl_pangguang = ['L-pangguang-9', 'L-pangguang-10', 'L-pangguang-11', 'L-pangguang-12', 'L-pangguang-13',
                    'L-pangguang-14', 'L-pangguang-15', 'L-pangguang-16', 'L-pangguang-17', 'L-pangguang-18',
                    'L-pangguang-19', 'L-pangguang-20', 'L-pangguang-21', 'L-pangguang-22', 'L-pangguang-23',
                    'L-pangguang-24', 'R-pangguang-9', 'R-pangguang-10',
                    'R-pangguang-11', 'R-pangguang-12', 'R-pangguang-13',
                    'R-pangguang-14', 'R-pangguang-15', 'R-pangguang-16', 'R-pangguang-17', 'R-pangguang-18',
                    'R-pangguang-19', 'R-pangguang-20', 'R-pangguang-21', 'R-pangguang-22', 'R-pangguang-23',
                    'R-pangguang-24']

    # 肾经-上身
    jl_shenjing_shangshen = ['R-shen-14', 'R-shen-15', 'R-shen-16', 'R-shen-17', 'R-shen-18', 'R-shen-19',
                             'L-shen-14', 'L-shen-15', 'L-shen-16', 'L-shen-17', 'L-shen-18', 'L-shen-19']

    # 肾经-下身
    jl_shenjing_xiashen = ['R-shen-1', 'R-shen-2', 'R-shen-3', 'R-shen-4', 'R-shen-5',
                           'R-shen-6', 'R-shen-7', 'R-shen-8', 'R-shen-9', 'R-shen-10', 'R-shen-11', 'R-shen-12',
                           'R-shen-13',
                           'L-shen-1', 'L-shen-2', 'L-shen-3', 'L-shen-4', 'L-shen-5',
                           'L-shen-6', 'L-shen-7', 'L-shen-8', 'L-shen-9', 'L-shen-10', 'L-shen-11', 'L-shen-12',
                           'L-shen-13']

    # 胆-right(之前标注中有部分人标到41，就以41为标准)
    jl_dan_right = ['R-dan-21', 'R-dan-22', 'R-dan-23', 'R-dan-24', 'R-dan-25','R-dan-53','R-dan-50',
                    'R-dan-27', 'R-dan-28', 'R-dan-29', 'R-dan-30',
                    'R-dan-31', 'R-dan-34', 'R-dan-35', 'R-dan-36',
                    'R-dan-37', 'R-dan-38', 'R-dan-39', 'R-dan-40', 'R-dan-41',]

    # 胆-left
    jl_dan_left = ['L-dan-21', 'L-dan-22', 'L-dan-23', 'L-dan-24', 'L-dan-25','L-dan-53','L-dan-50',
                   'L-dan-27', 'L-dan-28', 'L-dan-29', 'L-dan-30',
                   'L-dan-31', 'L-dan-34', 'L-dan-35', 'L-dan-36', 'L-dan-37',
                   'L-dan-38', 'L-dan-39', 'L-dan-40', 'L-dan-41']

    #新增胆经3个点
    jl_dan_middle = ['L-dan-26','L-dan-51','L-dan-52','R-dan-26','R-dan-51','R-dan-52']



    jl_pangguang_left = ['L-pangguang-25', 'L-pangguang-26']
    jl_pangguang_right = ['R-pangguang-25', 'R-pangguang-26']

    jl_middle_up_nei_care = ['L-pi-1', 'L-pi-2', 'L-pi-3', 'L-pi-4',
                   'L-pi-5', 'L-pi-6', 'L-pi-7', 'L-pi-8','L-pi-9','L-pi-10','L-pi-11','L-pi-12', 
                   'R-pi-1', 'R-pi-2', 'R-pi-3', 'R-pi-4',
                   'R-pi-5', 'R-pi-6', 'R-pi-7', 'R-pi-8','R-pi-9','R-pi-10','R-pi-11','R-pi-12']+jl_xingbao+jl_wei_middle
    # jl_middle_up_nei_care =  jl_xingbao +jl_wei_middle
    jl_middle_down_wai_care= ['L-sanjiao-1', 'L-sanjiao-2', 'L-sanjiao-3', 'L-sanjiao-4', 'L-sanjiao-5',
                  'L-sanjiao-6', 'L-sanjiao-7','L-sanjiao-8','L-sanjiao-9', 'R-sanjiao-1', 'R-sanjiao-2', 'R-sanjiao-3', 'R-sanjiao-4',
                  'R-sanjiao-5','R-sanjiao-6', 'R-sanjiao-7', 'R-sanjiao-8', 'R-sanjiao-9',
                'L-pangguang-9', 'L-pangguang-10', 'L-pangguang-11', 'L-pangguang-12', 'L-pangguang-13',
                'L-pangguang-14', 'L-pangguang-15', 'L-pangguang-16', 'L-pangguang-17', 'L-pangguang-18',
                'L-pangguang-19', 'L-pangguang-20', 'L-pangguang-21', 'L-pangguang-22', 'L-pangguang-23',
                'L-pangguang-24', 'R-pangguang-9', 'R-pangguang-10',
                'R-pangguang-11', 'R-pangguang-12', 'R-pangguang-13',
                'R-pangguang-14', 'R-pangguang-15', 'R-pangguang-16', 'R-pangguang-17', 'R-pangguang-18',
                'R-pangguang-19', 'R-pangguang-20', 'R-pangguang-21', 'R-pangguang-22', 'R-pangguang-23',
                'R-pangguang-24']

    jl_head_left = ['R-sanjiao-8','R-sanjiao-9','R-sanjiao-10','R-sanjiao-11','R-sanjiao-12','R-sanjiao-13','R-sanjiao-14','R-sanjiao-15','R-sanjiao-16',
                    'R-sanjiao-17','R-sanjiao-18','R-sanjiao-19','R-sanjiao-20','R-sanjiao-21','R-sanjiao-22','R-sanjiao-23','R-sanjiao-24',
                    'R-dan-1','R-dan-2','R-dan-3','R-dan-4','R-dan-5','R-dan-6','R-dan-7','R-dan-8','R-dan-9','R-dan-10','R-dan-11','R-dan-12',
                    'R-dan-13','R-dan-14','R-dan-15','R-dan-16','R-dan-17','R-dan-18']
    jl_head_down_wai = ["R-pangguang-3","R-pangguang-4","R-pangguang-5","R-pangguang-6","R-pangguang-7",
                        "L-pangguang-3","L-pangguang-4","L-pangguang-5","L-pangguang-6","L-pangguang-7",
                        ]
    jl_head_middle_down_wai = ['R-pangguang-7','R-pangguang-30','R-pangguang-8',
                            'L-pangguang-7','L-pangguang-30','L-pangguang-8',]


    jl_pi_yolo_test = ['L-pi-1', 'L-pi-2', 'L-pi-3', 'L-pi-4',
                   'L-pi-5', 'L-pi-6', 'L-pi-7', 'L-pi-8','L-pi-9','L-pi-10','L-pi-11','L-pi-12', 
                   'R-pi-1', 'R-pi-2', 'R-pi-3', 'R-pi-4',
                   'R-pi-5', 'R-pi-6', 'R-pi-7', 'R-pi-8','R-pi-9','R-pi-10','R-pi-11','R-pi-12']

    jl_whole_middle_down_wai = jl_middle_down_wai_care + jl_head_middle_down_wai

    jl_right_head_left_down_wai = ['R-sanjiao-8', 'R-sanjiao-9', 'R-sanjiao-10', 'R-sanjiao-11', 'R-sanjiao-12', 'R-sanjiao-13', 'R-sanjiao-14', 'R-sanjiao-15', 'R-sanjiao-16', 'R-sanjiao-17', 'R-sanjiao-18', 'R-sanjiao-19', 'R-sanjiao-20', 'R-sanjiao-21', 'R-sanjiao-22', 'R-sanjiao-23', 'R-sanjiao-24',
                                   'R-dan-1', 'R-dan-2', 'R-dan-3', 'R-dan-4', 'R-dan-5', 'R-dan-6', 'R-dan-7', 'R-dan-8', 'R-dan-9', 'R-dan-10', 'R-dan-11', 'R-dan-12', 'R-dan-13', 'R-dan-14', 'R-dan-15', 'R-dan-16', 'R-dan-17', 'R-dan-18']

    jl_left_foot_left_up_nei = ['L-dan-40','L-dan-41','L-gan-1','L-gan-2']



    # *********************************************合并经络-pointName******************************************************************
    jl_left_down_wai = jl_head_left

    jl_right_down_wai = jl_pangguang_left

    # 经络（left-up-nei    左侧 胆经 ）
    jl_left_up_nei = jl_dan_left

    # 经络（left-up-wai    左侧 心经 肝经 脾经）
    jl_left_up_wai = jl_gan_left + jl_pi_left + jl_xin_left

    # 经络（middle-down-nei   肾经(下)）
    jl_middle_down_nei = jl_shenjing_xiashen

    # 经络（middle-down-wai   大肠  三焦  小肠   膀胱）
    jl_middle_down_wai = jl_sanjiao

    # 经络（middle-up-nei   肾经(上)  心包  肺 胃 胆）
    # jl_middle_up_nei = jl_shenjing_shangshen + jl_xingbao + jl_fei + jl_wei_middle +jl_dan_middle
    jl_middle_up_nei = jl_wei_middle
    
    # 经络（middle-up-wai   脾经）
    jl_middle_up_wai = jl_pi_middle

    # 经络（right-up-nei  right(胆经)）
    jl_right_up_nei = jl_dan_right

    # 经络（right-up-wai  right(肝经 脾经 心经)）
    jl_right_up_wai = jl_gan_right + jl_pi_right + jl_xin_right


    jl_partial_middle_up_nei = ['L-pi-1', 'L-pi-2', 'L-pi-3', 'L-pi-4','L-pi-5', 'L-pi-6', 'L-pi-7',
                            'R-pi-1', 'R-pi-2', 'R-pi-3', 'R-pi-4','R-pi-5', 'R-pi-6', 'R-pi-7',
                            'L-wei-24', 'L-wei-25', 'L-wei-26', 'L-wei-27', 'L-wei-28', 'L-wei-29', 'L-wei-30',
                            'R-wei-24', 'R-wei-25', 'R-wei-26', 'R-wei-27', 'R-wei-28', 'R-wei-29', 'R-wei-30']


    #36 个点
    jl_yolo_kp = ['L-xinbao-1', 'L-xinbao-2', 'L-xinbao-3', 'L-xinbao-4', 'L-xinbao-5',
                    'R-xinbao-1', 'R-xinbao-2', 'R-xinbao-3', 'R-xinbao-4', 'R-xinbao-5',
                    'L-wei-15', 'L-wei-16', 'L-wei-17', 'L-wei-18', 'L-wei-19', 'L-wei-20', 'L-wei-21', 'L-wei-22',
                     'L-wei-23','L-wei-24', 'L-wei-25', 'L-wei-26', 'L-wei-27',
                     'R-wei-15', 'R-wei-16', 'R-wei-17', 'R-wei-18', 'R-wei-19', 'R-wei-20', 'R-wei-21', 'R-wei-22',
                     'R-wei-23','R-wei-24', 'R-wei-25', 'R-wei-26', 'R-wei-27']


    baseDir = "/911G/data/new_all_jldata/20230410/left_up_nei/"
    EightModelList = [
        [jl_left_foot_left_up_nei, 'train_crop/left_foot'],
        [jl_left_foot_left_up_nei, 'test_crop/left_foot'],
        ]

    # # 生成手脚18个模型的数据集json文件
    # for jlname, dir1 in cropdict:
    #     labelme_directory = rootdir + dir1
    #     labelme_json = glob.glob(os.path.join(labelme_directory, "*.json"))
    #     output = labelme_directory + ".json"
    #     labelme2coco(jlname, labelme_json, output)

    # 生成8个模型的数据集json文件
    for jlname, dir1 in EightModelList:
        # print(dir1)
        labelme_directory = baseDir + dir1
        labelme_json = glob.glob(os.path.join(labelme_directory, "*.json"))
        output = labelme_directory + ".json"
        labelme2coco(jlname, labelme_json, output)
