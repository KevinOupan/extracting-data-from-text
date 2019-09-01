from product_type_extract import *
from brand_name import brandd
"""主程序：
address_in为输入数据的地址
address_out为输出数据的地址
注:输入数据的含型号的文本数据列的列名为‘NAME123’
"""
address_in = '0731复印机（原数据-标准值）.xlsx'
address_out = '7777445type_pro_standard.csv'
data = read_in(address_in)
type_pro = []
print("型号提取中。。。")
address_in2 = '1122京东平安0812.xlsx'
model1 = brandd(address_in2)
brandname = model1.runing()
# print('brandname', brandname)

for i in range(len(data)):
    model = Extract(str(data[i]), brandname)
    type_single = model.runing()
    type_pro.append(type_single)
    print(type_single)

print('提取的型号数据：', type_pro)
out_data(type_pro, address_out)
print("提取结束！！！")
