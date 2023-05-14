import json
import requests
import re
import datetime
import csv 
import os
from convert import formalize

def crawler():
    f=open ('stkcd.csv',mode='w',encoding='gbk',newline='')
    writer = csv.writer(f)
    head=['stkcd']
    writer.writerow(head)
    # 要下载的年报日期可以根据需要调整，开始日期和结束日期间隔最好不要超过30日
    # 下载路劲默认为proj根目录，我手动将pdf源文件移入pdf文件夹，受制于时间限制该部分并没有实现完全自动化作业
    begin = datetime.date(2020,1,1)
    end = datetime.date(2022,12,31)

    for i in range((end - begin).days+1):
        searchDate = str(begin + datetime.timedelta(days=i))
        response=requests.get(
            'http://query.sse.com.cn/infodisplay/queryLatestBulletinNew.do?&jsonCallBack=jsonpCallback43752&productId=&reportType2=DQGG&reportType=YEARLY&beginDate='+searchDate+'&endDate='+searchDate+'&pageHelp.pageSize=25&pageHelp.pageCount=50&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.cacheSize=1&pageHelp.endPage=5&_=1561094157400'
            ,
            headers={'Referer':'http://www.sse.com.cn/disclosure/listedinfo/regular/'}
        )
        json_str = response.text[19:-1]
        data = json.loads(json_str)
        for report in data['result']:
            download_url = 'http://www.sse.com.cn/' + report['URL']
            if re.search('年度报告',report['title'],re.S):
                if re.search('摘要',report['title'],re.S):###避免下载一些年报摘要等不需要的文件###
                    pass
                else:
                    filename = report['security_Code']+report['title'] +searchDate+ '.pdf'
                    print(filename)
                    writer.writerow([report['security_Code']])###将公司代码写进csv文件，便于计数，非必须步骤###
                    if re.search('ST',report['title'],re.S):###下载前要将文件名中带*号的去掉，因为文件命名规则不能带*号，否则程序会中断###
                        filename=report['security_Code']+'-ST' +searchDate+ '.pdf'
                        download_url = 'http://static.sse.com.cn/' + report['URL']
                        resource = requests.get(download_url, stream=True)
                        with open(filename, 'wb') as fd:
                            for y in resource.iter_content(102400):
                                fd.write(y)
                            print(filename, '完成下载')
                    else:
                        download_url = 'http://static.sse.com.cn/' + report['URL']
                        resource = requests.get(download_url, stream=True)
                        with open(filename, 'wb') as fd:
                            for y in resource.iter_content(102400):
                                fd.write(y)
                            print(filename, '完成下载')


    # 指定文件夹路径
    folder_path = r"C:\Users\LZJ\OneDrive\学习\py_ass\pdf"

    # 遍历文件夹下所有文件
    for file_name in os.listdir(folder_path):
        # 判断文件是否为PDF格式
        if file_name.endswith(".pdf"):
            # 获取年度报告位置并去除之后的字符
            new_file_name = re.sub(r"年度报告.*?\.pdf", "年度报告.pdf", file_name)
            # 拼接新文件名和旧文件路径
            old_path = os.path.join(folder_path, file_name)
            new_path = os.path.join(folder_path, new_file_name)
            # 重命名文件
            os.rename(old_path, new_path)

if __name__ == "__main__":
    crawler()
    formalize()