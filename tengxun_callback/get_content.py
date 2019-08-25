#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : get_content.py
@Author: Fengjicheng
@Date  : 2019/8/24
@Desc  :
'''
import requests
import re
import random
import time
import json
import jieba
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.font_manager as fmgr
from wordcloud import WordCloud
from common import user_agent
from common import my_fanction

#词云形状图片
img1 = 'lib/fangxing.png'
img2 = 'lib/xin.png'
#词云字体
font = 'lib/simsun.ttc'
#评论请求地址
url = 'http://coral.qq.com/article/4093121984/comment/v2'
agent = random.choice(user_agent.user_agent_list)
header = {
'Host': 'video.coral.qq.com',
'User-Agent': agent,
'Accept': '*/*',
'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
'Accept-Encoding': 'gzip, deflate, br',
'Connection': 'keep-alive',
'Referer': 'https://page.coral.qq.com/coralpage/comment/video.html',
'TE': 'Trailers'
}
# 第一页
cursor = '0'
vid = 1566724116229

def get_comment(a,b):
    parameter = {
    'callback':	'_varticle4093121984commentv2',
    'orinum': '10',
    'oriorder':	'o',
    'pageflag':	'1',
    'cursor': a,
    'scorecursor': '0',
    'orirepnum': '2',
    'reporder':	'o',
    'reppageflag': '1',
    'source': '1',
    '_': str(b)
    }
    try:
        html = requests.get(url,params=parameter,headers=header)
    except Exception as e:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"请求失败。",e)
    else:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"请求成功。")
    content = html.content.decode('utf-8')
    sep1 = '"last":"(.*?)"' # 下一个 cursor
    sep2 = '"content":"(.*?)"' # 评论
    sep3 = '"nick":"(.*?)"' # 昵称
    sep4 = '"region":"(.*?)"' # 地区
    global cursor
    cursor = re.compile(sep1).findall(content)[0]
    comment = re.compile(sep2).findall(content)
    nick = re.compile(sep3).findall(content)
    region = re.compile(sep4).findall(content)
    my_fanction.file_write('txt/comment.txt',comment)
    my_fanction.file_write('txt/nick.txt',nick)
    my_fanction.file_write('txt/region.txt',region)

def cut_word(file_path):
    with open(file_path,'r',encoding='utf-8') as f:
        comment_txt = f.read()
        wordlist = jieba.cut(comment_txt, cut_all=True)
        wl = " ".join(wordlist)
        print(wl)
        return wl #返回分词后的数据

def create_word_cloud(file_path,img):
    # 设置词云形状图片
    wc_mask = np.array(Image.open(img))
    # 设置词云的一些配置，如：字体，背景色，词云形状，大小
    wc = WordCloud(background_color="white", max_words=200, mask=wc_mask, scale=4,
                   max_font_size=50, random_state=42, font_path=font)
    # 生成词云
    wc.generate(cut_word(file_path))
    # 在只设置mask的情况下,你将会得到一个拥有图片形状的词云
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    #plt.figure()
    plt.show()

def create_region_histogram():
    with open('txt/region.txt','r',encoding='utf-8') as f:
        country_list = f.readlines()
        country_list = [x.strip() for x in country_list if x.strip() != '::']
    sep1 = ':'
    pattern1 = re.compile(sep1)
    province_lit = []
    province_count = []
    other_list = []
    other_count = []
    for country in country_list:
        country_detail = re.split(pattern1,country)
        if '中国' in country_detail:
            if country_detail[1] != '':
                province_lit.append(country_detail[1])
        else:
            other_list.append(country_detail[0])
    province_uniq = list(set(province_lit))
    other_uniq = list(set(other_list))
    for i in province_uniq:
        province_count.append(province_lit.count(i))
    for i in other_uniq:
        other_count.append(other_list.count(i))
    # 构建数据
    x_data = province_uniq
    y_data = province_count
    # 自定义字体属性
    fp = fmgr.FontProperties(fname='lib/simsun.ttc')
    bar_width = 0.7
    # Y轴数据使用range(len(x_data)
    plt.barh(y=range(len(x_data)), width=y_data, label='count',
             color='steelblue', alpha=0.8, height=bar_width)
    # 在柱状图上显示具体数值, ha参数控制水平对齐方式, va控制垂直对齐方式
    for y, x in enumerate(y_data):
        plt.text(x+10, y - bar_width / 2, '%s' % x, ha='center', va='bottom')
    # 为Y轴设置刻度值
    plt.yticks(np.arange(len(x_data)) + bar_width / 2, x_data,fontproperties=fp)
    # 设置标题
    plt.title("各地区参与评论用户量",fontproperties=fp)
    # 为两条坐标轴设置名称
    plt.xlabel("人数",fontproperties=fp)
    plt.ylabel("地区",fontproperties=fp)
    # 显示图例
    plt.legend()
    plt.show()


if __name__ == "__main__":
    # 爬取数据
    get_comment(cursor, vid)
    for i in range(1, 1000):
        vid = vid + i
        get_comment(cursor, vid)
        time.sleep(1)
    # 生成词云
    create_word_cloud('txt/comment.txt',img2)
    create_word_cloud('txt/nick.txt', img1)
    # 生成柱状图
    create_region_histogram()
