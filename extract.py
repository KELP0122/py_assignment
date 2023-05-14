import pandas as pd
import os
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import *
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage,PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter

def get_data(iloc):
    df["rep_period"] = pd.to_datetime(df["rep_period"])
    df['year'] = df['rep_period'].dt.year
    firm = df.at[iloc,'security_name'].replace("*","") # 去掉*ST的*号
    code = df.at[iloc,'security_code']
    year = df.at[iloc,'year']
    return firm,code,year

def load_pdf(code, firm,year):
    file_path = r"C:\Users\LZJ\OneDrive\学习\py_ass\pdf"
    # file_path = r":\Users\Think\OneDrive\学习\py_ass\pdf"
    file_name = "{}-{}".format(code,year)
    pdf_path = os.path.join(file_path,file_name)
    return pdf_path

def parsePDF(pdf_path,txt_path):
    # 以二进制读模式打开pdf文档
    fp = open(pdf_path,'rb')

    # 用文件对象来创建一个pdf文档分析器
    parser = PDFParser(fp)

    # pdf文档的对象，与分析器连接起来
    doc = PDFDocument(parser=parser)
    parser.set_document(doc=doc)

    # 如果是加密pdf，则输入密码，新版好像没有这个属性
    # doc._initialize_password()

    # 创建pdf资源管理器 来管理共享资源
    resource = PDFResourceManager()

    # 参数分析器
    laparam=LAParams()

    # 创建一个聚合器
    device = PDFPageAggregator(resource,laparams=laparam)

    # 创建pdf页面解释器
    interpreter = PDFPageInterpreter(resource,device)
    
    # 用来计数页面，图片，曲线，figure，水平文本框等对象的数量
    num_page, num_image, num_curve, num_figure, num_TextBoxHorizontal = 0, 0, 0, 0, 0

    # 获取页面的集合
    for page in PDFPage.get_pages(fp):
        num_page += 1  # 页面增一
        # 使用页面解释器来读取
        interpreter.process_page(page)

        # 使用聚合器来获取内容
        layout = device.get_result()
        # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
        for x in layout:
            if isinstance(x,LTImage):  # 图片对象
                num_image += 1
            if isinstance(x,LTCurve):  # 曲线对象
                num_curve += 1
            if isinstance(x,LTFigure):  # figure对象
                num_figure += 1
            if isinstance(x, LTTextBoxHorizontal):  # 获取文本内容
                num_TextBoxHorizontal += 1  # 水平文本框对象增一
                    # 保存文本内容
                with open(txt_path, 'a',encoding='UTF-8',errors='ignore') as f:
                    results = x.get_text()
                    print(results,end='')
                    f.write(results + '\n')
        print('对象数量：\n','页面数：%s\n'%num_page,'图片数：%s\n'%num_image,'曲线数：%s\n'%num_curve,'水平文本框：%s\n'%num_TextBoxHorizontal)

if __name__ == "__main__":
    df = pd.read_excel(r"C:\Users\LZJ\OneDrive\学习\py_ass\data\index.xlsx",sheet_name = "sh")
    for iloc in range(1,len(df)+1):
        firm, code, year = get_data(iloc)
        pdf_path = load_pdf(code, firm, year) + ".pdf"
        txt_path = load_pdf(code, firm, year) + ".txt"
        print(pdf_path)
        parsePDF(pdf_path, txt_path)