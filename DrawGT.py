# -*- coding: UTF-8 -*-
# 开发人员  ：Chen
# 开发时间  ：2023/4/16 12:21
# 开发名称  ：DrawGT.py
# 开发工具  ：PyCharm
# 描述      ：在图像上绘制标签文件中的检测框并保存处理后的图像
# 备注      ：YOLO-txt格式的标签文件

import os
import tqdm
import cv2

# 设置处理后图像的保存路径
save_path = "./imagesGT/"

def main():
    # 定义图像和标签文件的根目录
    path_root_imgs = 'images'  # 图像文件夹
    path_root_labels = '../datasets/zj-dataset/test-A/labels'  # 标签文件夹
    type_object = '.txt'  # 标签文件的扩展名

    # 如果保存路径不存在，则创建
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # 遍历图像文件夹
    for ii in os.walk(path_root_imgs):
        # ii[2]是当前目录下的所有文件列表
        for j in tqdm.tqdm(ii[2]):
            # 检查文件类型是否为 jpg，不是则跳过
            type = j.split(".")[1]
            if type != 'jpg':
                continue

            # 获取当前图像的完整路径
            path_img = os.path.join(path_root_imgs, j)
            label_name = j[:-4] + type_object  # 生成对应的标签文件名
            save_name = j[:-4]  # 设置保存文件名
            path_label = os.path.join(path_root_labels, label_name)  # 标签文件的完整路径

            # 打开标签文件（如果存在）
            if os.path.exists(path_label):
                f = open(path_label, 'r+', encoding='utf-8')

                # 读取图像数据
                img = cv2.imread(path_img)
                w, h = img.shape[1], img.shape[0]  # 获取图像宽度和高度
                img_tmp = img.copy()  # 创建图像副本用于绘制框

                # 逐行读取标签文件内容，处理每个物体的边框信息
                while True:
                    line = f.readline()
                    if line:
                        msg = line.split(" ")
                        # 根据标签文件计算边框的左上角和右下角坐标
                        x1 = int((float(msg[1]) - float(msg[3]) / 2) * w)  # x_center - width/2
                        y1 = int((float(msg[2]) - float(msg[4]) / 2) * h)  # y_center - height/2
                        x2 = int((float(msg[1]) + float(msg[3]) / 2) * w)  # x_center + width/2
                        y2 = int((float(msg[2]) + float(msg[4]) / 2) * h)  # y_center + height/2

                        # 在图像上绘制矩形框，颜色为绿色，线宽为15
                        cv2.rectangle(img_tmp, (x1, y1), (x2, y2), (0, 255, 0), 15)
                    else:
                        break  # 文件读取完毕，跳出循环

                # 保存带有检测框的图像到指定目录
                cv2.imwrite(save_path + save_name + '.jpg', img_tmp)

    print("Complete!")  # 完成所有操作后输出提示

# 程序入口
if __name__ == '__main__':
    main()

