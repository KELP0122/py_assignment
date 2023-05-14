# 考虑到时间和算力限制，在文本分析方法这里本项目采用常老师提供的样本文本进行分析

import pandas as pd
import numpy as np
import os
import re
import jieba
from nltk import FreqDist
from collections import Counter
from matplotlib import pyplot as plt

# 定义一个包含描述极端天气的词典
dict_weather = {
    '高温', '海平面上升', '洪水', '干旱','天气','恶劣',
    '雨','雪','风','雷','雾','沙尘','沙尘暴','雾霾','霾',
    '温','湿','冷','阴','高温','低温','影响','冲击'
    }
# dict_weather = {"防疫","疫情","新冠","covid","病毒","肺炎","疫"}

# 从文件中加载 pandas dataframe
df = pd.read_excel(r"C:\Users\LZJ\OneDrive\学习\py_ass\data\sample.xlsx")

# 使用 str.contains() 方法筛选出包含在词典中的文本
df["body"] = df["body"].str.replace('[^\u4e00-\u9fa5]+', '')  # 删除非汉字项
df['sep'] = df['body'].apply(lambda x: ' '.join(jieba.cut(x)))  # 使用jieba库进行分词
mask = df['body'].str.contains('|'.join(dict_weather), case=False)
filtered_df = df.loc[mask, ['stkcd', 'year', 'body']]

# 将包含词典中关键字的所有文本进行拼接，并使用 Counter 类进行词频统计
text = ' '.join(filtered_df['body']).lower()
word_count = Counter(text.split())

word_count_list = []
for text in df['sep']:
    word_count = Counter(text.split())
    word_count_dict = {word: count for word, count in word_count.items() if word in dict_weather}
    word_count_sum = sum(word_count.values())
    word_count_list.append(word_count_dict)

df['word_count'] = word_count_list
df['word_count_sum'] = pd.Series(word_count_list)

def dict2int(d):
    return sum(d.values())
df['word_count_sum'] = df['word_count_sum'].apply(dict2int)

# 打印词频统计结果
print(df[["stkcd","year","word_count_sum"]])
df.to_excel(r"C:\Users\LZJ\OneDrive\学习\py_ass\data\sample整合词频.xlsx")

bins = 50
range_min = df['word_count_sum'].min()
range_max = df['word_count_sum'].max()
# range_max = 10
range_step = (range_max - range_min) / bins
n, bins, patches = plt.hist(df['word_count_sum'], bins=bins, range=(range_min, range_max + range_step), alpha=1)
plt.xlabel('Number of words in dict occurred')
plt.ylabel('Frequency')
plt.title('Histogram of word_count_sum')

for i in range(len(patches)):
    x = patches[i].get_x() + patches[i].get_width() / 2
    y = patches[i].get_height()
    if n[i]>0:
        plt.text(x, y, str(int(n[i])), ha='center', va='bottom')
plt.show()


# 明细词频
df = pd.read_excel(r"C:\Users\LZJ\OneDrive\学习\py_ass\data\sample.xlsx")

def clean_text(text):
    # 删除非汉字项
    return re.sub('[^\u4e00-\u9fa5]+', '', text)

# 对“年报正文”列进行数据清洗和中文分词
df['body'] = df['body'].apply(lambda x: clean_text(x))
df['sep'] = df['body'].apply(lambda x: jieba.lcut(x))

# 词频统计函数
def count_words(text, dict_list):
    # 构造一个字典，键为词汇，值为该词汇出现的次数
    word_count = {}
    for word in text:
        if word in dict_list:
            if word not in word_count:
                word_count[word] = 1
            else:
                word_count[word] += 1
    # 返回每个词汇出现的频率
    total_count = sum(word_count.values())
    freq_dict = {}
    for word in word_count:
        # 计算组内相对频率
        freq_dict[f'{word}'] = word_count[word] / total_count
        # 计算绝对频率
        freq_dict[f'{word}'] = word_count[word]
    return freq_dict

# 对“分词结果”列进行词频统计，将结果添加到数据框的最右侧
freq_df = pd.DataFrame(df['sep'].apply(lambda x: count_words(x, dict_weather)).tolist())
df = pd.concat([df, freq_df], axis=1)

df.to_excel(r"C:\Users\LZJ\OneDrive\学习\py_ass\data\sample明细词频.xlsx")
print("over")