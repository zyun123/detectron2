


__all__ = ["MIDDLE_UP_ALL_JL","MIDDLE_DOWN_ALL_JL",
            "MIDDLE_DOWN_CARE","MIDDLE_UP_WITH_FEI","MIDDLE_UP_WITHOUT_FEI",
            "LEFT_DOWN","HEAD_MIDDLE_DOWN","DOWN_NEI",
            "PARTIAL_LEG_UP","PARTIAL_LEFT_HAND_UP","PARTIAL_RIGHT_HAND_UP",
            "RULES_WHOLE_DOWN","RULES_UP",
            "RULES_LEFT_DOWN",
            "UP_LEFT_HAND","UP_RIGHT_HAND","UP_LEFT_FOOT","UP_RIGHT_FOOT","DOWN_LEFT_HAND","DOWN_RIGHT_HAND",
            "ALLJL_DOWN_RIGHT_FOOT","ALLJL_UP_LEFT_HAND","ALLJL_UP_RIGHT_HAND","ALLJL_DOWN_RIGHT_HAND","ALLJL_DOWN_LEFT_HAND",
            "ALLJL_DOWN_RIGHT_HEAD","ALLJL_UP_LEFT_FOOT","ALLJL_UP_FACE","ALLJL_TOP_HEAD"]

#  26个点 middle_down_nei
DOWN_NEI = ['R-shen-1', 'R-shen-2', 'R-shen-3', 'R-shen-4', 'R-shen-5',
                           'R-shen-6', 'R-shen-7', 'R-shen-8', 'R-shen-9', 'R-shen-10', 'R-shen-11', 'R-shen-12','R-shen-13',
                           'L-shen-1', 'L-shen-2', 'L-shen-3', 'L-shen-4', 'L-shen-5',
                           'L-shen-6', 'L-shen-7', 'L-shen-8', 'L-shen-9', 'L-shen-10', 'L-shen-11', 'L-shen-12', 'L-shen-13'] 


#全经络版本84个点            
MIDDLE_UP_ALL_JL = ['R-shen-14', 'R-shen-15', 'R-shen-16', 'R-shen-17', 'R-shen-18', 'R-shen-19',
                         'L-shen-14', 'L-shen-15', 'L-shen-16', 'L-shen-17', 'L-shen-18', 'L-shen-19','R-xinbao-1', 
                         'R-xinbao-2', 'R-xinbao-3', 'R-xinbao-4', 'R-xinbao-5', 'R-xinbao-6','R-xinbao-7', 
                         'R-xinbao-8', 'R-xinbao-9','L-xinbao-1', 'L-xinbao-2', 'L-xinbao-3', 'L-xinbao-4', 
                         'L-xinbao-5', 'L-xinbao-6','L-xinbao-7', 'L-xinbao-8', 'L-xinbao-9','L-fei-1', 'L-fei-2', 
                         'L-fei-3', 'L-fei-4', 'L-fei-5', 'L-fei-6', 'L-fei-7', 'L-fei-8','R-fei-1', 'R-fei-2',
                         'R-fei-3', 'R-fei-4', 'R-fei-5', 'R-fei-6', 'R-fei-7', 'R-fei-8','L-wei-15', 'L-wei-16', 
                         'L-wei-17', 'L-wei-18', 'L-wei-19', 'L-wei-20', 'L-wei-21', 'L-wei-22', 'L-wei-23',
                            'L-wei-24', 'L-wei-25', 'L-wei-26', 'L-wei-27', 'L-wei-28', 'L-wei-29', 'L-wei-30', 
                            'R-wei-15', 'R-wei-16', 'R-wei-17', 'R-wei-18', 'R-wei-19', 'R-wei-20', 'R-wei-21', 
                            'R-wei-22', 'R-wei-23','R-wei-24', 'R-wei-25', 'R-wei-26', 'R-wei-27', 'R-wei-28', 
                            'R-wei-29', 'R-wei-30','L-dan-26','L-dan-51','L-dan-52','R-dan-26','R-dan-51','R-dan-52']


#全经络版本  90个点   middle_down_wai                     
MIDDLE_DOWN_ALL_JL = ['R-dachang-1','R-dachang-2', 'R-dachang-3','R-dachang-4','R-dachang-5',
    'R-dachang-6','R-dachang-20','R-dachang-7','R-dachang-8',
    'L-dachang-1','L-dachang-2','L-dachang-3','L-dachang-4','L-dachang-5','L-dachang-6','L-dachang-20',
    'L-dachang-7','L-dachang-8','L-sanjiao-1','L-sanjiao-2', 'L-sanjiao-3','L-sanjiao-4','L-sanjiao-5',
    'L-sanjiao-6','L-sanjiao-7','R-sanjiao-1','R-sanjiao-2', 'R-sanjiao-3','R-sanjiao-4','R-sanjiao-5',
    'R-sanjiao-6','R-sanjiao-7','L-xiaochang-1', 'L-xiaochang-2','L-xiaochang-3','L-xiaochang-4','L-xiaochang-20','L-xiaochang-5',
    'L-xiaochang-6','L-xiaochang-7','L-xiaochang-8','L-xiaochang-9','L-xiaochang-10',
    'L-xiaochang-11', 'L-xiaochang-12',
    'R-xiaochang-1', 'R-xiaochang-2','R-xiaochang-3','R-xiaochang-4','R-xiaochang-20','R-xiaochang-5',
    'R-xiaochang-6','R-xiaochang-7','R-xiaochang-8','R-xiaochang-9','R-xiaochang-10',
    'R-xiaochang-11', 'R-xiaochang-12','L-pangguang-9','L-pangguang-10', 'L-pangguang-11','L-pangguang-12','L-pangguang-13',
    'L-pangguang-14','L-pangguang-15', 'L-pangguang-16','L-pangguang-17','L-pangguang-18',
    'L-pangguang-19','L-pangguang-20', 'L-pangguang-21','L-pangguang-22','L-pangguang-23',
    'L-pangguang-24','R-pangguang-9','R-pangguang-10', 
    'R-pangguang-11','R-pangguang-12','R-pangguang-13',
    'R-pangguang-14','R-pangguang-15', 'R-pangguang-16','R-pangguang-17','R-pangguang-18',
    'R-pangguang-19','R-pangguang-20', 'R-pangguang-21','R-pangguang-22','R-pangguang-23',
    'R-pangguang-24']    

#调理版本                    
MIDDLE_DOWN_CARE = ['L-sanjiao-1', 'L-sanjiao-2', 'L-sanjiao-3', 'L-sanjiao-4', 'L-sanjiao-5',
                'L-sanjiao-6', 'L-sanjiao-7', 'L-sanjiao-8', 'L-sanjiao-9', 'R-sanjiao-1', 'R-sanjiao-2',
                 'R-sanjiao-3', 'R-sanjiao-4', 'R-sanjiao-5','R-sanjiao-6', 'R-sanjiao-7', 'R-sanjiao-8', 'R-sanjiao-9',
                'L-pangguang-9', 'L-pangguang-10', 'L-pangguang-11', 'L-pangguang-12', 'L-pangguang-13',
                'L-pangguang-14', 'L-pangguang-15', 'L-pangguang-16', 'L-pangguang-17', 'L-pangguang-18',
                'L-pangguang-19', 'L-pangguang-20', 'L-pangguang-21', 'L-pangguang-22', 'L-pangguang-23',
                'L-pangguang-24', 'R-pangguang-9', 'R-pangguang-10',
                'R-pangguang-11', 'R-pangguang-12', 'R-pangguang-13',
                'R-pangguang-14', 'R-pangguang-15', 'R-pangguang-16', 'R-pangguang-17', 'R-pangguang-18',
                'R-pangguang-19', 'R-pangguang-20', 'R-pangguang-21', 'R-pangguang-22', 'R-pangguang-23',
                'R-pangguang-24']


# #加肺经
MIDDLE_UP_WITH_FEI = ['L-pi-1', 'L-pi-2', 'L-pi-3', 'L-pi-4', 'L-pi-5', 'L-pi-6', 'L-pi-7', 'L-pi-8', 'L-pi-9', 
'L-pi-10', 'L-pi-11', 'L-pi-12', 'R-pi-1', 'R-pi-2', 'R-pi-3', 'R-pi-4', 'R-pi-5', 'R-pi-6', 'R-pi-7', 'R-pi-8', 'R-pi-9', 
'R-pi-10', 'R-pi-11', 'R-pi-12', 'R-xinbao-1', 'R-xinbao-2', 'R-xinbao-3', 'R-xinbao-4', 'R-xinbao-5', 'R-xinbao-6', 
'R-xinbao-7', 'R-xinbao-8', 'R-xinbao-9', 'L-xinbao-1', 'L-xinbao-2', 'L-xinbao-3', 'L-xinbao-4', 'L-xinbao-5', 
'L-xinbao-6', 'L-xinbao-7', 'L-xinbao-8', 'L-xinbao-9', 'L-wei-15', 'L-wei-16', 'L-wei-17', 'L-wei-18', 'L-wei-19', 
'L-wei-20', 'L-wei-21', 'L-wei-22', 'L-wei-23', 'L-wei-24', 'L-wei-25', 'L-wei-26', 'L-wei-27', 'L-wei-28', 'L-wei-29', 
'L-wei-30', 'R-wei-15', 'R-wei-16', 'R-wei-17', 'R-wei-18', 'R-wei-19', 'R-wei-20', 'R-wei-21', 'R-wei-22', 'R-wei-23', 
'R-wei-24', 'R-wei-25', 'R-wei-26', 'R-wei-27', 'R-wei-28', 'R-wei-29', 'R-wei-30','L-fei-1', 'L-fei-2', 'L-fei-3', 
'L-fei-4', 'L-fei-5', 'L-fei-6', 'L-fei-7', 'L-fei-8','R-fei-1', 'R-fei-2', 'R-fei-3', 'R-fei-4', 'R-fei-5', 'R-fei-6', 
'R-fei-7', 'R-fei-8']

#不加肺经
MIDDLE_UP_WITHOUT_FEI = ['L-pi-1', 'L-pi-2', 'L-pi-3', 'L-pi-4', 'L-pi-5', 'L-pi-6', 'L-pi-7', 'L-pi-8', 'L-pi-9', 'L-pi-10', 'L-pi-11', 'L-pi-12', 'R-pi-1', 'R-pi-2', 'R-pi-3', 'R-pi-4', 'R-pi-5', 'R-pi-6', 'R-pi-7', 'R-pi-8', 'R-pi-9', 'R-pi-10', 'R-pi-11', 'R-pi-12', 'R-xinbao-1', 'R-xinbao-2', 'R-xinbao-3', 'R-xinbao-4', 'R-xinbao-5', 'R-xinbao-6', 'R-xinbao-7', 'R-xinbao-8', 'R-xinbao-9', 'L-xinbao-1', 'L-xinbao-2', 'L-xinbao-3', 'L-xinbao-4', 'L-xinbao-5', 'L-xinbao-6', 'L-xinbao-7', 'L-xinbao-8', 'L-xinbao-9', 'L-wei-15', 'L-wei-16', 'L-wei-17', 'L-wei-18', 'L-wei-19', 'L-wei-20', 'L-wei-21', 'L-wei-22', 'L-wei-23', 'L-wei-24', 'L-wei-25', 'L-wei-26', 'L-wei-27', 'L-wei-28', 'L-wei-29', 'L-wei-30', 'R-wei-15', 'R-wei-16', 'R-wei-17', 'R-wei-18', 'R-wei-19', 'R-wei-20', 'R-wei-21', 'R-wei-22', 'R-wei-23', 'R-wei-24', 'R-wei-25', 'R-wei-26', 'R-wei-27', 'R-wei-28', 'R-wei-29', 'R-wei-30']


#局部脚
PARTIAL_LEG_UP = ['L-pi-1', 'L-pi-2', 'L-pi-3', 'L-pi-4','L-pi-5', 'L-pi-6', 'L-pi-7',
                            'R-pi-1', 'R-pi-2', 'R-pi-3', 'R-pi-4','R-pi-5', 'R-pi-6', 'R-pi-7',
                            'L-wei-24', 'L-wei-25', 'L-wei-26', 'L-wei-27', 'L-wei-28', 'L-wei-29', 'L-wei-30',
                            'R-wei-24', 'R-wei-25', 'R-wei-26', 'R-wei-27', 'R-wei-28', 'R-wei-29', 'R-wei-30']
#局部左手
PARTIAL_LEFT_HAND_UP = ["L-xinbao-5","L-xinbao-6","L-xinbao-7","L-xinbao-8","L-xinbao-9","L-fei-6","L-fei-7","L-fei-8"]
#局部右手
PARTIAL_RIGHT_HAND_UP = ["R-xinbao-5","R-xinbao-6","R-xinbao-7","R-xinbao-8","R-xinbao-9","R-fei-6","R-fei-7","R-fei-8"]

#局部图局部手
UP_LEFT_HAND = ["L-xinbao-5","L-xinbao-6","L-xinbao-7","L-xinbao-8","L-xinbao-9"]
UP_RIGHT_HAND = ["R-xinbao-5","R-xinbao-6","R-xinbao-7","R-xinbao-8","R-xinbao-9"]
UP_LEFT_FOOT = ["L-wei-27", "L-wei-28", "L-wei-29", "L-wei-30","L-pi-1","L-pi-2","L-pi-3"]
UP_RIGHT_FOOT = ["R-wei-27", "R-wei-28", "R-wei-29", "R-wei-30","R-pi-1","R-pi-2","R-pi-3"]
DOWN_LEFT_HAND = ["L-sanjiao-1","L-sanjiao-2","L-sanjiao-3"]
DOWN_RIGHT_HAND = ["R-sanjiao-1","R-sanjiao-2","R-sanjiao-3"]


#新全经络局部手脚

#侧面 脚 right_foot_left_down_wai
ALLJL_DOWN_RIGHT_FOOT = ["L-shen-1","L-shen-2","L-shen-7","L-shen-8","R-pangguang-25","R-pangguang-26"]

#left_hand_middle_up_nei
ALLJL_UP_LEFT_HAND = ["L-xinbao-5","L-xinbao-6", "L-xinbao-7", "L-xinbao-8", "L-xinbao-9","L-fei-6","L-fei-7","L-fei-8","L-xin-4","L-xin-5","L-xin-6"]
#right_hand_middle_up_nei
ALLJL_UP_RIGHT_HAND = ["R-xinbao-5","R-xinbao-6", "R-xinbao-7", "R-xinbao-8", "R-xinbao-9","R-fei-6","R-fei-7","R-fei-8","R-xin-4","R-xin-5","R-xin-6"]

#left_hand_middle_down_wai
ALLJL_DOWN_LEFT_HAND = ["L-dachang-1", "L-dachang-2", "L-dachang-3", "L-dachang-4", "L-xiaochang-1","L-xiaochang-2", "L-xiaochang-3", "L-sanjiao-1", "L-sanjiao-2", "L-sanjiao-3"]
#right_hand_middle_down_wai
ALLJL_DOWN_RIGHT_HAND = ["R-dachang-1", "R-dachang-2", "R-dachang-3", "R-dachang-4", "R-xiaochang-1","R-xiaochang-2", "R-xiaochang-3", "R-sanjiao-1", "R-sanjiao-2", "R-sanjiao-3"]


#头部 right_head_left_down_wai
ALLJL_DOWN_RIGHT_HEAD = ['R-sanjiao-8', 'R-sanjiao-9', 'R-sanjiao-10', 'R-sanjiao-11', 'R-sanjiao-12', 'R-sanjiao-13', 'R-sanjiao-14', 'R-sanjiao-15', 'R-sanjiao-16', 'R-sanjiao-17', 'R-sanjiao-18', 'R-sanjiao-19', 'R-sanjiao-20', 'R-sanjiao-21', 'R-sanjiao-22', 'R-sanjiao-23', 'R-sanjiao-24','R-dan-1', 'R-dan-2', 'R-dan-3', 'R-dan-4', 'R-dan-5', 'R-dan-6', 'R-dan-7', 'R-dan-8', 'R-dan-9', 'R-dan-10', 'R-dan-11', 'R-dan-12', 'R-dan-13', 'R-dan-14', 'R-dan-15', 'R-dan-16', 'R-dan-17', 'R-dan-18']

#up  侧面 脚  left_foot_left_up_nei
ALLJL_UP_LEFT_FOOT = ['L-dan-40','L-dan-41','L-gan-1','L-gan-2']

ALLJL_UP_FACE = ['L-wei-1','L-wei-2','L-wei-3','L-wei-4','L-wei-5','L-wei-6','L-wei-7','L-wei-8','L-wei-9','L-wei-10','L-wei-11',
                             'R-wei-1','R-wei-2','R-wei-3','R-wei-4','R-wei-5','R-wei-6','R-wei-7','R-wei-8','R-wei-9','R-wei-10','R-wei-11',
                             'L-gan-20','L-gan-21','L-gan-22','L-gan-23','L-gan-24','L-gan-25','L-gan-26',
                             'R-gan-20','R-gan-21','R-gan-22','R-gan-23','R-gan-24','R-gan-25','R-gan-26',
                             'du-8','du-9','du-10','du-11','ren-1','ren-2']

#头部相机  头顶天灵盖穴位
ALLJL_TOP_HEAD = ['L-pangguang-4','L-pangguang-5','L-pangguang-6','L-pangguang-40','R-pangguang-4','R-pangguang-5','R-pangguang-6','R-pangguang-40',
                'du-20','du-21','du-22']




res = ALLJL_DOWN_RIGHT_FOOT+ALLJL_UP_LEFT_HAND+ALLJL_UP_RIGHT_HAND+ALLJL_DOWN_LEFT_HAND+ALLJL_DOWN_RIGHT_HAND+ \
        ALLJL_DOWN_RIGHT_HEAD+ALLJL_UP_LEFT_FOOT+ALLJL_UP_FACE+ALLJL_TOP_HEAD




RULES_UP = [
        # xinbao
        ('R-xinbao-1', 'R-xinbao-2', (10, 204, 255)),
        ('R-xinbao-2', 'R-xinbao-3', (20, 204, 255)),
        ('R-xinbao-3', 'R-xinbao-4', (30, 204, 255)),
        ('R-xinbao-4', 'R-xinbao-5', (40, 204, 255)),
        ('R-xinbao-5', 'R-xinbao-6', (50, 204, 255)),
        ('R-xinbao-6', 'R-xinbao-7', (60, 204, 255)),
        ('R-xinbao-7', 'R-xinbao-8', (70, 204, 255)),
        ('R-xinbao-8', 'R-xinbao-9', (80, 204, 255)),

        ('L-xinbao-1', 'L-xinbao-2', (10, 204, 255)),
        ('L-xinbao-2', 'L-xinbao-3', (20, 204, 255)),
        ('L-xinbao-3', 'L-xinbao-4', (30, 204, 255)),
        ('L-xinbao-4', 'L-xinbao-5', (40, 204, 255)),
        ('L-xinbao-5', 'L-xinbao-6', (50, 204, 255)),
        ('L-xinbao-6', 'L-xinbao-7', (60, 204, 255)),
        ('L-xinbao-7', 'L-xinbao-8', (70, 204, 255)),
        ('L-xinbao-8', 'L-xinbao-9', (80, 204, 255)),

        #wei
        ('L-wei-1','L-wei-2',(255, 128, 0)),
        ('L-wei-2','L-wei-3',(255, 128, 0)),
        ('L-wei-3','L-wei-4',(255, 128, 0)),
        ('L-wei-4','L-wei-5',(255, 128, 0)),
        ('L-wei-5','L-wei-6',(255, 128, 0)),
        ('L-wei-6','L-wei-7',(255, 128, 0)),
        ('L-wei-7','L-wei-8',(255, 128, 0)),
        ('L-wei-8','L-wei-9',(255, 128, 0)),
        ('L-wei-9','L-wei-10',(255, 128, 0)),
        ('L-wei-10','L-wei-11',(255, 128, 0)),
        ('L-wei-15', 'L-wei-16', (255, 128, 0)),
        ('L-wei-16', 'L-wei-17', (255, 128, 0)),
        ('L-wei-17', 'L-wei-18', (255, 128, 0)),
        ('L-wei-18', 'L-wei-19', (255, 128, 0)),
        ('L-wei-19', 'L-wei-20', (255, 128, 0)),
        ('L-wei-20', 'L-wei-21', (255, 128, 0)),
        ('L-wei-21', 'L-wei-22', (255, 128, 0)),
        ('L-wei-22', 'L-wei-23', (255, 128, 0)),
        ('L-wei-23', 'L-wei-24', (255, 128, 0)),
        ('L-wei-24', 'L-wei-25', (255, 128, 0)),
        ('L-wei-25', 'L-wei-26', (255, 128, 0)),
        ('L-wei-26', 'L-wei-27', (255, 128, 0)),
        ('L-wei-27', 'L-wei-28', (255, 128, 0)),
        ('L-wei-28', 'L-wei-29', (255, 128, 0)),
        ('L-wei-29', 'L-wei-30', (255, 128, 0)),

        ('R-wei-1','R-wei-2',(255, 128, 0)),
        ('R-wei-2','R-wei-3',(255, 128, 0)),
        ('R-wei-3','R-wei-4',(255, 128, 0)),
        ('R-wei-4','R-wei-5',(255, 128, 0)),
        ('R-wei-5','R-wei-6',(255, 128, 0)),
        ('R-wei-6','R-wei-7',(255, 128, 0)),
        ('R-wei-7','R-wei-8',(255, 128, 0)),
        ('R-wei-8','R-wei-9',(255, 128, 0)),
        ('R-wei-9','R-wei-10',(255, 128, 0)),
        ('R-wei-10','R-wei-11',(255, 128, 0)),
        ('R-wei-15', 'R-wei-16', (255, 128, 0)),
        ('R-wei-16', 'R-wei-17', (255, 128, 0)),
        ('R-wei-17', 'R-wei-18', (255, 128, 0)),
        ('R-wei-18', 'R-wei-19', (255, 128, 0)),
        ('R-wei-19', 'R-wei-20', (255, 128, 0)),
        ('R-wei-20', 'R-wei-21', (255, 128, 0)),
        ('R-wei-21', 'R-wei-22', (255, 128, 0)),
        ('R-wei-22', 'R-wei-23', (255, 128, 0)),
        ('R-wei-23', 'R-wei-24', (255, 128, 0)),
        ('R-wei-24', 'R-wei-25', (255, 128, 0)),
        ('R-wei-25', 'R-wei-26', (255, 128, 0)),
        ('R-wei-26', 'R-wei-27', (255, 128, 0)),
        ('R-wei-27', 'R-wei-28', (255, 128, 0)),
        ('R-wei-28', 'R-wei-29', (255, 128, 0)),
        ('R-wei-29', 'R-wei-30', (255, 128, 0)),

        #pi
        ('L-pi-1', 'L-pi-2', (10,255,10)),
        ('L-pi-2', 'L-pi-3', (10,255,10)),
        ('L-pi-3', 'L-pi-4', (10,255,10)),
        ('L-pi-4', 'L-pi-5', (10,255,10)),
        ('L-pi-5', 'L-pi-6', (10,255,10)),
        ('L-pi-6', 'L-pi-7', (10,255,10)),
        ('L-pi-7', 'L-pi-8', (10,255,10)),
        ('L-pi-8', 'L-pi-9', (10,255,10)),
        ('L-pi-9', 'L-pi-10', (10,255,10)),
        ('L-pi-10', 'L-pi-11', (10,255,10)),
        ('L-pi-11', 'L-pi-12', (10,255,10)),

        ('R-pi-1', 'R-pi-2', (10,255,10)),
        ('R-pi-2', 'R-pi-3', (10,255,10)),
        ('R-pi-3', 'R-pi-4', (10,255,10)),
        ('R-pi-4', 'R-pi-5', (10,255,10)),
        ('R-pi-5', 'R-pi-6', (10,255,10)),
        ('R-pi-6', 'R-pi-7', (10,255,10)),
        ('R-pi-7', 'R-pi-8', (10,255,10)),
        ('R-pi-8', 'R-pi-9', (10,255,10)),
        ('R-pi-9', 'R-pi-10', (10,255,10)),
        ('R-pi-10', 'R-pi-11', (10,255,10)),
        ('R-pi-11', 'R-pi-12', (10,255,10)),
        
        #feijing
        ('L-fei-1', 'L-fei-2', (10,255,100)),
        ('L-fei-2', 'L-fei-3', (10,255,100)),
        ('L-fei-3', 'L-fei-4', (10,255,100)),
        ('L-fei-4', 'L-fei-5', (10,255,100)),
        ('L-fei-5', 'L-fei-6', (10,255,100)),
        ('L-fei-6', 'L-fei-7', (10,255,100)),
        ('L-fei-7', 'L-fei-8', (10,255,100)),

        ('R-fei-1', 'R-fei-2', (10,255,100)),
        ('R-fei-2', 'R-fei-3', (10,255,100)),
        ('R-fei-3', 'R-fei-4', (10,255,100)),
        ('R-fei-4', 'R-fei-5', (10,255,100)),
        ('R-fei-5', 'R-fei-6', (10,255,100)),
        ('R-fei-6', 'R-fei-7', (10,255,100)),
        ('R-fei-7', 'R-fei-8', (10,255,100)),

        ('R-xin-1', 'R-xin-2', (10,255,100)),
        ('R-xin-2', 'R-xin-3', (10,255,100)),
        ('R-xin-3', 'R-xin-4', (10,255,100)),
        ('R-xin-4', 'R-xin-5', (10,255,100)),
        ('R-xin-5', 'R-xin-6', (10,255,100)),
        ('R-xin-6', 'R-xin-7', (10,255,100)),
        ('R-xin-7', 'R-xin-8', (10,255,100)),

        ('L-xin-1', 'L-xin-2', (10,255,100)),
        ('L-xin-2', 'L-xin-3', (10,255,100)),
        ('L-xin-3', 'L-xin-4', (10,255,100)),
        ('L-xin-4', 'L-xin-5', (10,255,100)),
        ('L-xin-5', 'L-xin-6', (10,255,100)),
        ('L-xin-6', 'L-xin-7', (10,255,100)),
        ('L-xin-7', 'L-xin-8', (10,255,100)),

        ('L-gan-20','L-gan-21',(10,255,100)),
        ('L-gan-21','L-gan-22',(10,255,100)),
        ('L-gan-22','L-gan-23',(10,255,100)),
        ('L-gan-23','L-gan-24',(10,255,100)),
        ('L-gan-24','L-gan-25',(10,255,100)),
        ('L-gan-25','L-gan-26',(10,255,100)),


        ('R-gan-20','R-gan-21',(10,255,100)),
        ('R-gan-21','R-gan-22',(10,255,100)),
        ('R-gan-22','R-gan-23',(10,255,100)),
        ('R-gan-23','R-gan-24',(10,255,100)),
        ('R-gan-24','R-gan-25',(10,255,100)),
        ('R-gan-25','R-gan-26',(10,255,100)),



        ('du-8','du-9',(10,10,100)),
        ('du-9','du-10',(10,10,100)),
        ('du-10','du-11',(10,10,100)),
        ('ren-1','ren-2',(10,10,100)), 
    ]

LEFT_DOWN = ['R-sanjiao-8','R-sanjiao-9','R-sanjiao-10','R-sanjiao-11','R-sanjiao-12','R-sanjiao-13','R-sanjiao-14','R-sanjiao-15','R-sanjiao-16',
                    'R-sanjiao-17','R-sanjiao-18','R-sanjiao-19','R-sanjiao-20','R-sanjiao-21','R-sanjiao-22','R-sanjiao-23','R-sanjiao-24',
                    'R-dan-1','R-dan-2','R-dan-3','R-dan-4','R-dan-5','R-dan-6','R-dan-7','R-dan-8','R-dan-9','R-dan-10','R-dan-11','R-dan-12',
                    'R-dan-13','R-dan-14','R-dan-15','R-dan-16','R-dan-17','R-dan-18']
RULES_LEFT_DOWN = [
        # sanjiao
        ('R-sanjiao-8', 'R-sanjiao-9', (255, 0 , 255)),
        ('R-sanjiao-9', 'R-sanjiao-10', (255, 0 , 255)),
        ('R-sanjiao-10', 'R-sanjiao-11', (255, 0 , 255)),
        ('R-sanjiao-11', 'R-sanjiao-12', (255, 0 , 255)),
        ('R-sanjiao-12', 'R-sanjiao-13', (255, 0 , 255)),
        ('R-sanjiao-13', 'R-sanjiao-14', (255, 0 , 255)),
        ('R-sanjiao-14', 'R-sanjiao-15', (255, 0 , 255)),
        ('R-sanjiao-15', 'R-sanjiao-16', (255, 0 , 255)),
        ('R-sanjiao-16', 'R-sanjiao-17', (255, 0 , 255)),
        ('R-sanjiao-17', 'R-sanjiao-18', (255, 0 , 255)),
        ('R-sanjiao-18', 'R-sanjiao-19', (255, 0 , 255)),
        ('R-sanjiao-19', 'R-sanjiao-20', (255, 0 , 255)),
        ('R-sanjiao-20', 'R-sanjiao-21', (255, 0 , 255)),
        ('R-sanjiao-21', 'R-sanjiao-22', (255, 0 , 255)),
        ('R-sanjiao-22', 'R-sanjiao-23', (255, 0 , 255)),
        ('R-sanjiao-23', 'R-sanjiao-24', (255, 0 , 255)),

        ('R-dan-1', 'R-dan-2', (0, 255 , 255)),
        ('R-dan-2', 'R-dan-3', (0, 255 , 255)),
        ('R-dan-3', 'R-dan-4', (0, 255 , 255)),
        ('R-dan-4', 'R-dan-5', (0, 255 , 255)),
        ('R-dan-5', 'R-dan-6', (0, 255 , 255)),
        ('R-dan-6', 'R-dan-7', (0, 255 , 255)),
        ('R-dan-7', 'R-dan-8', (0, 255 , 255)),
        ('R-dan-8', 'R-dan-9', (0, 255 , 255)),
        ('R-dan-9', 'R-dan-10', (0 ,255, 255)),
        ('R-dan-10', 'R-dan-11', (0 ,255, 255)),
        ('R-dan-11', 'R-dan-12', (0 ,255, 255)),
        ('R-dan-12', 'R-dan-13', (0 ,255, 255)),
        ('R-dan-13', 'R-dan-14', (0 ,255, 255)),
        ('R-dan-14', 'R-dan-15', (0 ,255, 255)),
        ('R-dan-15', 'R-dan-16', (0 ,255, 255)),
        ('R-dan-16', 'R-dan-17', (0 ,255, 255)),
        ('R-dan-17', 'R-dan-18', (0 ,255, 255)),

]


HEAD_MIDDLE_DOWN = ["R-pangguang-7","R-pangguang-30","R-pangguang-8",
                                                "L-pangguang-7","L-pangguang-30","L-pangguang-8",]

# RULES_HEAD_MIDDLE_DOWN = [
#     ('R-pangguang-7', 'R-pangguang-30', (255, 0 , 255)),
#     ('R-pangguang-30', 'R-pangguang-8', (255, 0 , 255)),
#     ('L-pangguang-7', 'L-pangguang-30', (0 ,255, 255)),
#     ('L-pangguang-30', 'L-pangguang-8', (0 ,255, 255)),
# ]

RULES_WHOLE_DOWN = [
        #大肠经 景泰蓝
        ('R-dachang-1', 'R-dachang-2', (39,117,182)),
        ('R-dachang-2', 'R-dachang-3', (39,117,182)),
        ('R-dachang-3', 'R-dachang-4', (39,117,182)),
        ('R-dachang-4', 'R-dachang-5', (39,117,182)),
        ('R-dachang-5', 'R-dachang-20', (39,117,182)),
        ('R-dachang-20', 'R-dachang-6', (39,117,182)),
        ('R-dachang-6', 'R-dachang-7', (39,117,182)),
        ('R-dachang-7', 'R-dachang-8', (39,117,182)),
        ('L-dachang-1', 'L-dachang-2', (39,117,182)),
        ('L-dachang-2', 'L-dachang-3', (39,117,182)),
        ('L-dachang-3', 'L-dachang-4', (39,117,182)),
        ('L-dachang-4', 'L-dachang-5', (39,117,182)),
        ('L-dachang-5', 'L-dachang-20', (39,117,182)),
        ('L-dachang-20', 'L-dachang-6', (39,117,182)),
        ('L-dachang-6', 'L-dachang-7', (39,117,182)),
        ('L-dachang-7', 'L-dachang-8', (39,117,182)),

        #小肠  油菜花黄
        ('L-xiaochang-1', 'L-xiaochang-2', (251,218,65)),
        ('L-xiaochang-2', 'L-xiaochang-3', (251,218,65)),
        ('L-xiaochang-3', 'L-xiaochang-4', (251,218,65)),
        ('L-xiaochang-4', 'L-xiaochang-20', (251,218,65)),
        ('L-xiaochang-20', 'L-xiaochang-5', (251,218,65)),
        ('L-xiaochang-5', 'L-xiaochang-6', (251,218,65)),
        ('L-xiaochang-6', 'L-xiaochang-7', (251,218,65)),
        ('L-xiaochang-7', 'L-xiaochang-8', (251,218,65)),
        ('L-xiaochang-8', 'L-xiaochang-9', (251,218,65)),
        ('L-xiaochang-9', 'L-xiaochang-10', (251,218,65)),
        ('L-xiaochang-10', 'L-xiaochang-11', (251,218,65)),
        ('L-xiaochang-11', 'L-xiaochang-12', (251,218,65)),
        ('R-xiaochang-1', 'R-xiaochang-2', (251,218,65)),
        ('R-xiaochang-2', 'R-xiaochang-3', (251,218,65)),
        ('R-xiaochang-3', 'R-xiaochang-4', (251,218,65)),
        ('R-xiaochang-4', 'R-xiaochang-20', (251,218,65)),
        ('R-xiaochang-20', 'R-xiaochang-5', (251,218,65)),
        ('R-xiaochang-5', 'R-xiaochang-6', (251,218,65)),
        ('R-xiaochang-6', 'R-xiaochang-7', (251,218,65)),
        ('R-xiaochang-7', 'R-xiaochang-8', (251,218,65)),
        ('R-xiaochang-8', 'R-xiaochang-9', (251,218,65)),
        ('R-xiaochang-9', 'R-xiaochang-10', (251,218,65)),
        ('R-xiaochang-10', 'R-xiaochang-11', (251,218,65)),
        ('R-xiaochang-11', 'R-xiaochang-12', (251,218,65)),

        #肾经 下  鲸鱼灰
        ('R-shen-1', 'R-shen-2', (71,81,100)),
        ('R-shen-2', 'R-shen-3', (71,81,100)),
        ('R-shen-3', 'R-shen-4', (71,81,100)),
        ('R-shen-4', 'R-shen-5', (71,81,100)),
        ('R-shen-5', 'R-shen-6', (71,81,100)),
        ('R-shen-6', 'R-shen-7', (71,81,100)),
        ('R-shen-7', 'R-shen-8', (71,81,100)),
        ('R-shen-8', 'R-shen-9', (71,81,100)),
        ('R-shen-9', 'R-shen-10', (71,81,100)),
        ('R-shen-10', 'R-shen-11', (71,81,100)),
        ('R-shen-11', 'R-shen-12', (71,81,100)),
        ('R-shen-12', 'R-shen-13', (71,81,100)),
        ('L-shen-1', 'L-shen-2', (71,81,100)),
        ('L-shen-2', 'L-shen-3', (71,81,100)),
        ('L-shen-3', 'L-shen-4', (71,81,100)),
        ('L-shen-4', 'L-shen-5', (71,81,100)),
        ('L-shen-5', 'L-shen-6', (71,81,100)),
        ('L-shen-6', 'L-shen-7', (71,81,100)),
        ('L-shen-7', 'L-shen-8', (71,81,100)),
        ('L-shen-8', 'L-shen-9', (71,81,100)),
        ('L-shen-9', 'L-shen-10', (71,81,100)),
        ('L-shen-10', 'L-shen-11', (71,81,100)),
        ('L-shen-11', 'L-shen-12', (71,81,100)),
        ('L-shen-12', 'L-shen-13', (71,81,100)),
        # sanjiao
        ('R-sanjiao-1', 'R-sanjiao-2', (255, 0 , 255)),
        ('R-sanjiao-2', 'R-sanjiao-3', (255, 0 , 255)),
        ('R-sanjiao-3', 'R-sanjiao-4', (255, 0 , 255)),
        ('R-sanjiao-4', 'R-sanjiao-5', (255, 0 , 255)),
        ('R-sanjiao-5', 'R-sanjiao-6', (255, 0 , 255)),
        ('R-sanjiao-6', 'R-sanjiao-7', (255, 0 , 255)),
        ('R-sanjiao-7', 'R-sanjiao-8', (255, 0 , 255)),
        ('R-sanjiao-8', 'R-sanjiao-9', (255, 0 , 255)),
        ('R-sanjiao-9', 'R-sanjiao-10', (255, 0 , 255)),
        ('R-sanjiao-10', 'R-sanjiao-11', (255, 0 , 255)),
        ('R-sanjiao-11', 'R-sanjiao-12', (255, 0 , 255)),
        ('R-sanjiao-12', 'R-sanjiao-13', (255, 0 , 255)),
        ('R-sanjiao-13', 'R-sanjiao-14', (255, 0 , 255)),
        ('R-sanjiao-14', 'R-sanjiao-15', (255, 0 , 255)),
        ('R-sanjiao-15', 'R-sanjiao-16', (255, 0 , 255)),
        ('R-sanjiao-16', 'R-sanjiao-17', (255, 0 , 255)),
        ('R-sanjiao-17', 'R-sanjiao-18', (255, 0 , 255)),
        ('R-sanjiao-18', 'R-sanjiao-19', (255, 0 , 255)),
        ('R-sanjiao-19', 'R-sanjiao-20', (255, 0 , 255)),
        ('R-sanjiao-20', 'R-sanjiao-21', (255, 0 , 255)),
        ('R-sanjiao-21', 'R-sanjiao-22', (255, 0 , 255)),
        ('R-sanjiao-22', 'R-sanjiao-23', (255, 0 , 255)),
        ('R-sanjiao-23', 'R-sanjiao-24', (255, 0 , 255)),

        ('L-sanjiao-1', 'L-sanjiao-2', (255, 0 , 255)),
        ('L-sanjiao-2', 'L-sanjiao-3', (255, 0 , 255)),
        ('L-sanjiao-3', 'L-sanjiao-4', (255, 0 , 255)),
        ('L-sanjiao-4', 'L-sanjiao-5', (255, 0 , 255)),
        ('L-sanjiao-5', 'L-sanjiao-6', (255, 0 , 255)),
        ('L-sanjiao-6', 'L-sanjiao-7', (255, 0 , 255)),
        ('L-sanjiao-7', 'L-sanjiao-8', (255, 0 , 255)),
        ('L-sanjiao-8', 'L-sanjiao-9', (255, 0 , 255)),
        #pangguang


        ('L-pangguang-4', 'L-pangguang-5', (0 ,255, 255)),
        ('L-pangguang-5', 'L-pangguang-6', (0 ,255, 255)),
        ('L-pangguang-6', 'L-pangguang-40', (0 ,255, 255)),

        ('L-pangguang-7', 'L-pangguang-30', (0 ,255, 255)),
        ('L-pangguang-30', 'L-pangguang-8', (0 ,255, 255)),
        ('L-pangguang-8', 'L-pangguang-9', (0 ,255, 255)),
        ('L-pangguang-9', 'L-pangguang-10',  (0,255,255)),
        ('L-pangguang-10', 'L-pangguang-11', (0,255,255)),
        ('L-pangguang-11', 'L-pangguang-12', (0,255,255)),
        ('L-pangguang-12', 'L-pangguang-13', (0,255,255)),
        ('L-pangguang-13', 'L-pangguang-14', (0,255,255)),
        ('L-pangguang-14', 'L-pangguang-15', (0,255,255)),
        ('L-pangguang-15', 'L-pangguang-16', (0,255,255)),
        ('L-pangguang-16', 'L-pangguang-17', (0,255,255)),

        ('L-pangguang-18', 'L-pangguang-19', (255,255,0)),
        ('L-pangguang-19', 'L-pangguang-20', (255,255,0)),
        ('L-pangguang-20', 'L-pangguang-21', (255,255,0)),
        ('L-pangguang-21', 'L-pangguang-22', (255,255,0)),
        ('L-pangguang-22', 'L-pangguang-23', (255,255,0)),
        ('L-pangguang-23', 'L-pangguang-24', (255,255,0)),


        ('R-pangguang-4', 'R-pangguang-5', (0 ,255, 255)),
        ('R-pangguang-5', 'R-pangguang-6', (0 ,255, 255)),
        ('R-pangguang-6', 'R-pangguang-40', (0 ,255, 255)),

        ('R-pangguang-7', 'R-pangguang-30', (0,255,255)),
        ('R-pangguang-30', 'R-pangguang-8', (0,255,255)),
        ('R-pangguang-8', 'R-pangguang-9', (0,255,255)),
        ('R-pangguang-9', 'R-pangguang-10',  (0,255,255)),
        ('R-pangguang-10', 'R-pangguang-11', (0,255,255)),
        ('R-pangguang-11', 'R-pangguang-12', (0,255,255)),
        ('R-pangguang-12', 'R-pangguang-13', (0,255,255)),
        ('R-pangguang-13', 'R-pangguang-14', (0,255,255)),
        ('R-pangguang-14', 'R-pangguang-15', (0,255,255)),
        ('R-pangguang-15', 'R-pangguang-16', (0,255,255)),
        ('R-pangguang-16', 'R-pangguang-17', (0,255,255)),

        ('R-pangguang-18', 'R-pangguang-19', (255,255,0)),
        ('R-pangguang-19', 'R-pangguang-20', (255,255,0)),
        ('R-pangguang-20', 'R-pangguang-21', (255,255,0)),
        ('R-pangguang-21', 'R-pangguang-22', (255,255,0)),
        ('R-pangguang-22', 'R-pangguang-23', (255,255,0)),
        ('R-pangguang-23', 'R-pangguang-24', (255,255,0)),    



        ('R-dan-1', 'R-dan-2', (255,255,0)),    
        ('R-dan-2', 'R-dan-3', (255,255,0)),    
        ('R-dan-3', 'R-dan-4', (255,255,0)),    
        ('R-dan-4', 'R-dan-5', (255,255,0)),    
        ('R-dan-5', 'R-dan-6', (255,255,0)),    
        ('R-dan-6', 'R-dan-7', (255,255,0)),    
        ('R-dan-7', 'R-dan-8', (255,255,0)),    
        ('R-dan-8', 'R-dan-9', (255,255,0)),    
        ('R-dan-9', 'R-dan-10', (255,255,0)),    
        ('R-dan-10', 'R-dan-11', (255,255,0)),    
        ('R-dan-11', 'R-dan-12', (255,255,0)),    
        ('R-dan-12', 'R-dan-13', (255,255,0)),    
        ('R-dan-13', 'R-dan-14', (255,255,0)),    
        ('R-dan-14', 'R-dan-15', (255,255,0)),    
        ('R-dan-15', 'R-dan-16', (255,255,0)),    
        ('R-dan-16', 'R-dan-17', (255,255,0)),    
        ('R-dan-17', 'R-dan-18', (255,255,0)),  

        #督脉
        ('du-20', 'du-21', (255,255,0)),    
        ('du-21', 'du-22', (255,255,0)),    




    ]



