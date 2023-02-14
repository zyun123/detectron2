"""
统计样本的anchor
"""
import json
import numpy as np
data_root = "/911G/data/temp/20221229新加手托脚托新数据/精确标注320套middle_down_wai_change_rec/train.json"
with open(data_root, 'r') as f:
    dataDict = json.load(f)

annotations = dataDict["annotations"]
re_wh = []
for ann in annotations:
    wh = ann["bbox"][2:]
    re_wh.append(wh)

re_wh = np.array(re_wh,dtype = np.int64)

clustor_anchor = np.mean(re_wh,axis = 0)
print(clustor_anchor)

base_anchor_size = np.int64(np.sqrt(clustor_anchor.prod(0)))
print(base_anchor_size)







