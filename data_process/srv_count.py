#%%
import cv2
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import os
from utils import memorize


def esc_on(img:cv2.Mat):
    '''
    判断图片左上角是否有ESC PRESSED字样
    '''
    if sum(img[45,23])>400:
        return True
    else:
        return False
    

def menu_appear(img:cv2.Mat):
    '''
    判断菜单是否出现
    '''
    if sum(img[387,360])>700:
        return True
    else:
        return False
    

def stream_id(img:cv2.Mat):
    '''
    返回当前画面是来自dn1还是dn2
    '''
    if sum(img[80,710])>400:
        return 2
    else:
        return 1
    

def analyze(dir_name: str):
    file_num = len(os.listdir(dir_name))
    print(f"{dir_name}: {file_num}")

    raw_data = {1:[], 2:[]}
    frame_diff = {1:[], 2:[]}

    img = cv2.imread(f"{dir_name}/frame0.jpg")
    p_esc = esc_on(img)
    p_menu = menu_appear(img)
    p_id = 1
    temp = [0,-1]

    for i in range(1,file_num):
        img = cv2.imread(f"{dir_name}/frame{i}.jpg")
        id = stream_id(img)
        esc = esc_on(img)
        menu = menu_appear(img)
        if esc != p_esc:
            temp[0] = i
            p_esc = esc
        
        if menu!=p_menu:
            temp[1] = i
            p_menu = menu

        if id!=p_id:
            temp=[-1,-1]
            p_id=id
            p_esc = esc
            p_menu = menu

        if -1 not in temp:
            raw_data[id].append(temp)
            frame_diff[id].append(temp[1]-temp[0])
            temp = [-1,-1]
    
    return raw_data, frame_diff

#%%
if __name__ == "__main__":
    dir_name = 'srv_mig_04_01_56' # 'srv_mig_03_59_22'
    dd, df = analyze(dir_name)


