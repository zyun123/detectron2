
import random
from detectron2.utils.visualizer import Visualizer
from detectron2.data.catalog import MetadataCatalog, DatasetCatalog
import pothole_data
import cv2
from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg
import os
from detectron2.engine.defaults import DefaultPredictor
#from detectron2.utils.visualizer import ColorMode


from detectron2.evaluation import COCOEvaluator, inference_on_dataset
from detectron2.data import build_detection_test_loader


DATASET_STR = "pothole_test"

if __name__ == "__main__":
    cfg = get_cfg()
    cfg.merge_from_file(
        "../configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"
    )
    cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, "model_final.pth")
    print('loading from: {}'.format(cfg.MODEL.WEIGHTS))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5   # set the testing threshold for this model
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 5
    cfg.DATASETS.TEST = (DATASET_STR, )
    predictor = DefaultPredictor(cfg)

    evaluator = COCOEvaluator(DATASET_STR, output_dir="./output")
    val_loader = build_detection_test_loader(cfg, DATASET_STR)
    print(inference_on_dataset(predictor.model, val_loader, evaluator))
