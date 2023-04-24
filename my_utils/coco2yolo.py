from pycocotools.coco import COCO
import numpy as np
import tqdm
import argparse
import os
train_val = "val"
def arg_parser():
    parser = argparse.ArgumentParser('code by rbj')
    parser.add_argument('--annotation_path', type=str,default=f'/911G/data/temp/20221229新加手托脚托新数据/20230311_最新修改/coco_middle_up_nei/annotations/{train_val}.json')
    #生成的txt文件保存的目录
    parser.add_argument('--save_base_path', type=str, default=f'/911G/data/temp/20221229新加手托脚托新数据/20230311_最新修改/coco_middle_up_nei/labels/{train_val}')
    args = parser.parse_args(args=[])
    #原网页中是args = parser.parse_args()会报错，改成这个以后解决了
    return args
if __name__ == '__main__':
    args = arg_parser()
    annotation_path = args.annotation_path
    if not os.path.exists(annotation_path):
        raise Exception('please input right path!')
    save_base_path = args.save_base_path
    if not os.path.exists(save_base_path):
        os.makedirs(save_base_path)
    
    img_txt_dir = os.path.join(os.path.dirname(os.path.dirname(save_base_path)),"img_txt")
    if not os.path.exists(img_txt_dir):
        os.makedirs(img_txt_dir)

    root_txt_file = os.path.join(img_txt_dir,f"{train_val}.txt")
    data_source = COCO(annotation_file=annotation_path)
    catIds = data_source.getCatIds()
    categories = data_source.loadCats(catIds)
    categories.sort(key=lambda x: x['id'])
    classes = {}
    coco_labels = {}
    coco_labels_inverse = {}
    for c in categories:
        coco_labels[len(classes)] = c['id']
        coco_labels_inverse[c['id']] = len(classes)
        classes[c['name']] = len(classes)

    img_ids = data_source.getImgIds()
    for index, img_id in tqdm.tqdm(enumerate(img_ids), desc='change .json file to .txt file'):
        img_info = data_source.loadImgs(img_id)[0]
        file_name = img_info['file_name']
        height = img_info['height']
        width = img_info['width']

        save_path = os.path.join(save_base_path, file_name.replace("jpg","txt"))
        annotation_id = data_source.getAnnIds(img_id)
        # boxes = np.zeros((0, 5))
        if len(annotation_id) == 0:
            # fp.write('')
            continue
        with open(save_path, mode='w') as fp: 
            annotations = data_source.loadAnns(annotation_id)
            lines = ''
            for annotation in annotations:
                box = annotation['bbox']
                # some annotations have basically no width / height, skip them
                if box[2] < 1 or box[3] < 1:
                    continue
                #top_x,top_y,width,height---->cen_x,cen_y,width,height
                box[0] = round((box[0] + box[2] / 2) / width, 6)
                box[1] = round((box[1] + box[3] / 2) / height, 6)
                box[2] = round(box[2] / width, 6)
                box[3] = round(box[3] / height, 6)
                label = coco_labels_inverse[annotation['category_id']]
                lines = lines + str(label)
                for i in box:
                    lines += ' ' + str(i)
                
                if "keypoints" in annotation:
                    # keypoints = [round(x,3) for x in annotation['keypoints']]
                    keypoints = annotation['keypoints']
                    for i,kp in enumerate(keypoints):
                        if i %3 ==0:
                            lines += ' ' + str(round(kp/width,6))
                        elif i%3 == 1:
                            lines += ' ' + str(round(kp/height,6))
                        else:
                            lines += ' ' + str(kp)


                    lines += '\n'
            fp.writelines(lines)

    with open(root_txt_file,"w") as f:
        for filename in os.listdir(args.save_base_path):
            img_path = os.path.join(args.save_base_path.replace("labels", "images"),
                                        filename.split(".")[0]) + ".jpg"
            line = img_path + "\n"
            assert os.path.exists(img_path), "file:{} not exist!".format(img_path)
            f.write(line)

    print('finish')
