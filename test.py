from PIL import ImageGrab
import time
import cv2
import numpy as np

t1 = time.time()
im = ImageGrab.grab()
im_cv = cv2.cvtColor(np.array(im), cv2.COLOR_BGR2RGB)
t = time.time()-t1

print(f'每次截屏用时{t}，fps={1/t}')
