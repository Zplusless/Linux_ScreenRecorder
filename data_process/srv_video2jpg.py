import time
import os

import cv2
import numpy as np

# videoname 指定了视频路径


def video2jpg(videoname):
    videonamewithoutext = videoname[:-4]

    # 创建存储该视频文件每一帧图像的文件夹
    if not os.path.exists(videonamewithoutext):
        print(f'{videonamewithoutext}不存在，开始处理')
        os.mkdir(videonamewithoutext)
    else:
        print(f'{videonamewithoutext}已经存在，跳过')
        return 0

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


if __name__ == "__main__":
    videoname = "srv_mig_04_01_56.mp4"
    video2jpg(videoname)