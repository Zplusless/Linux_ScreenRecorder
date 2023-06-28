# 1. 使用PIL截图，使用opencv生成视频
# 2. 采用多线程结构，将图像采集和视频写入分开，保障图像采集的频率（实时证明不会受GIL的影响）
# 3. VideoGet中录屏需要warm up，在init阶段拿到的帧率普遍偏小（几十fps），因而限制了整体的fps，warm up之后能到300fps
# 4. 截图进程和主进程之间信息传递不应该使用队列，因为如果子进程截图fps大于主进程写入视频的fps，会导致写入的帧不是当前截图的帧，容易产生漂移。
#   - 前几个commit中帧率上不去是因为VideoGet中录屏需要warm up，在init阶段拿到的帧率普遍偏小，因而限制了整体的fps
#   - 本commit中取消了Queue而是采用Manager中的数据共享，缓冲区大小只有1，没有读取的会被后面覆盖，避免了写（200+fps）快于读（120fps）造成的esc水印与esc弹出menu不同步。




import numpy as np
from PIL import ImageGrab
import cv2
import time
from threading import Thread
import socket
import logging
from typing import Tuple


from utils.call_cmd import cmd
from utils.timmer import wait,hms
import utils.switch_window as sw
import config


hostname = socket.gethostname()
logging.basicConfig(
    level=logging.INFO, 
    format= f'%(asctime)s - {hostname} - %(levelname)s - %(message)s', #'%(asctime)s - %(levelname)s - %(message)s',
    filename='record_screen.log',
    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
    )
log = logging.getLogger('record_screen')




class VideoGet:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self, fps:int, length):
        self.length = length

        im = ImageGrab.grab()
        self.size = im.size
        self.fps = fps
        # self.data_manager = Manager()
        # self.shared_data = self.data_manager.dict()
        # self.shared_data['running'] = True #! 使用进程共享的变量，否则后面stop失效
        self.running = True
        _, self.frame = self.next_frame()

    def next_frame(self) -> Tuple[int, np.ndarray]:
        t1 = time.time()
        im = ImageGrab.grab()
        im_cv = cv2.cvtColor(np.array(im), cv2.COLOR_BGR2RGB)
        t = time.time()-t1
        return 1/t, im_cv

    def start(self):    
        self.start_time = time.time()
        Thread(target=self.get, args=()).start()
        return self, self.size

    def get(self):
        ptime = time.time()
        while self.running:

            fps, self.frame = self.next_frame()
            log.info(fps)


            if time.time() - self.start_time > self.length:
                print(f'{self.__class__}: time exceeded, end process')
                break
            
        print('Screen recording process stopped!')

    def read(self):
        return self.frame
            
    def stop(self):
        self.running = False





class LocalRecorder:
    def __init__(self, path:str, length=30, fps=120) -> None:
        fourcc = cv2.VideoWriter_fourcc(*'avc1')  # 设置视频编码格式
        # self.fps = fps # 设置帧率
        # init只是给出期望帧率，VideoGet返回的是实际帧率
        self.capture, self.size = VideoGet(fps, length=length).start()
        self.fps = fps
        self.writer = cv2.VideoWriter(path, fourcc, self.fps, self.size)
        self.length = length
        self.is_running=True
        self.show_text = False
        

    def run(self):

        time.sleep(1) # 等待录屏进程开始写入

        ptime = time.time()
        t_start = ptime
        in_app_ptime = ptime
        count = 0
        print(f'self.fps={self.fps}')
        while self.is_running:  # 开始录制
            # 图像写入
            nowtime = time.time()
            if (nowtime-ptime)>=1/(self.fps*1.04):  #! 正常录屏会略低于fps，乘上1.04进行弥补
                frame = self.capture.read()
                if config.IN_APP_LATENCY_MEASURE:
                    if nowtime - in_app_ptime > config.IN_APP_LATENCY_INTERVAL:
                        sw.press_esc()
                        self.show_text = (self.show_text==False)  # True False交替出现
                        in_app_ptime = time.time()
                    if self.show_text:
                        # https://docs.opencv.org/4.x/d6/d6e/group__imgproc__draw.html#ga5126f47f883d730f633d74f07456c576   
                        cv2.putText(frame, 'ESC Pressed', (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 3.0, (255, 255, 0), thickness = 5)
                
                self.writer.write(frame)
                count+=1
                ptime=nowtime
            
            if time.time()-t_start>=self.length:  # 当某某条件满足中断循环
                print(f'默认录屏30s，以超时，任务退出')
                break
        tt = time.time()-t_start
        print(f'录制结束，共录制{tt}秒, 总帧数为{count}, 实际fps{count/tt}')
        self.release()


    def release(self):
        self.writer.release()
        self.capture.stop()
        time.sleep(1)# 避免主进程比子进程早结束，出现broken pipe
        print('release cv writer, end!')

    def close(self):
        self.is_running=False


if __name__ == "__main__":
    # 启动要录屏的应用
    res, t1 = cmd(f"~/minetest/bin/minetest --address {config.CLOUD_IP} --port 30000 --name {config.GAME_ACCOUNT} --password {config.GAME_PASSWORD} --go", False, logfile='minetest_output.log')
    
    time.sleep(3)
    r = LocalRecorder(f'ue_log/srv_mig_{hms()}.mp4', fps=150)
    t = Thread(target=r.run)
    t.start()

    time.sleep(6)  # run会先等1s让VideoGet那边有数据写入
    r.close()
    print('end\n\n')