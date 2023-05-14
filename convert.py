import os
import re

def formalize():
    # 文件夹路径
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
            # 如果新文件名和旧文件名不相同，则进行重命名操作
            if old_path != new_path:
                # 如果新文件名已经存在，则删除原文件
                if os.path.exists(new_path):
                    os.remove(new_path)
                os.rename(old_path, new_path)

def add_pdf():

    # 文件夹路径
    folder_path = r"C:\Users\LZJ\OneDrive\学习\py_ass\pdf"

    # 遍历文件夹下所有文件
    for file_name in os.listdir(folder_path):
        # 获取文件路径
        old_path = os.path.join(folder_path, file_name)
        # 如果文件没有.pdf后缀，则进行重命名操作
        if not file_name.endswith(".pdf"):
            new_path = old_path + ".pdf"
            os.rename(old_path, new_path)

def unify():
    folder_path = r"C:\Users\LZJ\OneDrive\学习\py_ass\pdf"

    # 遍历文件夹下所有文件
    for file_name in os.listdir(folder_path):
        # 判断文件是否为PDF格式
        if file_name.endswith(".pdf"):
            # 使用正则表达式获取文件名中的公司代码和年份信息
            match = re.search(r"(\d{6,})[^\d]*(20\d{2})[^\d]*", file_name)
            if match:
                company_code = match.group(1)
                year = match.group(2)
                # 生成新文件名并进行重命名操作
                new_file_name = "{}-{}.pdf".format(company_code, year)
                old_path = os.path.join(folder_path, file_name)
                new_path = os.path.join(folder_path, new_file_name)
                if old_path != new_path:
                    if os.path.exists(new_path):
                        os.remove(new_path)
                    os.rename(old_path, new_path)

if __name__ == "__main__":
    unify()
    print("over")