# -*- coding: UTF-8 -*-
# 开发人员  ：Chen
# 开发时间  ：2023/3/10 22:00
# 开发名称  ：class.py.py
# 开发工具  ：PyCharm
#   描述   ：数据集处理类
#   1.前提：数据集的图片和标签名称一一对应，且文件名为数字，从1开始；
#          必须将图片和标签文件夹放在数据集的路径下；
#   2.模型模式：VOCInit —— 数据集未分配状态，只需要所有图片和标签文件夹的路径
#             VOCandYOLOv5 —— 数据集完备状态，已经划分好数据集，只需要做一些分析及信息解释。（必须提供训练集和验证集的txt文件，测试集可以没有，若有必须也是txt文件）
#   3.基本属性：dataset_classes —— [str(,str)] 数据集类别名称列表
#              dataset_mode —— str 数据集模式
#              dataset_path —— str 数据集路径
#              dataset_num —— int 数据集图片数量
#              files_name —— {"train":[str(,str)], "val":[str(,str)], "test":[str(,str)]} 训练集、验证集和测试集的图片名称
#              files_num —— {"train":int, "val":int, "test":int} 训练集、验证集和测试集的图片数量
#              imagesdir_path —— {"train":str, "val":str, "test":str} 训练集、验证集和测试集的图片文件夹路径
#              labelsdir_path —— {"train":str, "val":str, "test":str} 训练集、验证集和测试集的标签文件夹路径
#   4.注："all"字典只是一个暂时的，表示未分配的情况，未分配的情况下也可以执行诸如操作：数据集划分(划分后"all"会被取消，进入数据集完备状态)数据集格式转换、保存图片路径。
#        YOLOv5的训练集、验证集和测试集支持的图片文件夹的名称为"images"，标签文件夹的名称为"labels"，不修改为此名称的话会报错找不到文件。


import xml.etree.ElementTree as ET
import os
from os import listdir, getcwd
import cv2
from pathlib import Path  # 将路径转化为一个元组
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


mode_list = ["VOCInit", "VOCandYOLOv5"]
class DatasetProcess:
    # dataset_path : str 数据集的主目录
    # imagedir_path : dict 图片文件夹(或图片路径集合的txt文件)的绝对路径
    # labeldir_path  : dict 标签文件夹的绝对路径
    # dataset_classes : str 类别名称列表(非索引值)
    # test_path : list[str, str]
    def __init__(self, dataset_path, dataset_classes, imagesdir_path, labelsdir_path):
        # assert images_path.startswith(dataset_path), print("dataset_path is not a prefix of images_path")
        # assert images_path.startswith(labels_path), print("dataset_path is not a prefix of labels_path")

        self.dataset_path = dataset_path  # 数据集主目录
        self.imagesdir_path = imagesdir_path  # 图片文件夹的路径
        self.labelsdir_path = labelsdir_path  # 标签文件的路径
        self.dataset_classes = dataset_classes  # 数据集类别名称

        self.files_name = {"train": [], "val": [], "test": [], "all": []}  # 文件名称集合
        self.files_num = {"train": 0, "val": 0, "test": 0, "all": 0}  # 文件数量
        self.dataset_num = 0  # 数据集总图片数量(train+val+test)

        s = input("请输入数据集的模式：")
        assert s in mode_list, "输入错误，%s 不属于设定的模式集。" % s
        if s == "VOCInit":
            self.files_name["all"] = os.listdir(self.imagesdir_path["all"])
            self.files_name["all"].sort()  # 避免乱序
            self.files_name["all"] = [name[:-4] for name in self.files_name["all"]]  # 去掉 .jpg 后缀
            self.files_num["all"] = len(self.files_name["all"])
            self.dataset_num = self.files_num["all"]
        elif s == "VOCandYOLOv5":
            for data_str in self.imagesdir_path.keys():
                if os.path.isdir(self.imagesdir_path[data_str]):  # 若传入的是文件夹
                    self.files_name[data_str] = os.listdir(self.imagesdir_path[data_str])  # 当前数据集合的文件名列表
                    self.files_name[data_str].sort()  # 避免乱序
                elif os.path.isfile(self.imagesdir_path[data_str]):  # 若传入的是文件
                    images_f = open(self.imagesdir_path[data_str], 'r')
                    self.files_name[data_str] = images_f.read().strip('\n').splitlines()  # 读取文件(相对或绝对)路径列表
                    self.files_name[data_str] = [list(Path(path).parts)[-1] for i, path in enumerate(self.files_name[data_str])]  # 取得路径列表末索引值组成的新路径列表
                self.files_name[data_str] = [name[:-4] for name in self.files_name[data_str]]  # 去掉 .jpg 后缀
                self.files_num[data_str] = len(self.files_name[data_str])  # 当前数据集合的文件数量
                self.dataset_num += self.files_num[data_str]
            self.files_name["all"] = self.files_name["train"] + self.files_name["test"] + self.files_name["val"]
            self.files_name["all"].sort()  # 避免乱序

        self.dataset_mode = s  # 数据集的模式

        self.print_dataset()  # 打印数据集信息

    # def setFormat(self, format):
    #     """
    #     设置数据集模式
    #     :param format: str，模式名称
    #     :return:None
    #     """
    #     if format == "YOLOv5":
    #         # self.mode = "YOLOv5"
    #         print("\n数据集格式：YOLOv5", end='')
    #         if not os.path.exists(self.dataset_path + "\\images"):  # 若路 images 文件夹不存在，则改名
    #             os.rename(self.images_path, self.dataset_path + "\\images")  # 将存放图片的文件夹名称改为 images
    #         # self.images_path = self.dataset_path + "\\images"
    #         print("    将存放图片的文件夹名称改为 images（官方demo里指定 images 文件夹存放图片）。")


    def insertAttribute(self, img_path, xml_path):
        """
        往xml文件里插入属性
        :param img_path: 单个图片的路径
        :param xml_path: 图片对应标签文件(xml)路径
        :return:None
        """
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


    def convert(self, size, box):
        """
        坐标进行归一化操作
        :param size:  (原图w,原图h)
        :param box: (xmin,xmax,ymin,ymax) 分别表示矩形框的左上角和右下角的坐标
        :return: 相对于原图的物体中心点的 (x坐标比,y坐标比,宽度比,高度比) 取值范围[0-1]
        """
        dw = 1. / size[0]  # 1/w
        dh = 1. / size[1]  # 1/h
        x = (box[0] + box[1]) / 2.0  # 物体在图中的中心点x坐标
        y = (box[2] + box[3]) / 2.0  # 物体在图中的中心点y坐标
        w = box[1] - box[0]  # 物体实际像素宽度
        h = box[3] - box[2]  # 物体实际像素高度
        x = x * dw  # 物体中心点x的坐标比(相当于 x/原图w)
        w = w * dw  # 物体宽度的宽度比(相当于 w/原图w)
        y = y * dh  # 物体中心点y的坐标比(相当于 y/原图h)
        h = h * dh  # 物体宽度的宽度比(相当于 h/原图h)
        return (x, y, w, h)


    def xmlConvertTxt(self, data_list, abandon_classes=[], save_dir="labels_txt"):
        """
        将VOC格式(xml)转化为YOLO格式(txt)
        :param data_list: [str(,str)]，需要转化的数据,例如["train", "val"]或["all"]（注：不支持 "all" 与其它单独组合）
        :param abandon_classes:[str(,str)] 需要剔除的类别列表
        :param save_dir: str，保存的文件夹名称
        :return: None
        """
        for i, name in enumerate(abandon_classes):  # 转换为索引列表
            abandon_classes[i] = self.dataset_classes.index(name)
        abandon_classes.sort()  # 排序

        for data_str in data_list:  # 遍历每个数据集合
            abandon_num = 0  # 剔除次数
            print("\nStar %s file convert: xml -> txt , save to %s" % (data_str, self.dataset_path + "\\" + save_dir))
            if not os.path.exists(self.dataset_path + "/" + save_dir):  # 若路 save_dir 文件夹不存在，则创建
                os.makedirs(self.dataset_path + "/" + save_dir)
            for i, name in enumerate(self.files_name[data_str]):  # 遍历当前数据集合的每一个文件
                # print("处理号:%d   剩余量:%d   处理文件名:%s" % (i+1, self.files_num[data_str] - i, name), end='')
                in_file = open(self.labelsdir_path[data_str] + "/" + name + ".xml", encoding='utf-8')  # xml 文件对象
                out_file = open(self.dataset_path + '/' + save_dir + "/" + name + ".txt", 'w', encoding='utf-8')  # txt 文件对象

                tree = ET.parse(in_file)  # 解析xml文件
                root = tree.getroot()  # 获得对应的键值对
                # 先尝试通过 xml 中键值对获取图片尺寸
                size = root.find('size')  # 若是不存在 size 键，则返回 None
                if(size == None):
                    print("    xml存储的标签属性没有 size，创建 size 属性。", end='')
                    self.insertAttribute(self.imagesdir_path[data_str] + '/' + name + ".png",
                                         self.labelsdir_path[data_str] + '/' + name + ".xml")  # 往 xml 文件插入 size 属性
                    size = root.find('size')  # 若是不存在 size 键，则返回 None
                # 获得宽
                w = int(size.find('width').text)
                # 获得高
                h = int(size.find('height').text)
                for obj in root.iter('object'):  # 遍历当前 xml 文件里的键obj
                    cls = obj.find('name').text  # 获取当前Element对象的文本内容(即返回字符串类型的数据)
                    cls_id = 0
                    # 若是类别名不在预定义的类别名称列表中，则报错
                    assert (cls not in self.dataset_classes) or (cls not in [cls_id for cls_id, _ in enumerate(self.dataset_classes)]), \
                        "    find \"%s\" not in classes at %s." % (cls, "%s/%s.xml" % (self.labelsdir_path[data_str], name))
                    if isinstance(cls, int):
                        cls_id = int(cls)
                    else:
                        cls_id = self.dataset_classes.index(cls)  # 类别的数字索引

                    # 剔除不需要转换的类别
                    if cls_id in abandon_classes:  # 剔除
                        print("需要剔除的类属于文件：%s" % (in_file.name))
                        abandon_num += 1
                        continue
                    else:  # 保留，重新计算索引
                        temp = cls_id
                        for num in abandon_classes:
                            if num < temp:
                                cls_id -= 1
                            else:
                                break

                    xmlbox = obj.find('bndbox')
                    b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
                         float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))  # voc格式坐标
                    bb = self.convert((w, h), b)  # voc格式坐标 -> YOLO格式坐标
                    out_file.write(str(cls_id) + " " + " ".join(
                        [str(a) for a in bb]) + '\n')  # <class_label> <x_center> <y_center> <width> <height>
                in_file.close()
                out_file.close()
            if len(abandon_classes) > 0:
                print("    剔除次数：%d" % abandon_num)
            print("    Convert complete!")


    def imagesPathRecord(self, data_list):
        """
        对于每个数据集合，将图片的相对路径保存在 data_list[i] + ".txt"（注：也可以保存绝对路径，但是不利于移植）
        :param data_list: [str(,str)]，需要转化的数据,例如["train", "val"]或者["all"]（注：不支持 "all" 与其它单独组合）
        :return:None
        """
        for data_str in data_list:  # 遍历每个数据集合
            save_path = r"%s/%s.txt" % (self.dataset_path, data_str)  # Saved File Path
            print("\nStar save %s file name, save to %s" % (data_str, save_path))
            record_f = open(save_path, 'w')  # 存放图片路径的文件
            relative_path = './' + self.imagesdir_path[data_str][len(self.dataset_path)+1:] + '/'  # 相对路径
            for name in self.files_name[data_str]:  # 遍历当前数据集合的每一个文件
                image_path = relative_path + name + '.jpg' + '\n'
                record_f.write(image_path)

            record_f.close()
            print("    Save complete!")


    def trainValAllocate(self, ratio):
        """
        将数据集划分为训练集(ratio*0.1)和验证集((1-ratio)*0.1)，采用固定间隔抽样的方法进行抽样。
        :param ratio: int，元素值范围[1,9]
        :return:None
        """
        assert "all" in self.files_name.keys(), "Can't allocate!"

        step = int(self.files_num["all"] // ((1-ratio*0.1) * self.files_num["all"]))  # 计算固定间隔抽样的步长
        self.files_name["val"] = self.files_name["all"][::step]  # 按照步长抽取验证集
        self.files_name["train"] = [name for name in self.files_name["all"] if name not in self.files_name["val"]]  # 从原列表中删除已经抽取的元素，得到训练集
        self.files_num["val"] = len(self.files_name["val"])  # 验证集数量
        self.files_num["train"] = len(self.files_name["train"])  # 训练集数量
        self.dataset_num = self.files_num["all"]
        self.imagesdir_path["train"] = self.imagesdir_path["val"] = self.imagesdir_path["all"]
        self.labelsdir_path["train"] = self.labelsdir_path["val"] = self.labelsdir_path["all"]

        del self.files_name["all"]
        del self.files_num["all"]
        del self.imagesdir_path["all"]
        del self.labelsdir_path["all"]

        self.print_dataset()  # 打印数据集信息


    def print_dataset(self):
        """
        打印数据集信息 —— 训练集、验证集和测试集数量
        :return: None
        """
        print("\n数据集模式：%s    数据集图片数量：%d    训练集图片数量：%d    验证集图片数量：%d    测试集图片数量：%d    比例：%.2f:%.2f:%.2f" %
              (self.dataset_mode, self.dataset_num, self.files_num["train"], self.files_num["val"], self.files_num["test"],
               self.files_num["train"] / self.dataset_num, self.files_num["val"] / self.dataset_num, self.files_num["test"] / self.dataset_num))


    def image_clahe(self, imsge_path):
        """
        对单张图片进行 CLAHE 处理。（CLAHE是一种自适应方法，因此它能够在不同区域中提高图像的对比度，而不会过度增强整个图像）
        :param imsge_path: 图片路径
        :return:None
        """
        img = Image.open(imsge_path).convert('RGB')
        img = np.uint8(img)

        imgr = img[:, :, 0]
        imgg = img[:, :, 1]
        imgb = img[:, :, 2]

        claher = cv2.createCLAHE(clipLimit=1, tileGridSize=(8, 8))  # 创建CLAHE算法对象
        claheg = cv2.createCLAHE(clipLimit=1, tileGridSize=(8, 8))
        claheb = cv2.createCLAHE(clipLimit=1, tileGridSize=(8, 8))
        cllr = claher.apply(imgr)  # 对图像进行CLAHE处理
        cllg = claheg.apply(imgg)
        cllb = claheb.apply(imgb)

        rgb_img = np.dstack((cllr, cllg, cllb))

        # plt.subplot(1, 2, 1), plt.imshow(img)
        # plt.title('原图'), plt.axis('off')
        # plt.subplot(1, 2, 2), plt.imshow(rgb_img)
        # plt.title('Clahe'), plt.axis('off')
        # plt.show()

        # 显示原始图像和CLAHE处理后的图像
        cv2.imshow('Input Image', img)
        cv2.imshow('CLAHE Image', rgb_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def returnImagesSize(self, data_list):
        pass



#####################################################################################################################
# VOCInit 模式 （对数据集进行划分成训练集、验证集）
# dataset_path = r"S:\code\python\educateWork"  # 数据集的主目录
# imagesdir_path = {"all": r"S:\code\python\educateWork\images"}  # 图片文件夹的绝对路径
# labelsdir_path = {"all": r"S:\code\python\educateWork\Annotations"}  # 标签文件夹的绝对路径
# dataset_classes = ['holothurian', 'echinus', 'scallop', 'starfish', 'waterweeds']  # 类别名称列表(非索引值)
# zj_dataset = DatasetProcess(dataset_path, dataset_classes, imagesdir_path, labelsdir_path)
# zj_dataset.trainValAllocate(8)  # 训练集 : 验证集 -> 0.80:0.20
# zj_dataset.xmlConvertTxt(["train", "val"])  # VOC -> YOLO
# zj_dataset.imagesPathRecord(["train", "val"])  # 将图片路径保存在txt文件
#####################################################################################################################

#####################################################################################################################
# VOCInit 模式 （单独对测试集进行的操作）
dataset_path = r"S:\code\python\educateWork"  # 数据集的主目录
imagesdir_path = {"all": r"S:\code\python\datasets\zj-dataset\train\images"}  # 图片文件夹的绝对路径
labelsdir_path = {"all": r"S:\code\python\datasets\zj-dataset\train\Annotations"}  # 标签文件夹的绝对路径
dataset_classes = ['holothurian', 'echinus', 'scallop', 'starfish', 'waterweeds']  # 类别名称列表(非索引值)
zj_dataset = DatasetProcess(dataset_path, dataset_classes, imagesdir_path, labelsdir_path)

# zj_dataset.xmlConvertTxt(["all"], save_dir="test_label_txt")  # VOC -> YOLO
zj_dataset.xmlConvertTxt(["all"], abandon_classes=['waterweeds'], save_dir="labels-del")  # VOC -> YOLO and del_classes

zj_dataset.imagesPathRecord(["all"])  # 将图片路径保存在txt文件
#####################################################################################################################

#####################################################################################################################
# VOCandYOLOv5 模式  （必须提供训练集和验证集的txt文件，测试集可以没有，若有必须也是txt文件）
# dataset_path = r"S:\code\python\educateWork"  # 数据集的主目录
# imagesdir_path = {"train": r"S:\code\python\educateWork\train.txt",
#                   "val": r"S:\code\python\educateWork\val.txt",
#                   "test": r"S:\code\python\educateWork\test.txt"}  # 图片文件夹(或图片路径集合的txt文件)的绝对路径
# labelsdir_path = {"train": r"S:\code\python\educateWork\Annotations",
#                   "val": r"S:\code\python\educateWork\Annotations",
#                   "test": r"S:\code\python\educateWork\test-A-labels"}  # 标签文件夹的绝对路径
# dataset_classes = ['holothurian', 'echinus', 'scallop', 'starfish', 'waterweeds']  # 类别名称列表(非索引值)
# zj_dataset = DatasetProcess(dataset_path, dataset_classes, imagesdir_path, labelsdir_path)
# zj_dataset.xmlConvertTxt(["train", "val"], abandon_classes=["waterweeds"], save_dir="del")
#####################################################################################################################

