
import glob
import json
import logging
import random
import time
from detectron2.utils.visualizer import Visualizer
from detectron2.data.catalog import MetadataCatalog, DatasetCatalog
# import pothole_data
import cv2
from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg
import os
from detectron2.engine.defaults import DefaultPredictor
from detectron2.utils.visualizer import ColorMode
from detectron2.utils.logger import setup_logger
from detectron2.data.datasets import register_coco_instances, load_coco_json
# register_coco_instances("pothole_train", {}, "mydataset/instances_train2017.json", "mydataset/train2017")
register_coco_instances("person_test", 
                        {}, 
                        "/911G/data/temp/zhengfan_train_data/train.json", 
                        "/911G/data/temp/zhengfan_train_data/images")

DATASET_STR = "person_test"
IMAGE_STR = '/911G/data/temp/zhengfan_train_data/images/000005.jpg'
person_metadata = MetadataCatalog.get(DATASET_STR)
MetadataCatalog.get(DATASET_STR).thing_classes = ["fanmian", "zhengmian"]
#MetadataCatalog.get(DATASET_STR).thing_colors = [(255, 0, 255), (47, 255, 173), (255, 255, 0), (71, 99, 255), (205, 250, 255)]


if __name__ == "__main__":
    logger = setup_logger(name = "person zhengfan detect")
    cfg = get_cfg()
    cfg.merge_from_file(
        "configs/COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"
    )
    cfg.MODEL.WEIGHTS = os.path.join("output/2023-01-04-person", "model_final.pth")
    print('loading from: {}'.format(cfg.MODEL.WEIGHTS))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5   # set the testing threshold for this model
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 2
    cfg.DATASETS.TEST = (DATASET_STR, )
    predictor = DefaultPredictor(cfg)

    imgRoot = "/911G/data/temp/zhengfan_train_data/images"
    trainJson = "/911G/data/temp/zhengfan_train_data/train.json"
    person_data = load_coco_json(trainJson ,imgRoot)



    f = open("predict_res.txt","w")
    for instance in person_data:
        t1 = time.time()
        imgPath = instance["file_name"]
        truth_label = instance["annotations"][0]["category_id"]   #1 fanmian  or 2 zhengmian
        im = cv2.imread(imgPath)
        outputs = predictor(im)
        predict_label = outputs["instances"].pred_classes.tolist()[0] +1
        t2 = time.time()
        logger.info("predict single image use time: {} s".format(t2-t1))
        print("predict single image use time:",t2-t1, "s")
        if predict_label != truth_label:
            logger.warning("predict error {}".format(imgPath))
            f.write("predict error {} \n".format(imgPath))

        v = Visualizer(im[:, :, ::-1],
                    metadata=person_metadata,
                    #scale=0.8,
                    #instance_mode=ColorMode.IMAGE_BW   # remove the colors of unsegmented pixels
                    )
        v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
        img = v.get_image()[:, :, ::-1]
        cv2.imshow('faster rcnn instance detection', img)
        cv2.waitKey(1)
    f.close()
