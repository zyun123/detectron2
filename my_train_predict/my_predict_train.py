
import random
from detectron2.utils.visualizer import Visualizer
from detectron2.data.catalog import MetadataCatalog, DatasetCatalog
import pothole_data
import cv2
from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg
import os
from detectron2.engine.defaults import DefaultPredictor
from detectron2.utils.visualizer import ColorMode


DATASET_STR = "pothole_train"
IMAGE_STR = 'mydataset/train2017/img001.jpg'

pothole_metadata = MetadataCatalog.get(DATASET_STR)
MetadataCatalog.get(DATASET_STR).thing_classes = ["car", "dashedline", "midlane", "pothole", "rightlane"]
#MetadataCatalog.get(DATASET_STR).thing_colors = [(255, 0, 255), (47, 255, 173), (255, 255, 0), (71, 99, 255), (205, 250, 255)]


if __name__ == "__main__":
    cfg = get_cfg()
    cfg.merge_from_file(
        "configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"
    )
    cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, "model_final.pth")
    print('loading from: {}'.format(cfg.MODEL.WEIGHTS))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5   # set the testing threshold for this model
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 5
    cfg.DATASETS.TEST = (DATASET_STR, )
    predictor = DefaultPredictor(cfg)

    data_f = IMAGE_STR
    im = cv2.imread(data_f)
    outputs = predictor(im)
    v = Visualizer(im[:, :, ::-1],
                   metadata=pothole_metadata,
                   #scale=0.8,
                   #instance_mode=ColorMode.IMAGE_BW   # remove the colors of unsegmented pixels
                   )
    v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    img = v.get_image()[:, :, ::-1]
    cv2.imshow('mask_rcnn instance segmentation', img)
    cv2.waitKey(0)
