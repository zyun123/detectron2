"""
将每个json数据里的imgae data清除掉
"""
import json
import os
import numpy as np
import glob

root_dir = "/911G/mergeData/middle_down_wai（736套）更新/middle_down_wai"

for jsfile in glob.glob(os.path.join(root_dir,"*.json")):
    with open(jsfile,"r") as f:
        data_dict = json.load(f)
    data_dict["imageData"] = None

    with open(jsfile,"w") as f:
        json.dump(data_dict,f,indent=4)
