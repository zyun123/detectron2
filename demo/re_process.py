"""
识别后处理，检测识别错位
传入参数，[识别结果],[模型名称]
"""
import json
import numpy as np
import os
import glob
import math
from demo.keypoints_names import *
__all__ = ["main_process","split_kp"]
#置信度和距离阈值
CONFIDENCE_THRESHOLD = 50
DISTANCE_THRESHOLD = 50

#middle_up_nei_care
jl_pi = ['L-pi-1', 'L-pi-2', 'L-pi-3', 'L-pi-4',
                   'L-pi-5', 'L-pi-6', 'L-pi-7', 'L-pi-8','L-pi-9','L-pi-10','L-pi-11','L-pi-12', 
                   'R-pi-1', 'R-pi-2', 'R-pi-3', 'R-pi-4',
                   'R-pi-5', 'R-pi-6', 'R-pi-7', 'R-pi-8','R-pi-9','R-pi-10','R-pi-11','R-pi-12']
jl_xinbao = ['R-xinbao-1', 'R-xinbao-2', 'R-xinbao-3', 'R-xinbao-4', 'R-xinbao-5', 'R-xinbao-6',
              'R-xinbao-7', 'R-xinbao-8', 'R-xinbao-9',
              'L-xinbao-1', 'L-xinbao-2', 'L-xinbao-3', 'L-xinbao-4', 'L-xinbao-5', 'L-xinbao-6',
              'L-xinbao-7', 'L-xinbao-8', 'L-xinbao-9']
jl_wei = ['L-wei-15', 'L-wei-16', 'L-wei-17', 'L-wei-18', 'L-wei-19', 'L-wei-20', 'L-wei-21', 'L-wei-22', 'L-wei-23',
                 'L-wei-24', 'L-wei-25', 'L-wei-26', 'L-wei-27', 'L-wei-28', 'L-wei-29', 'L-wei-30', 
                 'R-wei-15', 'R-wei-16', 'R-wei-17', 'R-wei-18', 'R-wei-19', 'R-wei-20', 'R-wei-21', 'R-wei-22', 'R-wei-23',
                 'R-wei-24', 'R-wei-25', 'R-wei-26', 'R-wei-27', 'R-wei-28', 'R-wei-29', 'R-wei-30']
jl_middle_up_nei = jl_pi + jl_xinbao + jl_wei

#----------------middle_down_wai_care-----------------------
jl_sanjiao = ['L-sanjiao-1', 'L-sanjiao-2', 'L-sanjiao-3', 'L-sanjiao-4', 'L-sanjiao-5',
                  'L-sanjiao-6', 'L-sanjiao-7', 'L-sanjiao-8', 'L-sanjiao-9', 'R-sanjiao-1', 'R-sanjiao-2', 'R-sanjiao-3', 'R-sanjiao-4', 'R-sanjiao-5',
                  'R-sanjiao-6', 'R-sanjiao-7', 'R-sanjiao-8', 'R-sanjiao-9']
jl_pangguang = ['L-pangguang-9', 'L-pangguang-10', 'L-pangguang-11', 'L-pangguang-12', 'L-pangguang-13',
                    'L-pangguang-14', 'L-pangguang-15', 'L-pangguang-16', 'L-pangguang-17', 'L-pangguang-18',
                    'L-pangguang-19', 'L-pangguang-20', 'L-pangguang-21', 'L-pangguang-22', 'L-pangguang-23',
                    'L-pangguang-24', 'R-pangguang-9', 'R-pangguang-10',
                    'R-pangguang-11', 'R-pangguang-12', 'R-pangguang-13',
                    'R-pangguang-14', 'R-pangguang-15', 'R-pangguang-16', 'R-pangguang-17', 'R-pangguang-18',
                    'R-pangguang-19', 'R-pangguang-20', 'R-pangguang-21', 'R-pangguang-22', 'R-pangguang-23',
                    'R-pangguang-24']

jl_middle_down_wai =COCO_PERSON_KEYPOINT_NAMES_DOWN + COCO_PERSON_KEYPOINT_NAMES_HEAD_MIDDLE_DOWN


#模型对应的经络
model_jl_dict = {"middle_up_nei":jl_middle_up_nei,"middle_down_wai":jl_middle_down_wai}

m_up_nei_jlid = [(0,12),(12,24),(33,42),(24,33),(42,58),(58,74)] #左闭右开
m_up_nei_jlname = ['l_pi','r_pi','l_xinbao','r_xinbao','l_wei','r_wei']

# m_down_wai_jlid = [(0,9),(9,18),(18,34),(34,50)]
# m_down_wai_jlname = ['l_sanjiao','r_sanjiao','l_pangguang','r_pangguang']

middle_down_wai_name_ids = {"l_sanjiao":[(0,9)],
                "r_sanjiao":[(9,18)],
                "l_pangguang":[(18,34),(53,56)],
                "r_pangguang":[(34,50),(50,53)]}


split_kp_accname_id = {
                        "middle_up_nei":(m_up_nei_jlid,m_up_nei_jlname),
                        "middle_down_wai":middle_down_wai_name_ids
                    }
def get_kp(js_dict):
    """get keypoints from jl_dict
    Args:
        js_dict (dict): _description_
    Returns:
        _type_: _description_
    """
    kp_dict = dict()
    for shape in js_dict['shapes']:
        if shape['label'] != 'person':
            kp_dict[shape['label']] = shape['points']
    return kp_dict


def split_kp(keypoints,jl_name_ids,jl): 
    """分割关键点，左经络和右经络各一个list   
    Args:
        keypoints (list): 2d识别结果
        jl_name_ids (dict): 每条经络对应的id区间
        jl (list): (全局经络关键点列表) 
    Returns:
        dict: 每条经络对应一个列表   
    """
    l_kp_list = []
    l_kp = []
    r_kp_list = []
    r_kp = []
    
    # accu_kp =jl_id_name[1]
    # accu_id = jl_id_name[0]
    for accu_kp, accu_ids in jl_name_ids.items():
        temp_kp_names =[]
        temp_keypoints =[]
        for id_range in accu_ids:
            for i in range(id_range[0],id_range[1]):
                temp_kp_names.append(jl[i])
                temp_keypoints.append(keypoints[i])
        if accu_kp.split("_")[0] == "l":
            l_kp_list.extend(temp_kp_names)
            l_kp.extend(temp_keypoints)
        else: 
            r_kp_list.extend(temp_kp_names)
            r_kp.extend(temp_keypoints)
    assert len(l_kp) == len(r_kp) == len(l_kp_list) == len(r_kp_list),"左右经络的关键点列表长度需要一致"
    return l_kp, r_kp, l_kp_list, r_kp_list

            


    '''
    for i,jlname in enumerate(accu_kp):
        split_range = accu_id[i] #list
        # kp_list.extent([jl[id] for id in range(split_range[0],split_range[1]) if accu_kp[id].split("_")[0] == "l"])
        # l_kp.extend([keypoints[id] for id in range(split_range[0],split_range[1]) if accu_kp[id].split("_")[0] == "l"])
        # l_kp.extend([keypoints[id] for id in range(split_range[0],split_range[1]) if accu_kp[id].split("_")[0] == "r"])
        for id in range(split_range[0],split_range[1]):
            if accu_kp[i].split("_")[0] == "l":
                l_kp_list.append(jl[id])
                l_kp.append(keypoints[id])
            else:
                r_kp_list.append(jl[id])
                r_kp.append(keypoints[id])
    assert len(l_kp) == len(r_kp) == len(l_kp_list) == len(r_kp_list),"左右经络的关键点列表长度需要一致"

    return l_kp, r_kp, l_kp_list, r_kp_list
    '''
    
def process_confidence(keypoints):
    kp_arr = np.array(keypoints)
    conf_min = kp_arr[:,2].min()
    if conf_min < CONFIDENCE_THRESHOLD:
        return False
    return True

def main_reprocess(keypoints:list, model_name:str)->bool: 
    """后处理主程序

    Args:
        keypoints (list): 识别的直接结果[[x,y,confidence]]
        model_name (str): 
    """
    l_kp, r_kp, l_kp_list, r_kp_list = split_kp(keypoints,split_kp_accname_id[model_name],model_jl_dict[model_name])
    l_kp_arr = np.array(l_kp)
    r_kp_arr = np.array(r_kp)
    l_xy_arr = l_kp_arr[1:] - l_kp_arr[:-1]
    l_dis_arr = np.sqrt(l_xy_arr[:,0]**2 + l_xy_arr[:,1] ** 2)

    r_xy_arr = r_kp_arr[1:] - r_kp_arr[:-1]
    r_dis_arr = np.sqrt(r_xy_arr[:,0]**2 + r_xy_arr[:,1] ** 2)

    assert l_xy_arr.shape == r_xy_arr.shape,"shape需一致"

    dis_err = np.abs(l_dis_arr - r_dis_arr)
    # dis_err = l_dis_arr - r_dis_arr
    max_dis_err = dis_err.max()
    err_index = dis_err.argmax()

    if max_dis_err >DISTANCE_THRESHOLD:
        err_kp_name = l_kp_list[err_index][2:]
        print("err keypoit name:{},max_err_distance:{}".format(err_kp_name,max_dis_err))
        return False
    # if process_confidence(keypoints):
    #     return False

    return True


def test():
    middle_up_nei_kp = [[1070.3389830508474, 347.4576271186441],
                        [1051.4018691588785, 358.411214953271],
                        [986.8644067796611, 359.7457627118644],
                        [949.0654205607476, 363.0841121495327],
                        [891.9491525423729, 357.6271186440678],
                        [841.9491525423729, 360.5932203389831],
                        [780.9322033898305, 366.52542372881356],
                        [704.6728971962616, 357.0093457943925],
                        [629.646017699115, 353.9823008849557],
                        [488.0847457627119, 345.3389830508475],
                        [475.7966101694916, 332.6271186440678],
                        [437.66101694915255, 336.0169491525424],
                        [1078.3898305084747, 493.6440677966102],
                        [1051.271186440678, 478.3898305084746],
                        [988.5593220338984, 472.4576271186441],
                        [950.0, 463.135593220339],
                        [884.7457627118645, 458.4745762711865],
                        [840.677966101695, 452.11864406779665],
                        [783.0508474576271, 446.6101694915254],
                        [702.6548672566371, 446.4601769911504],
                        [631.858407079646, 450.88495575221236],
                        [493.14079422382673, 443.32129963898916],
                        [469.1588785046729, 455.607476635514],
                        [435.96610169491527, 451.271186440678],
                        [468.23104693140795, 454.87364620938627],
                        [442.0, 471.0],
                        [491.0, 473.0],
                        [532.0, 477.0],
                        [642.1052631578947, 501.31578947368416],
                        [667.5438596491227, 508.33333333333326],
                        [716.0, 506.0],
                        [682.0175438596491, 497.3684210526315],
                        [710.0, 498.0],
                        [475.81227436823104, 333.2129963898917],
                        [443.0, 317.0],
                        [488.0, 313.0],
                        [542.0, 307.0],
                        [634.6491228070174, 292.98245614035085],
                        [668.8596491228069, 287.2807017543859],
                        [710.9649122807017, 287.719298245614],
                        [684.0, 293.0],
                        [710.0, 298.0],
                        [415.0, 382.0],
                        [416.0, 370.0],
                        [475.45126353790613, 347.29241877256317],
                        [501.0, 371.0],
                        [581.0, 373.0],
                        [602.0, 373.0],
                        [629.646017699115, 353.9823008849557],
                        [667.0, 343.0],
                        [719.0, 342.0],
                        [788.0, 349.0],
                        [838.0, 342.0],
                        [875.0, 341.0],
                        [978.0, 353.0],
                        [1043.0, 342.0],
                        [977.0, 349.0],
                        [1040.0, 336.0],
                        [413.0, 404.0],
                        [412.0, 418.0],
                        [469.3140794223827, 440.072202166065],
                        [498.0, 426.0],
                        [581.0, 427.0],
                        [602.0, 428.0],
                        [630.9734513274335, 450.4424778761061],
                        [668.0, 459.0],
                        [719.0, 463.0],
                        [788.0, 463.0],
                        [836.0, 471.0],
                        [871.0, 477.0],
                        [981.0, 477.0],
                        [1049.809885931559, 496.958174904943],
                        [980.0, 481.0],
                        [1046.0, 503.0]]
    middle_down_wai_kp = [[672.0430107526881, 510.21505376344084],
                        [630.0, 506.0],
                        [603.0, 505.0],
                        [505.0, 480.0],
                        [378.0780780780781, 474.17417417417414],
                        [370.57057057057057, 449.54954954954957],
                        [356.0, 408.0],
                        [671.0, 300.0],
                        [637.0, 304.0],
                        [604.0, 304.0],
                        [507.0, 324.0],
                        [379.57957957957956, 324.3243243243243],
                        [369.96996996996995, 357.057057057057],
                        [357.0, 396.0],
                        [325.0, 409.0],
                        [356.0, 408.0],
                        [369.0690690690691, 416.5165165165165],
                        [618.359375, 418.359375],
                        [598.4375, 410.546875],
                        [627.34375, 411.328125],
                        [663.0, 432.0],
                        [791.0, 479.0],
                        [796.195652173913, 463.5869565217391],
                        [326.0, 408.0],
                        [348.0, 416.0],
                        [369.0690690690691, 446.54654654654655],
                        [559.0, 434.0],
                        [579.0, 442.0],
                        [659.0, 452.0],
                        [876.0, 488.0],
                        [325.0, 392.0],
                        [357.0, 396.0],
                        [367.86786786786786, 391.59159159159157],
                        [617.96875, 376.171875],
                        [598.828125, 384.765625],
                        [628.125, 382.03125],
                        [661.0, 363.0],
                        [790.0, 326.0],
                        [793.4782608695651, 341.30434782608694],
                        [325.0, 392.0],
                        [347.0, 390.0],
                        [370.57057057057057, 351.95195195195197],
                        [553.125, 364.84375],
                        [571.484375, 355.46875],
                        [658.0, 344.0],
                        [874.0, 324.0],
                        [347.0, 390.0],
                        [370.57057057057057, 351.95195195195197],
                        [553.125, 364.84375],
                        [571.484375, 355.46875],
                        [658.0, 344.0],
                        [874.0, 324.0],
                        [553.125, 364.84375],
                        [571.484375, 355.46875],
                        [658.0, 344.0],
                        [874.0, 324.0]
                        ]
    model_name = "middle_down_wai"
    status = main_reprocess(middle_down_wai_kp,model_name)
    print("bool:{}".format(status))


if __name__ == "__main__":
    test()
