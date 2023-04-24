"""
test_pandas

"""


import pandas as pd
import numpy as np


# arr = np.arange(12).reshape(3,4)

# index = ["row1","row2","row3"]
# columns = ["col1","col2","col3","col4"]

# data = pd.DataFrame(arr,index = index,columns = columns)

# data.to_csv("./data.csv")

# with pd.ExcelWriter("data.xlsx") as writer:
#     data.to_excel(writer,sheet_name = "dist",index = True)



js_name = ["middle_up_nei_20230317151019933.json",
"middle_up_nei_20230116161353570.json",
"middle_up_nei_20230310162048108.json",
"middle_up_nei_20230316105732182.json",
"middle_up_nei_20230314111209341.json",
"middle_up_nei_20230112111819526.json",
"middle_up_nei_20230227091906284.json",
"middle_up_nei_20230203135324946.json",
"middle_up_nei_20230214091628647.json",
"middle_up_nei_20230112134422826.json",
"middle_up_nei_20230310103401144.json",
"middle_up_nei_20230315170451691.json",
"middle_up_nei_20230223185958655.json",
"middle_up_nei_20230309170542327.json",
"middle_up_nei_20230214090225627.json",
"middle_up_nei_20230120133430107.json",
"middle_up_nei_20230317170925227.json",
"middle_up_nei_20230317170404896.json",
"middle_up_nei_20230311191648572.json",
"middle_up_nei_20230313140113685.json",
"middle_up_nei_20230116134236054.json",
"middle_up_nei_20230222132609149.json",
"middle_up_nei_20230118110146379.json",
"middle_up_nei_20230322154048665.json",
"middle_up_nei_20230313162150923.json",
"middle_up_nei_20230201100806708.json",
"middle_up_nei_20230302094307941.json",
"middle_up_nei_20230112151106220.json",
"middle_up_nei_20230318112348286.json",
"middle_up_nei_20230310153651288.json",
"middle_up_nei_20230221192018457.json",
"middle_up_nei_20230113164014292.json",
"middle_up_nei_20230315102432690.json",
"middle_up_nei_20230116152732044.json",
"middle_up_nei_20230214100932687.json",
"middle_up_nei_20230323085036127.json",
"middle_up_nei_20230322154641145.json",
"middle_up_nei_20230316171648969.json",
"middle_up_nei_20230301120750281.json",
"middle_up_nei_20230114171800055.json",
"middle_up_nei_20230316172223179.json",
"middle_up_nei_20230309100254530.json",
"middle_up_nei_20230119150232963.json",
"middle_up_nei_20230322162148254.json",
"middle_up_nei_20230223150034844.json",
"middle_up_nei_20230118105449963.json",
"middle_up_nei_20230118120205319.json",
"middle_up_nei_20230320140555800.json",
"middle_up_nei_20230114170718009.json",
"middle_up_nei_20230308162103416.json",
"middle_up_nei_20230321161101892.json",
"middle_up_nei_20230316105741992.json",
"middle_up_nei_20230220100557161.json",
"middle_up_nei_20230112110449996.json",
"middle_up_nei_20230321132853462.json",
"middle_up_nei_20230310161443898.json",
"middle_up_nei_20230112140416116.json",
"middle_up_nei_20230220163749285.json",
"middle_up_nei_20230309164422817.json",
"middle_up_nei_20230223112422416.json",
"middle_up_nei_20230317205038213.json",
"middle_up_nei_20230321152127472.json",
"middle_up_nei_20230322115509935.json",
"middle_up_nei_20230316102740851.json",
"middle_up_nei_20230210140438968.json",
"middle_up_nei_20230302162300477.json",
"middle_up_nei_20230203140919140.json",
"middle_up_nei_20230113132841800.json",
"middle_up_nei_20230315101846861.json",
"middle_up_nei_20230316152356110.json",
"middle_up_nei_20230223192259416.json",
"middle_up_nei_20230228190926497.json",
"middle_up_nei_20230309100914770.json",
"middle_up_nei_20230314133709516.json",
"middle_up_nei_20230113143518903.json"]

import os
import shutil
src_dir = "/911G/data/cure_images/上位机第一次识别图像/局部识别/局部图预测draw整体图像"
dst_dir = "/911G/data/cure_images/上位机第一次识别图像/局部识别/pick_diff_max"
for file in js_name:
    src_json_file = os.path.join(src_dir,file)
    src_jpg_file = os.path.join(src_dir,file.replace("json", "jpg"))

    dst_json_file = os.path.join(dst_dir,file)
    dst_jpg_file = os.path.join(dst_dir,file.replace("json", "jpg"))

    shutil.copyfile(src_json_file,dst_json_file)
    shutil.copyfile(src_jpg_file,dst_jpg_file)