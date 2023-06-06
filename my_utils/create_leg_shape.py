import os
import json
import glob


def get_dataDict(json_path):
    '''得到json'内容'''
    with open(json_path, 'r') as f:
        dataDict = json.load(f)
        return dataDict
def create_shapes(center,label):

    shapes = []
    shape = {}
    shape["label"] = label
    shape["points"] = [[center[0]-100,center[1]-100],[center[0]+100,center[1]+100]]
    shape["group_id"] = None
    shape["shape_type"] = "rectangle"
    shape["flags"] = {}
    shapes.append(shape)
    
    return shapes        



if __name__ == "__main__":

    root_dir=  "/911G/data/cure_images/一楼拷贝数据/up_nei/middle_up_nei"

    for js_path in glob.glob(os.path.join(root_dir, "*.json")):
        dataDict = get_dataDict(js_path)
        shapes = dataDict["shapes"]
        l_lt = [None,None]
        l_rb = [None,None]
        r_lt = [None,None]
        r_rb = [None,None]
        for shape in shapes:
            if shape['label'] == "L-wei-28":
                l_lt = shape['points'][0] 
            elif shape['label'] == "L-wei-27":
                l_rb = shape['points'][0]
            elif shape['label'] == "R-wei-28":
                r_lt = shape['points'][0]
            elif shape['label']  == "R-wei-27":
                r_rb = shape['points'][0]
        l_center = [(l_lt[0] + l_rb[0]) // 2, (l_lt[1] + l_rb[1]) // 2]
        r_center = [(r_lt[0] + r_rb[0]) // 2, (r_lt[1] + r_rb[1]) // 2]
        l_shapes = create_shapes(l_center,"left_leg")
        r_shapes = create_shapes(r_center,"right_leg")

        dataDict["shapes"].extend(l_shapes)
        dataDict["shapes"].extend(r_shapes)

        with open(js_path, "w") as f:
            json.dump(dataDict,f,indent=4)

        print(js_path,"---done--")
    

        




