"""
将每个json数据里的imgae data清除掉
"""
import json
import os
import numpy as np
import glob



def del_image_data(root_dir):
    """
    刪除所有json文件里的imagedata
    """
    for jsfile in glob.glob(os.path.join(root_dir,"*.json")):
        with open(jsfile,"r") as f:
            data_dict = json.load(f)
        data_dict["imageData"] = None
        # data_dict['imageHeight'] = 720
        # data_dict['imageWidth'] = 1280
        print(data_dict["imagePath"])

        with open(jsfile,"w") as f:
            json.dump(data_dict,f,indent=4)

def del_shape_with_jl_names(root_dir,filter_names):
    """
    根据filter_names里的穴位点名，删除json文件里的对应的shape
    filter_names:需要删除的穴位点
    """
    n = 1
    for jsfile in glob.glob(os.path.join(root_dir,"*.json")):
        n+=1
        print(n)
        with open(jsfile,"r") as f:
            data_dict = json.load(f)
        
        # for i,shape in enumerate(data_dict['shapes']):
        for i in range(len(data_dict['shapes'])-1,-1,-1):
            if data_dict['shapes'][i]['label'] in filter_names:
                del data_dict['shapes'][i]


        with open(jsfile,"w") as f:
            json.dump(data_dict,f,indent=4)
    




if __name__ == "__main__":
    root_dir = "/911G/mergeData/0301经修改middle_down_wai/middle_down_wai"
    # del_image_data(root_dir) #删除图像数据
    filter_names = ['L-pi-1', 'L-pi-2', 'L-pi-3', 'L-pi-4', 'L-pi-5', 'L-pi-6', 'L-pi-7', 'L-pi-8', 'L-pi-9', 'L-pi-10', 'L-pi-11', 'L-pi-12', 'R-pi-1', 'R-pi-2', 'R-pi-3', 'R-pi-4', 'R-pi-5', 'R-pi-6', 'R-pi-7', 'R-pi-8', 'R-pi-9', 'R-pi-10', 'R-pi-11', 'R-pi-12', 'R-xinbao-6', 'R-xinbao-7', 'R-xinbao-8', 'R-xinbao-9', 'L-xinbao-6', 'L-xinbao-7', 'L-xinbao-8', 'L-xinbao-9', 'L-wei-28', 'L-wei-29', 'L-wei-30', 'R-wei-28', 'R-wei-29', 'R-wei-30','L-fei-1', 'L-fei-2', 'L-fei-3', 'L-fei-4', 'L-fei-5', 'L-fei-6', 'L-fei-7', 'L-fei-8','R-fei-1', 'R-fei-2', 'R-fei-3', 'R-fei-4', 'R-fei-5', 'R-fei-6','R-fei-7', 'R-fei-8'] 
    # del_shape_with_jl_names(root_dir,filter_names = filter_names)
    del_image_data(root_dir)