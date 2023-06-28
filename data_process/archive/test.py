#%%

import cv2
import numpy as np
import matplotlib.pyplot as plt

#! opencv 的颜色是BGR


# 15 950
img = cv2.imread(f"srv_mig_03_59_22/frame15.jpg")
esc = img[20, 100]
menu = img[216, 592]

#%%
len(img[1])

#%%
type(img[0][0])
# %%
# for i in range(600):
#     for j in range(800):
#         # if np.equal(img[i,j], [255,255,0]):
#         if (img[i,j] == [255, 255, 0]).all():
#             print(i ,j)


#%%
# cv2.imwrite('frame.jpg',img[10:60,2:100])
# cv2.imshow('image', img[20:25,20:25])
# cv2.waitKey(0)
# cv2.destroyAllWindows()


#%%
img = cv2.imread(f"srv_mig_03_59_22/frame36.jpg")
plt.plot('image')
plt.imshow(img[180:190,150:160])
print(img[180:190,150:160])

#%%
for i in range(20,25):
    for j in range(20,25):
        print(img[i,j][0]>235 and img[i,j][1]>235)


#%%
for i in range(1000):
    img = cv2.imread(f"srv_mig_03_59_22/frame{i}.jpg")
    if (img[40,425] == [255, 255, 0]).all():
        print(i)


# %%
l=[0]
for i in range(1979):
    img = cv2.imread(f"srv_mig_03_59_22/frame{i}.jpg")
    # print(img[25,25])
    if sum(img[80,710])>400:
    # if (img[180,150]==[48,51,49]).all():
        l.append(i)
# %%
for i in range(1,len(l)-1):
    if l[i+1]!=(l[i]+1) or l[i-1]!=(l[i]-1):
        print(l[i])


# %%
img = cv2.imread(f"srv_mig_03_59_22/frame1550.jpg")
plt.plot('image')
plt.imshow(img[80:81,710:711])
print(img[80:81,710:711])
# %%
