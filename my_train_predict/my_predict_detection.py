import random
from detectron2.utils.visualizer import Visualizer
from detectron2.data.catalog import MetadataCatalog, DatasetCatalog
import cv2
from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg
from detectron2.utils.logger import setup_logger
import os
setup_logger()
from detectron2.data.datasets import register_coco_instances

metadata ={
    "thing_classes":["fanmian","zhengmian"],

}
register_coco_instances("person_train",
                        metadata,
                        "/911G/data/temp/zhengfan_train_data/train.json",
                        "/911G/data/temp/zhengfan_train_data/images")

if __name__ == "__main__":
    cfg = get_cfg()
    cfg.merge_from_file(
        "configs/COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"
    )
    cfg.DATASETS.TRAIN = ("person_train",)
    cfg.DATASETS.TEST = ()  # no metrics implemented for this dataset
    cfg.DATALOADER.NUM_WORKERS = 2
    # cfg.MODEL.WEIGHTS = "detectron2://COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x/137849600/model_final_f10217.pkl"  # initialize from model zoo
    cfg.MODEL.WEIGHTS = "/home/zy/Downloads/model_final_280758.pkl"  # initialize from model zoo
    cfg.SOLVER.IMS_PER_BATCH = 2
    cfg.SOLVER.BASE_LR = 0.001
    cfg.SOLVER.STEPS = (7000, 8000)
    cfg.SOLVER.MAX_ITER = (9000)  # 36000 iterations seems good enough, but you can certainly train longer
    cfg.SOLVER.CHECKPOINT_PERIOD = 2000 
    cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = (128)  # faster, and good enough for this dataset
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 2  # 5 classes
    cfg.OUTPUT_DIR = "./output/2023-01-04-person"
    os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
    trainer = DefaultTrainer(cfg)
    trainer.resume_or_load(resume=False)
    trainer.train()
