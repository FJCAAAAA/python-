#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : file_writte.py
@Author: Fengjicheng
@Date  : 2019/8/24
@Desc  :
'''
def file_write(file_name,content):
    if content:
        if type(content) == list:
            for i in content:
                with open(file_name,'a',encoding='utf-8') as f:
                    f.write(i + '\n')
        if type(content) ==  str:
            with open(file_name, 'a', encoding='utf-8') as f:
                f.write(content)
    else:
        print(content,"内容为空，跳过")
        pass