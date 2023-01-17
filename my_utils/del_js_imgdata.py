import json
import os
import numpy as np
import glob

root_dir = "/911G/data/temp/20221229新加手托脚托新数据/精确标注362套middle_up_nei_changerecopy"

for jsfile in glob.glob(os.path.join(root_dir,"*.json")):
    with open(jsfile,"r") as f:
        data_dict = json.load(f)
    data_dict["imageData"] = None

    with open(jsfile,"w") as f:
        json.dump(data_dict,f,indent=4)
