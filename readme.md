# README
Author: 不含碘的海带

version 1.0

latest update 2023/5/14
## 简介
这是一个上市公司年报文本分析的大作业。

其中src文件夹为源代码
main.py为主代码。目前包含的功能是将pdf中的文本提取进txt文件，以便日后分析。
crawler.py为爬虫
convert为重命名清洗的代码

pdf文件夹中为2019-2022年上海证券交易所上市公司的年报pdf源文件和转换好的txt文件
data文件夹中的index.xlsx为上市公司的代码和公司名清单。

## 工作方向
目前项目并没有开始对文本进行分析。主要障碍在于如下几点：

1. 文本txt数据源还没有跑出来。这个需要一定时间去跑。
2. 对于文本分析的算法还没有确定，我目前的思路是采用两种算法进行分析：
   - 纯粹的词频统计，但是要区分等权重词典和人为设置不同权重词典的结果
   - 文本向量化，从行业聚类出发，采用文本向量化算法进行计算