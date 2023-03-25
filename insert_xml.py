# -*- coding: UTF-8 -*-
# 开发人员  ：Chen
# 开发时间  ：2023/3/8 21:08
# 开发名称  ：insert_xml.py
# 开发工具  ：PyCharm
#   描述   ：往文件夹中的所有 xml 文件中添加图片的尺寸信息
import os
import cv2
import xml.etree.ElementTree as ET


def insert(xml_path, img_path):
    # 读取当前图片的高/宽
    img = cv2.imread(img_path)
    h = str(img.shape[0])
    w = str(img.shape[1])
    c = str(img.shape[2])
    print("%s  %s  h = %s  w = %s  c = %s" % (img_path, xml_path, h, w, c))

    # 从当前xml文件中读取，使用getroot()获取根节点，得到的是一个Element对象
    tree = ET.parse(xml_path)
    root = tree.getroot()

    try:
        t = root.find("size").text   # 属性，若是 difficult 节点不存在，则发出异常
    except:  # 捕获任何类型的异常
        x = ET.Element("size")      # 创建节点属性
        root.append(x)                 # 将 x 节点添加入 object 节点的子节点

    object = root.find('size')
    try:
        t = object.find("height").text  # 属性，若是 height 节点不存在，则发出异常
    except:  # 捕获任何类型的异常
        x = ET.Element("height")  # 创建节点属性
        x.text = h  # 属性值
        object.append(x)  # 将 x 节点添加入 object 节点的子节点

    try:
        t = object.find("width").text  # 属性，若是 width 节点不存在，则发出异常
    except:  # 捕获任何类型的异常
        x = ET.Element("width")  # 创建节点属性
        x.text = w  # 属性值
        object.append(x)  # 将 x 节点添加入 object 节点的子节点

    try:
        t = object.find("depth").text  # 属性，若是 depth 节点不存在，则发出异常
    except:  # 捕获任何类型的异常
        x = ET.Element("depth")  # 创建节点属性
        x.text = c  # 属性值
        object.append(x)  # 将 x 节点添加入 object 节点的子节点
        tree.write(xml_path)  # 写入 xml 文件

def main():
    xml_dir = r"S:\code\python\datasets\zj-dataset\test-A-box"  # xml文件夹的绝对路径
    img_dir = r"S:\code\python\datasets\zj-dataset\test-A-image"  # img文件夹的绝对路径
    xml_path_list = [os.path.join(xml_dir, x) for x in os.listdir(xml_dir)]
    img_path_list = [os.path.join(img_dir, x) for x in os.listdir(img_dir)]


    for i in range(len(xml_path_list)):  # 遍历每个 xml 文件
        insert(xml_path_list[i], img_path_list[i])


if __name__ == '__main__':
    main()

