import jieba
import re
import xlrd
import pandas as pd
import numpy as np


class Extract:
    def __init__(self, string_non, BrandName):
        self.string_non = string_non
        self.BrandName = BrandName

    def contain_num(self, string):
        """判断字符串string中包含数字"""
        return bool(re.search('[0-9]', string))

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

    def contain_sym(self, string):
        """判断字符串string中包含'+'和'-'"""
        return bool(re.search('[-+]', string))

    def select_num(self, string):
        """挑选字符串中的数字"""
        num = re.findall(r"\d+\.?\d*", string)
        return num[0]

    def seek_type_maybe(self, str_single):
        """挑选可能的型号字符串"""
        str_goal = jieba.cut(str_single)
        word_goal = ""
        for word in str_goal:
            word_goal += word + " "
        sym = ('＋', '；', '：', '（', '(', ')', '）', "，", ',', '【', '】')
        word_goal = ''.join(c for c in word_goal if c not in sym)  # 去掉标点符号
        vec = word_goal.split()
        type_maybe = {}
        for i in range(len(vec)):
            if vec[i] == '-':
                type_maybe[i] = vec[i - 1] + '-' + vec[i + 1]
            elif vec[i] == '+':
                type_maybe[i] = vec[i - 1] + '+' + vec[i + 1]
            else:
                type_maybe[i] = vec[i]
        return type_maybe

    def select_one(self, type_in):
        """挑选含数字的字符串
        type_in数据类型为字典"""
        type_out = {}
        for key in type_in:
            if self.contain_num(type_in[key]):
                type_out[key] = type_in[key]
        return type_out

    def select_two(self, type_in):
        """挑选含字符串长度在三到十
        type_in数据类型为字典"""
        type_out = {}
        for key in type_in:
            if (len(type_in[key]) >= 3)and(len(type_in[key]) <= 10):
                type_out[key] = type_in[key]
        return type_out

    def select_three(self, type_in, type_st):
        """挑选品牌名后面的字符串
        返回的是一个值"""
        type_out = []
        for key in type_in:
            index = key
            if index == 1:
                if type_st[index-1] in self.BrandName:
                    type_out = type_in[key]
                    break
            elif index >= 2:
                if (type_st[index - 1] in self.BrandName)and(type_st[index - 2] in self.BrandName):
                    type_out = type_in[key]
                    break
        return type_out

    def select_four(self, type_in, type_st):
        """挑选型号后面的字符串"""
        type_product = []
        for i in range(1, len(type_in)):
            index = list(type_in.items())[i][0]
            if (type_st[index - 1] == '型号')and(type_st[index - 2] == '型号'):
                type_product.append(type_st[i])
        return list(set(type_product))

    def select_five(self, type_mul):
        """挑选带有'+'或者'-'的字符串"""
        type_sin = []
        for key in type_mul:
            if self.contain_sym(type_mul[key]):
                type_sin.append(type_mul[key])  # 可能有多个带有'+'或者'-'的可能型号
                break
        return type_sin

    def select_six(self, type_mul):
        """根据数字挑选字符串（重复的数字或者数字较多的字符串）"""
        type_select = []
        if len(type_mul) >= 2:
            for key_i in type_mul:
                for key_j in type_mul:
                    num_i = self.select_num(type_mul[key_i])
                    num_j = self.select_num(type_mul[key_j])
                    if num_i == num_j and key_i != key_j and len(type_mul[key_i]) >= len(type_mul[key_j]):
                        type_select = type_mul[key_j]
                        # break
                    else:
                        type_len = {}
                        for key in type_mul:
                            type_len[key] = self.select_num(type_mul[key])
                        index_max = max(type_len, key=type_len.get)
                        type_select = type_mul[index_max]
                        # type_select = type_mul
        return type_select

    def runing(self):
        global type_final_out
        output1 = self.seek_type_maybe(self.string_non)           # 字符串分词，挑选可能的型号
        output2 = self.select_one(output1)               # 挑选含数字的字符串
        output3 = self.select_two(output2)               # 挑选长度在三到十的字符串
        if len(output3) == 1:
            type_final = list(output3.items())[0][1]
        else:
            output4 = self.select_three(output3, output1)  # 挑选品牌名后面的字符串
            if len(output4) == 1:
                type_final = output4
            else:
                output5 = self.select_five(output3)          # 挑选带有'+'或者'-'的字符串
                if len(output5) == 1:
                    type_final = output5
                else:
                    output6 = self.select_four(output3, output1)      # 挑选型号后面的字符串
                    if len(output6) == 1:
                        type_final = output6
                    else:
                        output7 = self.select_six(output3)
                        if len(output7) == 1:
                            type_final = output7
                        else:
                            type_final =output3
        if len(type_final) == 0:
            type_final_out = 'na'
        elif type(type_final) == str:
            type_final_out = type_final
        elif len(type_final) == 1 and type(type_final) == list:
            type_final_out = type_final[0]
        elif len(type_final) == 1 and type(type_final) == dict:
            type_final_out = list(type_final.items())[0][1]
        elif len(type_final) >= 2 and type(type_final) == dict:
            type_len = {}
            for key in type_final:
                type_len[key] = len(type_final[key])
            index = max(type_len, key=type_len.get)
            type_final_out = type_final[index]
        return type_final_out


def read_in(addr_in):
    """从excel文件中读取数据
    addr_in为缺失的csv文件地址"""
    datafile = xlrd.open_workbook(addr_in)
    table = datafile.sheets()[0]
    matrix_text = pd.DataFrame([])
    for i in range(table.ncols):
        matrix_text[i] = table.col_values(i)
    matrix_text.rename(columns=matrix_text.iloc[0, :], inplace=True)
    matrix_text.drop([0], axis=0, inplace=True)
    type_nonstand = matrix_text[['产品型号（原）']]  # 匹配的非标准数据
    return list(np.array(type_nonstand))


def out_data(data, addr):
    columns = 'product_type'
    data.insert(0, columns)
    pd.DataFrame(data).to_csv(addr, index=0)
