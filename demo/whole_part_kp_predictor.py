# Copyright (c) Facebook, Inc. and its affiliates.
import argparse
import glob
import json
import multiprocessing as mp
import numpy as np
import os
import tempfile
import time
import torch
import warnings
import cv2
import tqdm
from re_process import main_reprocess
from detectron2.config import get_cfg
from detectron2.data.detection_utils import read_image
from detectron2.utils.logger import setup_logger

from predictor import VisualizationDemo
from detectron2.data.catalog import MetadataCatalog
# constants
from keypoints_names import *
# from detectron2 import COCO_PERSON_KEYPOINT_NAMES_UP
# from detectron2 import *
from save_kp_json import save_predictions_to_json,replace_jsfile_box,merge_pred_to_other_json
WINDOW_NAME = "kp detections"

def setup_cfg(args,kp_use_mean_std,kp_names_key):
    # load config from file and command-line arguments
    cfg = get_cfg()
    # To use demo for Panoptic-DeepLab, please uncomment the following two lines.
    # from detectron2.projects.panoptic_deeplab import add_panoptic_deeplab_config  # noqa
    # add_panoptic_deeplab_config(cfg)
    cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(args.opts)
    # Set score_threshold for builtin models
    # cfg.MODEL.RETINANET.SCORE_THRESH_TEST = args.confidence_threshold
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = args.confidence_threshold
    cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = args.confidence_threshold
    if args.use_mean_std:
        cfg.MODEL.PIXEL_MEAN = kp_use_mean_std[kp_names_key]["mean"]
        cfg.MODEL.PIXEL_STD = kp_use_mean_std[kp_names_key]["std"]
    cfg.freeze()
    return cfg


def get_parser():
    parser = argparse.ArgumentParser(description="Detectron2 demo for builtin configs")
    parser.add_argument(
        "--config-file",
        default="configs/quick_schedules/mask_rcnn_R_50_FPN_inference_acc_test.yaml",
        metavar="FILE",
        help="path to config file",
    )
    parser.add_argument("--webcam", action="store_true", help="Take inputs from webcam.")
    parser.add_argument("--save-json", action="store_true", help="Take inputs from webcam.")
    parser.add_argument("--compare_predict_res", action="store_true", help="Take inputs from webcam.")
    parser.add_argument("--use-mean-std", action="store_true", help="Take inputs from webcam.")
    parser.add_argument("--video-input", help="Path to video file.")
    parser.add_argument("--part-model", default="",help="left_hand,left_foot,right_hand,right_foot")

    parser.add_argument(
        "--input",
        nargs="+",
        help="A list of space separated input images; "
        "or a single glob pattern such as 'directory/*.jpg'",
    )
    parser.add_argument(
        "--output",
        help="A file or directory to save output visualizations. "
        "If not given, will show output in an OpenCV window.",
    )

    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=0.5,
        help="Minimum score for instance predictions to be shown",
    )
    parser.add_argument(
        "--opts",
        help="Modify config options using the command-line 'KEY VALUE' pairs",
        default=[],
        nargs=argparse.REMAINDER,
    )
    return parser


def test_opencv_video_format(codec, file_ext):
    with tempfile.TemporaryDirectory(prefix="video_format_test") as dir:
        filename = os.path.join(dir, "test_file" + file_ext)
        writer = cv2.VideoWriter(
            filename=filename,
            fourcc=cv2.VideoWriter_fourcc(*codec),
            fps=float(30),
            frameSize=(10, 10),
            isColor=True,
        )
        [writer.write(np.zeros((10, 10, 3), np.uint8)) for _ in range(30)]
        writer.release()
        if os.path.isfile(filename):
            return True
        return False

if __name__ == "__main__":
    
    mp.set_start_method("spawn", force=True)
    args = get_parser().parse_args()
    setup_logger(name="fvcore")
    logger = setup_logger()
    logger.info("Arguments: " + str(args))

    #middle_down_wai  包含头部56个点
    # kp_names_down = MIDDLE_DOWN_CARE+HEAD_MIDDLE_DOWN
    # kp_rules_down = RULES_WHOLE_DOWN

    #middle_down_wai  90个点
    # kp_names_down = MIDDLE_DOWN_ALL_JL
    # kp_rules_down = RULES_WHOLE_DOWN

    #middle_down_nei 28个点
    # kp_names_down = DOWN_NEI
    # kp_rules_down = RULES_WHOLE_DOWN

    #middle_up_nei  84个点  老版本
    # kp_names_up = MIDDLE_UP_ALL_JL
    # kp_rules_up = RULES_UP

    #middle_up_nei 无肺经  74个点
    # kp_names_up = MIDDLE_UP_WITHOUT_FEI
    # kp_rules_up = RULES_UP

    #middle_up_nei 有肺经  90个点
    # kp_names_up = MIDDLE_UP_WITH_FEI
    # kp_rules_up = RULES_UP



    #middle_up_nei  partial leg 28个点
    # kp_names_up = PARTIAL_LEG_UP
    # kp_rules_up = RULES_UP

    #middle_up_nei partial hand 8个点
    # kp_names_up = PARTIAL_LEFT_HAND_UP
    # kp_names_up = PARTIAL_RIGHT_HAND_UP
    # kp_rules_up = RULES_UP

    #middle_up_nei left_hand 局部图局部识别 只有心包经 5个点 
    # kp_names_up = UP_LEFT_HAND
    # kp_rules_up = RULES_UP
    
    # #middle_up_nei right_hand 局部图局部识别 只有心包经 5个点 
    # kp_names_up = UP_RIGHT_HAND
    # kp_rules_up = RULES_UP

    #middle_up_nei left_foot 局部图局部识别  7个点 
    # kp_names_up = UP_LEFT_FOOT
    # kp_rules_up = RULES_UP

    #middle_up_nei right_foot 局部图局部识别  7个点 
    kp_names_up = UP_RIGHT_FOOT
    kp_rules_up = RULES_UP

    # #middle_down_wai  left hand 3个点
    # kp_names_down = DOWN_LEFT_HAND
    # kp_rules_down = RULES_WHOLE_DOWN

    #middle_down_wai  left hand 3个点
    kp_names_down = DOWN_RIGHT_HAND
    kp_rules_down = RULES_WHOLE_DOWN



    kp_use_mean_std = {"down":{"mean":[140.871, 146.204, 151.602],"std":[43.098, 30.778, 25.503]},
                        "up":{"mean":[141.584,147.873,152.721],"std":[42.925,30.753,25.354]}}


    kp_name_rule_dict = {"down":{"kp_names":kp_names_down,"kp_rules":kp_rules_down},
                        "up":{"kp_names":kp_names_up,"kp_rules":kp_rules_up}}

    kp_names_key = os.path.basename(args.config_file).split("_")[1]
    kp_names = kp_name_rule_dict[kp_names_key]["kp_names"]
    kp_rules = kp_name_rule_dict[kp_names_key]["kp_rules"]
    metadata = {
            "thing_classes": ["person"],
            "keypoint_names": kp_names,
            "keypoint_connection_rules": kp_rules,
        }
    cfg = setup_cfg(args,kp_use_mean_std,kp_names_key)
    MetadataCatalog.get(cfg.DATASETS.TEST[0]).set(**metadata)
    device = torch.device("cuda:0" if torch.cuda.is_available else "cpu")
    demo = VisualizationDemo(cfg,parallel = False)

    model_label = {"left_hand": "L-xinbao-6", 
                   "right_hand": "R-xinbao-6", 
                   "left_foot": "L-wei-28",
                    "right_foot": "R-wei-28"}


    if args.input:
        if len(args.input) == 1:
            args.input = glob.glob(os.path.expanduser(args.input[0]))
            assert args.input, "The input path(s) was not found"
        image_list = glob.glob(os.path.join(args.input[0],"*.jpg"))
        ret = True
        h_flip = False
        compare_predict_res = args.compare_predict_res
        another_image = None
        replace_box = False
        for path in tqdm.tqdm(image_list, disable=not args.output):
            # use PIL, to be consistent with evaluation
            js_file = path.replace("jpg", "json")
            img = read_image(path, format="BGR")
            

            #裁剪图像
            with open(js_file, "r") as f:
                data_dict = json.load(f)
            shapes = data_dict["shapes"]
            label = model_label[args.part_model]
            if args.part_model in ["left_foot","right_foot"]:
                other_label = label.replace("28","27")
                point = [shape["points"][0] for shape in shapes if shape["label"] == label or shape["label"] ==other_label]
                center_point = [(point[0][0] + point[1][0]) // 2, (point[0][1] + point[1][1]) // 2]
            else:
                center_point = [shape["points"][0] for shape in shapes if shape["label"] == label][0]


            #crop img with center point
            start_x = max(int(center_point[0] -100),0)
            start_y = max(int(center_point[1] -100),0)
            end_x = min(int(center_point[0] +100),img.shape[1])
            end_y = min(int(center_point[1] +100), img.shape[0])
            
            new_img = img[start_y:end_y,start_x:end_x].copy()
            cv2.imshow("new_img",new_img)
            cv2.waitKey(1)
            # draw = img.copy()
            # draw = cv2.imread(path.replace(args.input[0],"/911G/data/cure_images/上位机第一次识别图像/局部图预测draw整体图像right_hand"))

            if h_flip:
                # img = np.rot90(img,2)
                img = cv2.flip(img,1)
            if compare_predict_res:
                another_image = read_image(os.path.join("/911G/data/temp/20221229新加手托脚托新数据/middle_up_nei_精确标注132套新增/train_cgrec",
                                                        os.path.basename(path)),format="RGB")
            start_time = time.time()
            # cv2.imshow("test_image",img)
            predictions, visualized_output = demo.run_on_image(new_img,compare_predict_res=compare_predict_res,another_image=another_image)
            if not predictions:
                print("predict error")
                continue
            time1 = time.time()
            print("predict use time :##############",time1-start_time)
            #---------------test-process keypoints--测试对称性--------------------------------
            keypoints = predictions['instances'].pred_keypoints.squeeze().cpu().numpy().tolist()
            
            if args.save_json:
                # keypoints = predictions['instances'].pred_keypoints.squeeze().cpu().numpy().tolist()
                if len(keypoints) == 0:
                    continue
                json_path = path.replace("jpg","json")

                #与标注中途报错的断开  可以吧注释打开
                # if os.path.exists(json_path):
                #     continue
                if h_flip:
                    new_kp_names = []
                    for i,name in enumerate(kp_names):
                        if name.startswith("R"):
                            new_kp_names.append(kp_names[i].replace("R","L"))
                        elif name.startswith("L"):
                            new_kp_names.append(kp_names[i].replace("L","R"))
                else:
                    new_kp_names = kp_names
                
                if replace_box:
                    replace_jsfile_box(predictions,js_file)
                else:
                    keypoints = [[kp[0]+start_x, kp[1]+start_y] for kp in keypoints]
                    box_list = predictions["instances"].pred_boxes.tensor.cpu().numpy()+np.array([[start_x,start_y,start_x,start_y]],dtype = np.float32)
                    box_list = box_list.tolist()
                    #正常的保存预测内容到json文件
                    save_predictions_to_json(box_list,keypoints,new_kp_names,path,h_flip)

                    #合并预测内容和原有的标注内容
                    # merge_pred_to_other_json(keypoints,kp_names,origin_json_path=json_path)
                    # pass


            
            # ret = main_reprocess(keypoints,os.path.basename(cfg.MODEL.WEIGHTS)[:-4])
            # if not ret:
            #     logger.warning("file  {} predict err ".format(os.path.basename(path)))
            #     # print("file  {} predict err ".format(os.path.basename(path)))
            #     with open("/home/zy/Desktop/predict_res.txt","a") as f:
            #         f.write("file  {} predict err \n".format(os.path.basename(path)))
            # os.path
            logger.info(
                "{}: {} in {:.2f}s".format(
                    path,
                    "detected {} instances".format(len(predictions["instances"]))
                    if "instances" in predictions
                    else "finished",
                    time.time() - start_time,
                )
            )
            # os.makedirs(args.output)
            
            if args.output:
                if not os.path.exists(args.output):
                    os.makedirs(args.output)
                
                if os.path.isdir(args.output):
                    assert os.path.isdir(args.output), args.output
                    out_filename = os.path.join(args.output, os.path.basename(path))
                else:
                    assert len(args.input) == 1, "Please specify a directory with args.output"
                    out_filename = args.output
                vis = dict(zip(kp_names,keypoints))
                for kp in keypoints:
                    x = int(kp[0])
                    y = int(kp[1])
                    cv2.circle(draw, (int(x)+start_x, int(y)+start_y),radius=2, color=255, thickness=-1, lineType=cv2.LINE_AA)
                    # cv2.circle(new_img, (int(x), int(y)),radius=2, color=255, thickness=-1, lineType=cv2.LINE_AA)

                for kp0, kp1, color in kp_rules:
                    if kp0 in vis and kp1 in vis:
                        x0, y0,_ = vis[kp0]
                        x1, y1,_ = vis[kp1]
                        cv2.line(draw,(int(x0)+start_x,int(y0)+start_y),(int(x1)+start_x,int(y1)+start_y),(255,0,0))
                        # cv2.line(new_img,(int(x0),int(y0)),(int(x1),int(y1)),(255,0,0))
                cv2.imshow("img",draw)
                cv2.waitKey(1)
                # cv2.destroyAllWindows()
                cv2.imwrite(out_filename,draw)
                # visualized_output.save(out_filename)
            else:
                cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
                cv2.imshow(WINDOW_NAME, visualized_output.get_image()[:, :, ::-1])
                if cv2.waitKey(1) == 27:
                    break  # esc to quit


