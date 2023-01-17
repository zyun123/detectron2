from detectron2.data.datasets import register_coco_instances
register_coco_instances("pothole_train", {}, "mydataset/instances_train2017.json", "mydataset/train2017")
register_coco_instances("pothole_test", {}, "mydataset/instances_val2017.json", "mydataset/val2017")
