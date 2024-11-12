# -*- coding: UTF-8 -*-
# 开发人员  ：Chen
# 开发时间  ：2023/5/12 11:12
# 开发名称  ：rmfile.py
# 开发工具  ：PyCharm
#   描述   ：
import os

image_folder = "rm/images"
label_folder = "rm/txt"

# 获取所有图片的文件名列表
image_files = os.listdir(image_folder)

# 获取所有带标签的图片的文件名列表
labeled_files = []
for file_name in image_files:
    label_file_name = os.path.join(label_folder, os.path.splitext(file_name)[0] + ".txt")
    if os.path.isfile(label_file_name):
        labeled_files.append(file_name)

# 找到没有标签的图片
unlabeled_files = []
for file_name in image_files:
    if file_name not in labeled_files:
        unlabeled_files.append(os.path.join(image_folder, file_name))

# 删除没有标签的图片
for file_name in unlabeled_files:
    os.remove(file_name)
