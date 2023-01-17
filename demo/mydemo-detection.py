# Copyright (c) Facebook, Inc. and its affiliates.
import argparse
import glob
import multiprocessing as mp
import numpy as np
import os
import tempfile
import time
import warnings
import cv2
import tqdm
# from demo.re_process import main_reprocess
from detectron2.config import get_cfg
from detectron2.data.detection_utils import read_image
from detectron2.utils.logger import setup_logger

from predictor import VisualizationDemo
from detectron2.data.catalog import MetadataCatalog
# constants
from keypoints_names import *
# from detectron2 import COCO_PERSON_KEYPOINT_NAMES_UP
# from detectron2 import *
# from save_kp_json import save_predictions_to_json
WINDOW_NAME = "kp detections"

def setup_cfg(args):
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
    cfg.DATASETS.TEST = ("person_test", )
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
    parser.add_argument("--video-input", help="Path to video file.")
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


    metadata = {
            "thing_classes": ["fanmian","zhengmian"],
        }
    cfg = setup_cfg(args)
    MetadataCatalog.get("person_test").set(**metadata)


    
    demo = VisualizationDemo(cfg)


    #---------------------use realsense camera -----------------------------
    # from cameras.camera import Camera
    # serial_num = "851112061862"
    # camera = Camera(serial_num) 
    # while True:
    #     t1 = time.time()
    #     img, _ = camera.get_data()
    #     predictions, visualized_output = demo.run_on_image(img)
    #     cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    #     cv2.imshow(WINDOW_NAME, visualized_output.get_image()[:, :, ::-1])
    #     cv2.waitKey(1)
    #     # if cv2.waitKey(1) == 27:
    #     #     break  # esc to quit
    # img = read_image(args.input, format="BGR")
    # predictions, visualized_output = demo.run_on_image(img)
    # out_filename = args.input.replace("jpg", "json")
    # visualized_output.save(out_filename)



    if args.input:
        if len(args.input) == 1:
            args.input = glob.glob(os.path.expanduser(args.input[0]))
            assert args.input, "The input path(s) was not found"
        image_list = glob.glob(os.path.join(args.input[0],"*.jpg"))
        for path in tqdm.tqdm(image_list, disable=not args.output):
            # use PIL, to be consistent with evaluation
            
            img = read_image(path, format="BGR")
          
            start_time = time.time()
            # cv2.imshow("test_image",img)
            predictions, visualized_output = demo.run_on_image(img)
            if not predictions:
                print("predict error")
                continue
            time1 = time.time()
            print("predict use time :##############",time1-start_time)
          
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
                visualized_output.save(out_filename)
            else:
                cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
                cv2.imshow(WINDOW_NAME, visualized_output.get_image()[:, :, ::-1])
                if cv2.waitKey(1) == 27:
                    break  # esc to quit
        # with open("/home/zy/Desktop/predict_res.txt","a") as f:
        #     f.write("*"*45)
    # elif args.webcam:
    #     assert args.input is None, "Cannot have both --input and --webcam!"
    #     assert args.output is None, "output not yet supported with --webcam!"
    #     cam = cv2.VideoCapture(0)
    #     for vis in tqdm.tqdm(demo.run_on_video(cam)):
    #         cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    #         cv2.imshow(WINDOW_NAME, vis)
    #         if cv2.waitKey(1) == 27:
    #             break  # esc to quit
    #     cam.release()
    #     cv2.destroyAllWindows()
    # elif args.video_input:
    #     video = cv2.VideoCapture(args.video_input)
    #     width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    #     height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #     frames_per_second = video.get(cv2.CAP_PROP_FPS)
    #     num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    #     basename = os.path.basename(args.video_input)
    #     codec, file_ext = (
    #         ("x264", ".mkv") if test_opencv_video_format("x264", ".mkv") else ("mp4v", ".mp4")
    #     )
    #     if codec == ".mp4v":
    #         warnings.warn("x264 codec not available, switching to mp4v")
    #     if args.output:
    #         if os.path.isdir(args.output):
    #             output_fname = os.path.join(args.output, basename)
    #             output_fname = os.path.splitext(output_fname)[0] + file_ext
    #         else:
    #             output_fname = args.output
    #         assert not os.path.isfile(output_fname), output_fname
    #         output_file = cv2.VideoWriter(
    #             filename=output_fname,
    #             # some installation of opencv may not support x264 (due to its license),
    #             # you can try other format (e.g. MPEG)
    #             fourcc=cv2.VideoWriter_fourcc(*codec),
    #             fps=float(frames_per_second),
    #             frameSize=(width, height),
    #             isColor=True,
    #         )
    #     assert os.path.isfile(args.video_input)
    #     for vis_frame in tqdm.tqdm(demo.run_on_video(video), total=num_frames):
    #         if args.output:
    #             output_file.write(vis_frame)
    #         else:
    #             cv2.namedWindow(basename, cv2.WINDOW_NORMAL)
    #             cv2.imshow(basename, vis_frame)
    #             if cv2.waitKey(1) == 27:
    #                 break  # esc to quit
    #     video.release()
    #     if args.output:
    #         output_file.release()
    #     else:
    #         cv2.destroyAllWindows()
