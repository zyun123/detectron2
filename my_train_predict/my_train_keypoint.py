import logging
import random
import shutil

import yaml
import detectron2.data.transforms as T
from detectron2.modeling.test_time_augmentation import GeneralizedRCNNWithTTA
from detectron2.utils.visualizer import Visualizer
from detectron2.data.catalog import MetadataCatalog, DatasetCatalog
from detectron2.data import DatasetMapper,build_detection_train_loader
from collections import OrderedDict
from detectron2.engine import DefaultTrainer, hooks
from detectron2.evaluation import COCOEvaluator, DatasetEvaluators
from detectron2.config import get_cfg
from detectron2.utils.logger import setup_logger
import os
from detectron2.data.datasets import register_coco_instances
from demo.keypoints_names import *
kp_names = MIDDLE_DOWN_CARE+HEAD_MIDDLE_DOWN
kp_rules = RULES_WHOLE_DOWN
# kp_names = COCO_PERSON_KEYPOINT_NAMES_UP
# kp_rules = KEYPOINT_CONNECTION_RULES_UP
metadata = {
            "thing_classes": ["person"],
            "keypoint_names": kp_names,
            "keypoint_connection_rules": kp_rules,
            "keypoint_flip_map": [],
        }
register_coco_instances("middle_down_wai_train",
                        metadata, 
                        "/911G/data/temp/20221229新加手托脚托新数据/精确标注320套middle_down_wai_change_rec/train.json", 
                        "/911G/data/temp/20221229新加手托脚托新数据/精确标注320套middle_down_wai_change_rec/train")

register_coco_instances("middle_down_wai_test", 
                        metadata, 
                        "/911G/data/temp/20221229新加手托脚托新数据/精确标注320套middle_down_wai_change_rec/test.json", 
                        "/911G/data/temp/20221229新加手托脚托新数据/精确标注320套middle_down_wai_change_rec/test")
setup_logger()

def build_keypoint_train_aug(cfg):
    augs = [
        T.ResizeShortestEdge(
            cfg.INPUT.MIN_SIZE_TRAIN, cfg.INPUT.MAX_SIZE_TRAIN, cfg.INPUT.MIN_SIZE_TRAIN_SAMPLING
        )
    ]
    transform_list = [
        # T.RandomRotation(angle=[180, 0], expand=False, sample_style="choice"),
        # T.RandomRotation(angle=[-5, 5], expand=False),
        # T.RandomContrast(intensity_min = 0.75,intensity_max = 1.25),
        # T.RandomBrightness(intensity_min = 0.75,intensity_max = 1.25),
        # T.RandomSaturation(intensity_min = 0.75,intensity_max = 1.25),
        # T.RandomLighting(scale=0.1),
        # T.RandomCrop(crop_type="relative_range",crop_size=(0.9,0.8)),
    ]
    augs.extend(transform_list)
    return augs

num_keypoints = len(kp_names)
sigmas = [0.006] *num_keypoints

class KeypointTrainer(DefaultTrainer):

    @classmethod
    def build_train_loader(cls,cfg):
        keypoint_names = ""
        mapper = DatasetMapper(cfg,is_train= True,augmentations = build_keypoint_train_aug(cfg))

        return build_detection_train_loader(cfg,mapper = mapper)

    @classmethod
    def build_evaluator(cls,cfg, dataset_name, output_folder=None):
        if output_folder is None:
            output_folder = os.path.join(cfg.OUTPUT_DIR, "inference")
        evaluator_list = []
        evaluator_type = MetadataCatalog.get(dataset_name).evaluator_type
        if evaluator_type in ["coco", "coco_panoptic_seg"]:
            evaluator_list.append(COCOEvaluator(dataset_name, output_dir=output_folder,kpt_oks_sigmas = sigmas))

        if len(evaluator_list) == 0:
            raise NotImplementedError(
                "no Evaluator for the dataset {} with the type {}".format(dataset_name, evaluator_type)
            )
        elif len(evaluator_list) == 1:
            return evaluator_list[0]
        return DatasetEvaluators(evaluator_list)
    
    @classmethod
    def test_with_TTA(cls,cfg,model):
        logger = logging.getLogger("detectron2.trainer")
        # In the end of training, run an evaluation with TTA
        # Only support some R-CNN models.
        logger.info("Running inference with test-time augmentation ...")
        model = GeneralizedRCNNWithTTA(cfg, model)
        evaluators = [
            cls.build_evaluator(
                cfg, name, output_folder=os.path.join(cfg.OUTPUT_DIR, "inference_TTA")
            )
            for name in cfg.DATASETS.TEST
        ]
        res = cls.test(cfg, model, evaluators)
        res = OrderedDict({k + "_TTA": v for k, v in res.items()})
        return res




if __name__ == "__main__":
    cfg = get_cfg()
    config_file = "configs/COCO-Keypoints/middle_down_wai_base.yaml"
    cfg.merge_from_file(config_file)
    cfg.DATASETS.TRAIN = ("middle_down_wai_train",)
    # cfg.DATASETS.TEST = ("middle_down_wai_test",)  # no metrics implemented for this dataset
    cfg.DATASETS.TEST = ()  # no metrics implemented for this dataset
 
    cfg.OUTPUT_DIR = "./output/2023-02-27-vis01"
    os.makedirs(cfg.OUTPUT_DIR,exist_ok = True)
    dst_config_file = os.path.join(cfg.OUTPUT_DIR,os.path.basename(config_file))
    shutil.copyfile(config_file,dst_config_file)
    # with open(dst_config_file,"r") as f:
    #     data = yaml.safe_load(f)
    #     data['_BASE_'] = "configs/COCO-Keypoints/Base-Keypoint-RCNN-FPN.yaml"
    # with open(dst_config_file,"w") as f:
    #     yaml.safe_dump(data,f)
    #     logging.info(f"{dst_config_file} saved")
    trainer = KeypointTrainer(cfg)

    trainer.resume_or_load(resume=True)
    if cfg.TEST.AUG.ENABLED:
        trainer.register_hooks(
            [hooks.EvalHook(0, lambda: trainer.test_with_TTA(cfg, trainer.model))]
        )
    trainer.train()
