"""
将hand,foot预测json文件合并
"""
import json
import os

def get_shapes(json_path):
        '''得到json'内容'''
        with open(json_path, 'r') as f:
            dataDict = json.load(f)
            return dataDict["shapes"]

def merge_instance(left_hand_json,right_hand_json,left_foot_json,right_foot_json,js_file,dst_dir,):
    new_shapes = []
    left_hand_shapes = get_shapes(left_hand_json)
    right_hand_shapes = get_shapes(right_hand_json)
    left_foot_shapes = get_shapes(left_foot_json)
    right_foot_shapes = get_shapes(right_foot_json)

    new_shapes.extend(left_hand_shapes)
    new_shapes.extend(right_hand_shapes)
    new_shapes.extend(left_foot_shapes)
    new_shapes.extend(right_foot_shapes)

    img_file = js_file.replace("json","jpg")
    data_dict = {"version": "4.5.6",
                "flages": {},
                "imagePath": img_file,
                "imageData": None,
                "imageHeight": 720,
                "imageWidth": 1280,}
    data_dict["shapes"] = new_shapes
    with open(os.path.join(dst_dir,js_file),"w") as f:
        json.dump(data_dict,f,indent=4)


if __name__ == "__main__":
    left_hand_dir = "/911G/data/cure_images/上位机第一次识别图像/局部图局部识别left_hand"
    right_hand_dir = "/911G/data/cure_images/上位机第一次识别图像/局部图局部识别right_hand"
    left_foot_dir = "/911G/data/cure_images/上位机第一次识别图像/局部图局部识别left_foot"
    right_foot_dir = "/911G/data/cure_images/上位机第一次识别图像/局部图局部识别right_foot"
    dst_dir = "/911G/data/cure_images/上位机第一次识别图像/局部图局部识别"
    os.makedirs(dst_dir,exist_ok=True)
    for file in os.listdir(left_hand_dir):
        if file.endswith("json"):
            left_hand_json = os.path.join(left_hand_dir,file)
            right_hand_json = os.path.join(right_hand_dir,file)
            left_foot_json = os.path.join(left_foot_dir,file)
            right_foot_json = os.path.join(right_foot_dir,file)
            merge_instance(left_hand_json, right_hand_json,left_foot_json,right_foot_json,file,dst_dir)

