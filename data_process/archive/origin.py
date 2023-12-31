import time
import os

import cv2
import numpy as np

# videoname 指定了视频路径
videoname = "/Users/zli/Desktop/data/streaming_mplayer_9_17/IMG_2604.MOV"
videonamewithoutext = videoname[:-4]

# 创建存储该视频文件每一帧图像的文件夹
if not os.path.exists(videonamewithoutext):
    os.mkdir(videonamewithoutext)

# 读取视频，获得 fps
vod4g = cv2.VideoCapture(videoname)
fps = vod4g.get(cv2.CAP_PROP_FPS)

# 将视频中每一帧存储为图片
count = 0
success = True
while success:
    success, frame = vod4g.read()
    if success:
        cv2.imwrite(os.path.join(videonamewithoutext, f"frame{count}.jpg"), frame)
        count += 1


# 记录 ESC 是否按下，菜单是否出现
pressEsc = False
occursMenu = False

# two dicts with {key: frame_num, value: appear_time}
# used for debug
pressEscFrameTime = {}
occursMenuFrameTime = {}

pressEscTime = []
occursMenuTime = []

# 从第 30 帧开始，排除前边的无用操作，减少几帧图片检测
for i in range(30, count):
    # 读取每一帧图片，检查图片上的两个像素点
    # 像素点需要根据录制的视频点击和菜单出现的位置设置
    # 所以需要预先处理图像
    img = cv2.imread(f"frame{i}.jpg")
    esc = img[67, 675]
    menu = img[216, 592]

    # press Esc now
    if not pressEsc and esc[0] > 150:
        pressEsc = True
        pressEscFrameTime[i] = i/fps
        pressEscTime.append(i/fps)
    # normal mode (not press Esc)
    if pressEsc and esc[0] < 100:
        pressEsc = False

    # menu occurs
    if not occursMenu and menu[-1] > 200:
        occursMenu = True
        occursMenuFrameTime[i] = i/fps
        occursMenuTime.append(i/fps)
    # menu disappear
    if occursMenu and menu[-1] < 100:
        occursMenu = False

# 检查按下 ESC 的次数是否等于二倍的菜单弹出次数
# 如果不等，说明某个行为没有被检测到
# 可以通过打印两个 dict 进行 debug
assert len(pressEscFrameTime) == 2 * len(occursMenuFrameTime)

# 去除第二次按下 ESC 的时间
# 让第一次按下 ESC 的时间 presstime_cut 和菜单出现的时间 occursMenuTime 一一对应
presstime_cut = [pressEscTime[i] for i in range(0, len(pressEscTime), 2)]

# 记录响应延迟
response_delay = []
for i in range(len(presstime_cut)):
    response_delay.append(occursMenuTime[i] - presstime_cut[i])

rd_avg = np.average(response_delay)
rd_std = np.std(response_delay)