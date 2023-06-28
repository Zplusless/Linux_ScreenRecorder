
# %% 
from srv_video2jpg import video2jpg
from srv_count import analyze
import os
import numpy as np
import pickle
import os
import time

#! 修改本行地址即可
video_dir = '..'
# video_dir = '../120fps串流，DN不等时延/300ms good'

os.chdir(video_dir)
working_dir = '.'

cach_file = 'data_cache'
files = os.listdir(working_dir)
raw_data = {}
frame_diff = {}

if os.path.exists(cach_file):
    os.remove(cach_file)
time.sleep(1)

if os.path.exists(cach_file):
    print('找到cache，读入数据')
    with open(cach_file, 'rb') as f:
        raw_data, frame_diff = pickle.load(f)
else:
    print('cache不存在，重新整理数据')
    for f in files:
        if '.mp4' in f:
            path = os.path.join(working_dir, f)
            video2jpg(path)
            dd, df = analyze(path[:-4])
            raw_data[f[:-4]] = dd
            frame_diff[f[:-4]] = df
    
    with open(cach_file, 'wb') as f:
        pickle.dump((raw_data, frame_diff), f)
#%%
# frame_diff



#%%
for k,v in raw_data.items():
    print(f'{k}---> 1:{len(v[1])}  2:{len(v[2])}')




# %%
# 两个流分别取多少个数据
n1 = min([len(frame_diff[k][1]) for k in frame_diff.keys()])
n2 = min([len(frame_diff[k][2]) for k in frame_diff.keys()])
fd1=[]
fd2=[]
# frame_df_np = {}
for key in frame_diff.keys():
    fd1.append(frame_diff[key][1][1:n1])  # 舍弃第一组，最后一组舍去比 其它组多的
    fd2.append(frame_diff[key][2][1:n2])
    

# %%
npfd1 = np.array(fd1)
npfd2 = np.array(fd2)
# %%
sum1 = npfd1.sum(axis=0)
sum2 = npfd2.sum(axis=0)
# %%
sum1/len(npfd1)*1000/120

# %%
sum2/len(npfd1)*1000/120
# %%
