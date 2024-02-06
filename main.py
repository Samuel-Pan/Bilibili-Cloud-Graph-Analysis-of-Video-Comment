import requests
import csv
import json
from datetime import datetime
import os
import pandas as pd

# 爬取评论信息
def get_comments(oid, max_page):
    comments = []
    # 循环，爬取每一页的评论
    for page in range(1, max_page+1):
        url = "https://api.bilibili.com/x/v2/reply/main"
        params = {
                    'mode': '3',  #mode=3代表按热门排序，mode=2代表按时间排序
                    'oid': oid,
                    'next': page,
                    'type': '1',
            }
        headers = {
            "User-Agent": " "   # 复制User-Agent
        }
        # 请求网页
        response = requests.get(url,params=params,headers=headers)
        data = response.text
        # 解析网页，以json格式
        result = json.loads(data)
        # 遍历每一条评论，获取评论者、评论时间、评论内容、点赞数
        for c in result['data']['replies']:
            member = c['member']['uname']   # 评论者
            ctime = datetime.fromtimestamp(c['ctime'])  # 评论时间，需要使用fromtimestamp转换时间戳
            content = c['content']['message']  # 评论内容
            like = c['like']   # 点赞数
            # 将每一条评论的信息存入列表
            comments.append([member, ctime, content, like])
        # 每爬取10页，打印提示信息
        if page%10==0:
            print(f"已经爬取{page}页")
    return comments

# 保存到csv文件
def save_to_csv(filename, comments):
    with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
        # 创建csv文件的写入对象
        writer = csv.writer(file)
        # 写入表头
        writer.writerow(['评论者', '评论时间', '评论内容','点赞数'])
        # 写入数据
        writer.writerows(comments)
    print("CSV文件成功写入")

#数据清洗，去重
def clean_data(filename):
    # 读取csv文件
    df = pd.read_csv(filename, encoding='utf-8-sig')
    # 删除原文件
    os.remove(filename)
    # 删除重复数据
    df.drop_duplicates(subset='评论内容', inplace=True, keep='first')
    # 重新写入文件
    column=header = ['评论者', '评论时间', '评论内容','点赞数']
    df.to_csv(filename, mode='a+', index=False, columns=column,header=header, encoding='utf-8-sig')
    print('数据清洗完成')

if __name__ == '__main__':
    oid = " "   # B站视频的id号
    max_page = 250    # 爬取评论的最大页数
    filename = 'comments.csv'   # 保存的csv文件名
    # 爬取评论信息
    comments = get_comments(oid, max_page)
    # 保存到csv文件
    save_to_csv(filename, comments)
    # 数据清洗
    clean_data(filename)
