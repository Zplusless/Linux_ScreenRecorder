import numpy as np
from PIL import ImageGrab
import cv2
import time
from threading import Thread


class Recorder:
    def __init__(self, path:str, length=20, fps=24) -> None:
        im = ImageGrab.grab()
        self.width, self.high = im.size  # 获取屏幕的宽和高
        fourcc = cv2.VideoWriter_fourcc(*'avc1')  # 设置视频编码格式
        self.fps = fps # 设置帧率
        self.video = cv2.VideoWriter(path, fourcc, fps, (self.width, self.high))
        self.length = length
        self.is_running=True

    def run(self):
        t_start = time.time()
        while self.is_running:  # 开始录制
            im = ImageGrab.grab()
            im_cv = cv2.cvtColor(np.array(im), cv2.COLOR_BGR2RGB)
            # 图像写入
            self.video.write(im_cv)
            # time.sleep(1/self.fps)
            if time.time()-t_start>=self.length:  # 当某某条件满足中断循环
                break
        
        self.video.release()  # 释放缓存，持久化视频
        print(f'录制结束，共录制{time.time()-t_start}秒')

    def close(self):
        self.is_running=False


if __name__ == "__main__":
    r = Recorder('./test.mp4')
    t = Thread(target=r.run)
    t.start()
    time.sleep(5)
    r.close()