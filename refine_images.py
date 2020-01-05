import cv2
import shutil
import os
import glob
import numpy as np
from tkinter import filedialog
import sys

Root = filedialog.askdirectory()
Folderlist = os.listdir(Root)
Folderlist = [folder for folder in Folderlist if (folder.startswith('TEST') or folder.startswith('HUWJ'))]
count = 0

def refine_imglist(imglist):

    refine_img_list = []

    for j in range(len(imglist)):

        try:
            ori_img = cv2.imread(os.path.join(Root, Folderlist[i], imglist[j]), 1)
            ori_img = cv2.resize(ori_img, None, fx=4, fy=4, interpolation=cv2.INTER_LINEAR)
            newimg = ori_img.astype(np.uint8)
            refine_img_list.append(newimg)

        except:
            print("image is corrupt {}".format(imglist[j]))
            continue

    return refine_img_list

for i in range(len(Folderlist)):

    imgs = glob.glob1(os.path.join(Root, Folderlist[i]), '*.bmp')
    imgs = [os.path.basename(name) for name in imgs]

    refine_data = refine_imglist(imgs)

    print("현재 폴더명 = " + Folderlist[i])
    print("현재 폴더 파일 개수 = " , len(refine_data))

    movelist = []
    q = 0

    while q < len(refine_data):

        cv2.imshow('img', refine_data[q])
        # ch = cv2.waitKey(0)
        ch = cv2.waitKeyEx(0)

        if ch == 32: # 스페이스로 해당 이미지 분류
            try:
                print('Move')
                movelist.append(os.path.join(Root, Folderlist[i], imgs[q]))
                q += 1

            except:
                print("Can't Duplicate Image {}".format(imgs[q]))

        elif ch == 48: # 오른쪽 숫자판 0 뒤로가기

            print('Back')
            q -= 1
            if q < 0:
                q = 0
                print('Back to ' + str(q))

        elif ch == ord('q'): #강제 종료
            sys.exit()

        elif int(ch) == 0x250000:
            print('Back')
            q -= 1
            if q < 0:
                q = 0
                print('Back to ' + str(q))

        else:
            q += 1

    # Move files
    movelist = list(set(movelist)) # 혹시모를 중복제거

    if not os.path.exists(os.path.join(Root, 'Trash')):
        os.mkdir(os.path.join(Root, 'Trash'))

    result = os.path.join(Root, 'Trash')

    for p in range(len(movelist)):
        shutil.copy(movelist[p], os.path.join(result, str(count)+'.bmp'))
        count += 1 # 이미지명이 겹치지 않게 구분