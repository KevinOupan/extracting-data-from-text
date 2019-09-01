import jieba
import re
import xlrd
import pandas as pd
import numpy as np


class brandd:
    """提取品牌名"""
    def __init__(self, addr):
        self.addr = addr

    def contain_let(self, string):
        """判断字符串string中包含字母"""
        return bool(re.search('[A-z]', string))

    def contain_chin(self, string):
        """判断字符串string中是否包含汉字"""
        zhmodel = re.compile(u'[\u4e00-\u9fa5]')
        match = zhmodel.search(string)
        if match:
            boolValue = True
        else:
            boolValue = False
        return boolValue

    def read_in_1(self, addr_in):
        """从excel文件中读取数据
        addr_in为缺失的csv文件地址"""
        datafile = xlrd.open_workbook(addr_in)
        table = datafile.sheets()[0]
        matrix_text = pd.DataFrame([])
        for i in range(table.ncols):
            matrix_text[i] = table.col_values(i)
        matrix_text.rename(columns=matrix_text.iloc[0, :], inplace=True)
        matrix_text.drop([0], axis=0, inplace=True)
        type_nonstand = matrix_text[['BAND_NAME']]  # 匹配的非标准数据
        BrandName_data = []
        for i in range(len(type_nonstand)):
            string_sin = jieba.cut(type_nonstand.iloc[i, 0])
            for string in string_sin:
                if self.contain_let(string) or self.contain_chin(string):
                    BrandName_data.append(string)
        return list(set(BrandName_data))

    def runing(self):
        brandname = self.read_in_1(self.addr)
        return brandname
