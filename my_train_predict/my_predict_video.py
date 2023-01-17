
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

import time
import datetime
import copy


DATASET_STR = "pothole_test"
pothole_metadata = MetadataCatalog.get(DATASET_STR)
MetadataCatalog.get(DATASET_STR).thing_classes = ["car", "dashedline", "midlane", "pothole", "rightlane"]
MetadataCatalog.get(DATASET_STR).thing_colors = [(255, 0, 255), (47, 255, 173), (255, 255, 0), (71, 99, 255), (205, 250, 255)]


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

    capture = cv2.VideoCapture(r'./drive.mp4')
    size = (
        int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    )
    

    save_dir = os.path.join(os.getcwd(), "./output")
    if not os.path.exists(save_dir):
       os.makedirs(save_dir)

    file_name = "video_masked_{:%Y%m%dT%H%M%S}.mp4".format(datetime.datetime.now())
    file_name = os.path.join(save_dir, file_name)

    #fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    fps = int(capture.get(cv2.CAP_PROP_FPS))
    output = cv2.VideoWriter(file_name, fourcc, fps, size)

    while True:
        start_time = time.time()
        ret_val, img = capture.read()
        
        if ret_val:
            outputs = predictor(img)
            v = Visualizer(
                   img[:, :, ::-1],
                   metadata=pothole_metadata,
                   #scale=0.8,
                   #instance_mode=ColorMode.IMAGE_BW   # remove the colors of unsegmented pixels
                   )
            v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
            img = v.get_image()[:, :, ::-1]
        
            print("Time: {:.2f} s / img".format(time.time() - start_time))
            cv2.imshow('mask_rcnn instance segmentation', img)
            output.write(img)
        else: break
        if cv2.waitKey(1) == 27:
            break  # esc to quit
    capture.release()
    output.release()
    cv2.destroyAllWindows()


