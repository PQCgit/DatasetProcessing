# -*- coding: UTF-8 -*-
# 开发人员  ：Chen
# 开发时间  ：2023/3/25 20:16
# 开发名称  ：test_del.py
# 开发工具  ：PyCharm
#   描述   ：



import os

file_path = '/path/to/filename.txt'
filename, extension = os.path.splitext(file_path)
full_file_path = os.path.join('/path/to', filename+extension)

print(full_file_path)   # 输出: /path/to/filename.txt

1