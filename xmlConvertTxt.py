# -*- coding: UTF-8 -*-
# 开发人员  ：Chen
# 开发时间  ：2023/3/8 14:13
# 开发名称  ：xmlConvertTxt.py
# 开发工具  ：PyCharm
#   描述   ：将 imagespath 文件夹里的 xml 转化为 txt，并保存在 save_dir 文件夹里

# os.listdir() 方法用于返回指定的文件夹包含的文件或文件夹的名字的列表。

# range(stop)：生成从 0 到 stop-1 的整数序列。

# open(file, mode='r') 方法用于打开一个文件，并返回文件对象。 注意：使用 open() 方法一定要保证关闭文件对象，即调用 close() 类方法。
# file.write(str) 将字符串写入文件，返回的是写入的字符长度。
# file.read([size])：从文件读取指定的字节数，如果未给定或为负则读取所有。

# os.path.exists(path)	路径存在则返回True,路径损坏返回False

# os.makedirs(path[, mode]) 方法用于创建一个名为path的文件夹。

# 字符串类的类函数：
# str.strip([chars]) 方法用于移除字符串头尾指定的字符（默认为空格）或字符序列。
# str.split(str="", num=string.count(str))   以 str 为分隔符[默认为所有的空字符，包括空格、换行(\n)、制表符(\t)等]截取字符串，如果 num 有指定值(默认为 -1, 即分隔所有。)，则仅截取 num+1 个子字符串。

# python操作xml——ElementTree(元素树)方式：https://blog.csdn.net/m0_37857151/article/details/84037148
import os
f = open(r"S:\code\python\educateWork\del.txt", 'w')
print(os.path.abspath(f.name))