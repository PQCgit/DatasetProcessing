# -*- coding: UTF-8 -*-
# 开发人员  ：Chen
# 开发时间  ：2023/3/8 17:56
# 开发名称  ：test.py
# 开发工具  ：PyCharm
#   描述   ：
import os
from os import getcwd
import cv2


# 更改当前工作目录为 S:\code\python\datasets\zj-dataset\train
os.chdir(r"S:\code\python\datasets\zj-dataset\train")
print("Now work position : %s" % getcwd())  # 打印当前工作路径

classes = ['holothurian', 'echinus', 'scallop', 'starfish', 'waterweeds']  # 类别名称
img_dir = "./Images/"  # 所有图像文件地址
lab_dir = "./Annotations/"  # 所有标签文件地址(VOC的xml格式)
imgsname_list = os.listdir(img_dir)  # 文件夹下的 img 文件名列表
imgs_num = len(imgsname_list)

print('类别数量:', len(classes))


# /**************************************************/

# 统计类别标签数量；
# 小目标(lab < 32*32=1024)、中目标(32*32 <= lab <= 96x96)、大目标(lab > 96x96)标签框数量；
# 无标签文件数量(即没有标签的图片数量)

import xml.etree.ElementTree as ET

non_lab = 0  # 方法1：通过无 object 键，统计无标签的图片数量
non_lab1 = 0  # 方法2：通过统计 object 键数量，统计无标签的图片数量（这两个值必然相等）
non_lab_file = open(getcwd() + "./non_lab_file.txt", 'w')  # 存放无标签文件名的文件(绝对路径)
small_objnum1, mid_objnum1, lar_objnum1 = 0, 0, 0  # 绝对尺寸定义法：小、中、大目标的数量
small_objnum2, mid_objnum2, lar_objnum2 = 0, 0, 0  # 相对尺寸定义法：小、中、大目标的数量
size_count = {}  # 存储不同尺寸的图片数量
for imgname in imgsname_list:  # 遍历所有文件名
    # 读取当前图片的高/宽
    # file_path = os.path.join(img_dir, imgname)
    # img = cv2.imread(file_path)
    # h = int(img.shape[0])
    # w = int(img.shape[1])
    # img_area = h*w

    # 读取标签框的高/宽
    xml_file = open('%s/%s.xml' % (lab_dir, imgname[:-4]), encoding='utf-8')  # xml 文件对象
    tree = ET.parse(xml_file)  # 解析xml文件
    root = tree.getroot()  # 获得对应的键值对

    # 通过 xml 获得图片的尺寸大小
    size = root.find('size')
    assert size !=  None, "xml 不存在 size 键"  # 若是不存在 size 键，则返回 None
    # 获得宽
    w = int(size.find('width').text)
    # 获得高
    h = int(size.find('height').text)
    img_area = h * w
    h_w = (h, w)
    if h_w in size_count:
        size_count[h_w] += 1
    else:
        size_count[h_w] = 1

    if root.find('object') == None:  # 无 object 即表明该图片没有标签，若是有 object 没有 name 必然报错，所以通过此方法进行统计
        non_lab += 1
        non_lab_file.write(os.path.abspath(xml_file.name) + '\n')  # 获取文件的绝对路径并写入路径
    obj_num = 0  # 当前图片标签数量
    for obj in root.iter('object'):  # 遍历当前 xml 文件里的键obj
        obj_num += 1
        cls = obj.find('name').text  # 获取当前Element对象的文本内容(即返回字符串类型的数据)
        if cls not in classes:
            print("Not find in classes : %s      File : " % (cls, xml_file))
            continue

        # 计算框的面积
        xmlbox = obj.find('bndbox')
        b = [float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
             float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text)]  # voc格式坐标
        box_area = (b[3] - b[2]) * (b[1] - b[0])  # 高度(ymax - ymin) * 宽度(xmax - xmin )
        assert box_area >= 0, "box area 为负值"

        # 绝对尺寸定义法
        if box_area < (32*32):
            small_objnum1 += 1
        elif box_area >= 32*32 and box_area <= 96*96:
            mid_objnum1 += 1
        else:
            lar_objnum1 += 1

        # 相对尺寸定义法
        rate = box_area / img_area
        if rate < 0.01:
            small_objnum2 += 1
        elif rate <= 0.1 and rate >= 0.01:
            mid_objnum2 += 1
        else:
            lar_objnum2 += 1

    if obj_num == 0:
        non_lab1 += 1


if non_lab == non_lab1:
    print("\n无标签的图片数量：%d   存放无标签文件名的文件路径：%s" % (non_lab, os.path.abspath(non_lab_file.name)))
else:
    print("\n❌方法1无标签的图片数量：%d    方法2无标签的图片数量：%d❌" % (non_lab, non_lab1))
non_lab_file.close()

# 绝对尺寸定义法  小目标数量：4025   中目标数量：22623   大目标数量：14875
print("\n绝对尺寸定义法  小目标数量：%d   中目标数量：%d   大目标数量：%d" % (small_objnum1, mid_objnum1, lar_objnum1))
# 相对尺寸定义法  小目标数量：28113   中目标数量：13253   大目标数量：157
print("相对尺寸定义法  小目标数量：%d   中目标数量：%d   大目标数量：%d\n" % (small_objnum2, mid_objnum2, lar_objnum2))

for size, count in size_count.items():
    print(f"Size {size}: {count} images")
i = 1
for size, count in size_count.items():
    if i == len(size_count):
        print(f"{size}", end='')
    else:
        print(f"{size}:", end='')
    i += 1
print("----->", end='')
i = 1
for size, count in size_count.items():
    if i == len(size_count):
        print("%.2f" % (count/imgs_num), end='')
    else:
        print("%.2f:" % (count/imgs_num), end='')
    i += 1
print("\n一共%d张图片" % imgs_num)







