#!/usr/bin/env python
# Copyright (c) Facebook, Inc. and its affiliates.
"""
A main training script.

This scripts reads a given config file and runs the training or evaluation.
It is an entry point that is made to train standard models in detectron2.

In order to let one script support training of many models,
this script contains logic that are specific to these built-in models and therefore
may not be suitable for your own project.
For example, your research project perhaps only needs a single "evaluator".

Therefore, we recommend you to use detectron2 as an library and take
this file as an example of how to use the library.
You may want to write your own script with your datasets and other customizations.
"""

import logging
import os
from collections import OrderedDict
from detectron2.data.datasets.coco import register_coco_instances
import detectron2.utils.comm as comm
from detectron2.checkpoint import DetectionCheckpointer
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.engine import DefaultTrainer, default_argument_parser, default_setup, hooks, launch
from detectron2.evaluation import (
    CityscapesInstanceEvaluator,
    CityscapesSemSegEvaluator,
    COCOEvaluator,
    COCOPanopticEvaluator,
    DatasetEvaluators,
    LVISEvaluator,
    PascalVOCDetectionEvaluator,
    SemSegEvaluator,
    verify_results,
)
from detectron2.modeling import GeneralizedRCNNWithTTA
kp_names = ['L-pi-1', 'L-pi-2', 'L-pi-3', 'L-pi-4', 'L-pi-5', 'L-pi-6', 'L-pi-7', 'L-pi-8', 'L-pi-9', 'L-pi-10', 'L-pi-11', 'L-pi-12', 'R-pi-1', 'R-pi-2', 'R-pi-3', 'R-pi-4', 'R-pi-5', 'R-pi-6', 'R-pi-7', 'R-pi-8', 'R-pi-9', 'R-pi-10', 'R-pi-11', 'R-pi-12', 'R-xinbao-1', 'R-xinbao-2', 'R-xinbao-3', 'R-xinbao-4', 'R-xinbao-5', 'R-xinbao-6', 'R-xinbao-7', 'R-xinbao-8', 'R-xinbao-9', 'L-xinbao-1', 'L-xinbao-2', 'L-xinbao-3', 'L-xinbao-4', 'L-xinbao-5', 'L-xinbao-6', 'L-xinbao-7', 'L-xinbao-8', 'L-xinbao-9', 'L-wei-15', 'L-wei-16', 'L-wei-17', 'L-wei-18', 'L-wei-19', 'L-wei-20', 'L-wei-21', 'L-wei-22', 'L-wei-23', 'L-wei-24', 'L-wei-25', 'L-wei-26', 'L-wei-27', 'L-wei-28', 'L-wei-29', 'L-wei-30', 'R-wei-15', 'R-wei-16', 'R-wei-17', 'R-wei-18', 'R-wei-19', 'R-wei-20', 'R-wei-21', 'R-wei-22', 'R-wei-23', 'R-wei-24', 'R-wei-25', 'R-wei-26', 'R-wei-27', 'R-wei-28', 'R-wei-29', 'R-wei-30']
train_ann_path = "/911G/data/temp/20221229新加手托脚托新数据/middle_up_nei_700/train.json"
train_image_dir  ="/911G/data/temp/20221229新加手托脚托新数据/middle_up_nei_700/train"
test_ann_path = "/911G/data/temp/20221229新加手托脚托新数据/middle_up_nei_700/test.json"
test_image_dir  ="/911G/data/temp/20221229新加手托脚托新数据/middle_up_nei_700/test"
metadata = {"thing_classes": ["person"],
        "keypoint_names": kp_names,
        "keypoint_connection_rules": [],
        "keypoint_flip_map": [],
            }
register_coco_instances("shanyi_dataset_train",metadata = metadata,json_file=train_ann_path,image_root = train_image_dir)  #注册训练数据集
register_coco_instances("shanyi_dataset_test",metadata = metadata,json_file=test_ann_path,image_root = test_image_dir) #注册验证数据集
def build_evaluator(cfg, dataset_name, output_folder=None):
    """
    Create evaluator(s) for a given dataset.
    This uses the special metadata "evaluator_type" associated with each builtin dataset.
    For your own dataset, you can simply create an evaluator manually in your
    script and do not have to worry about the hacky if-else logic here.
    """
    if output_folder is None:
        output_folder = os.path.join(cfg.OUTPUT_DIR, "inference")
    evaluator_list = []
    evaluator_type = MetadataCatalog.get(dataset_name).evaluator_type
    if evaluator_type in ["sem_seg", "coco_panoptic_seg"]:
        evaluator_list.append(
            SemSegEvaluator(
                dataset_name,
                distributed=True,
                output_dir=output_folder,
            )
        )
    if evaluator_type in ["coco", "coco_panoptic_seg"]:
        evaluator_list.append(COCOEvaluator(dataset_name, output_dir=output_folder))
    if evaluator_type == "coco_panoptic_seg":
        evaluator_list.append(COCOPanopticEvaluator(dataset_name, output_folder))
    if evaluator_type == "cityscapes_instance":
        return CityscapesInstanceEvaluator(dataset_name)
    if evaluator_type == "cityscapes_sem_seg":
        return CityscapesSemSegEvaluator(dataset_name)
    elif evaluator_type == "pascal_voc":
        return PascalVOCDetectionEvaluator(dataset_name)
    elif evaluator_type == "lvis":
        return LVISEvaluator(dataset_name, output_dir=output_folder)
    if len(evaluator_list) == 0:
        raise NotImplementedError(
            "no Evaluator for the dataset {} with the type {}".format(dataset_name, evaluator_type)
        )
    elif len(evaluator_list) == 1:
        return evaluator_list[0]
    return DatasetEvaluators(evaluator_list)


class Trainer(DefaultTrainer):
    """
    We use the "DefaultTrainer" which contains pre-defined default logic for
    standard training workflow. They may not work for you, especially if you
    are working on a new research project. In that case you can write your
    own training loop. You can use "tools/plain_train_net.py" as an example.
    """

    @classmethod
    def build_evaluator(cls, cfg, dataset_name, output_folder=None):
        return build_evaluator(cfg, dataset_name, output_folder)

    @classmethod
    def test_with_TTA(cls, cfg, model):
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


def setup(args):
    """
    Create configs and perform basic setups.
    """
    cfg = get_cfg()
    cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(args.opts)
    cfg.freeze()
    default_setup(cfg, args)
    return cfg


def main(args):
    cfg = setup(args)
    
    
    if args.eval_only:
        model = Trainer.build_model(cfg)
        DetectionCheckpointer(model, save_dir=cfg.OUTPUT_DIR).resume_or_load(
            cfg.MODEL.WEIGHTS, resume=args.resume
        )
        res = Trainer.test(cfg, model)
        if cfg.TEST.AUG.ENABLED:
            res.update(Trainer.test_with_TTA(cfg, model))
        if comm.is_main_process():
            verify_results(cfg, res)
        return res

    """
    If you'd like to do anything fancier than the standard training logic,
    consider writing your own training loop (see plain_train_net.py) or
    subclassing the trainer.
    """
    trainer = Trainer(cfg)
    trainer.resume_or_load(resume=args.resume)
    if cfg.TEST.AUG.ENABLED:
        trainer.register_hooks(
            [hooks.EvalHook(0, lambda: trainer.test_with_TTA(cfg, trainer.model))]
        )
    return trainer.train()


if __name__ == "__main__":
    



    args = default_argument_parser().parse_args()
    args.config_file = "configs/COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x_custom.yaml"
    args.num_gpu = 1
    args.resume =True #中断训练的时候
    print("Command Line Args:", args)
    launch(
        main,
        args.num_gpus,
        num_machines=args.num_machines,
        machine_rank=args.machine_rank,
        dist_url=args.dist_url,
        args=(args,),
    )
