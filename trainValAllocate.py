# -*- coding: UTF-8 -*-
# 开发人员  ：Chen
# 开发时间  ：2023/3/8 14:16
# 开发名称  ：trainValAllocate.py
# 开发工具  ：PyCharm
#   描述   ：将数据集划分为训练集(80%)和验证集(20%)，采用固定间隔抽样的方法进行抽样。


import os
from os import getcwd

# 更改当前工作目录为 S:\code\python\datasets\zj-dataset\train
os.chdir(r"/home/team01/detection/datasets/zj-dataset/test-A")
print("Now work position : %s" % getcwd())  # 打印当前工作路径

img_dir = "./images/"  # 所有图像文件地址
imgsname_list = os.listdir(img_dir)  # 文件夹下的 img 文件名列表
#imgsname_list = sorted(imgsname_list, key=lambda x: int(''.join(filter(str.isdigit, x))))  # 按数字顺序排列
img_num = len(imgsname_list)  # 图片数量


ratio = 10
train_f = open("test.txt", 'w')  # 存放训练集图片的文件（相对路径）
for i, imgname in enumerate(imgsname_list):
    hangContent = img_dir + imgname + '\n'  # 一张图片的相对路径
    train_f.write(os.path.abspath(hangContent))


train_f.close()
