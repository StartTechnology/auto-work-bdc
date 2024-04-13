import os
import shutil
import time
import math
import re
from rapidocr_onnxruntime import RapidOCR


img_path=r"C:\Users\LCY\AppData\Roaming\SPB_Data\gitee\auto-work\文档及测试数据\彭祥华 刘冬风\IMG_0003.jpg"
img_path1=r"C:\Users\LCY\AppData\Roaming\SPB_Data\gitee\auto-work\文档及测试数据\李萍华 刘为龙\IMG_0004.jpg"
img_path2=r"C:\Users\LCY\AppData\Roaming\SPB_Data\gitee\auto-work\文档及测试数据\郭丽华 刘桂根\IMG_0004.jpg"
class Person:
    def __init__(self, name, ID):

        if len(str.split(name," "))>1:
            self.name=str.split(name," ")[-1]
        else:
            self.name=name.replace("姓名","")
        if len(str.split(ID," "))>1:
            self.ID=str.split(ID," ")[-1]
        elif len(str.split(ID,"："))>1:
            self.ID=str.split(ID,"：")[-1]
        else:
            self.ID=ID
        # self.name = name

    def __str__(self):
        return f"Name: {self.name}, ID: {self.ID}"

def OCRImg(img_path):
    engine = RapidOCR()
    result, elapse = engine(img_path)
    return result

#从OCR结果找到含有字符串的行
def find_string(result, string):
    str_list=[]
    for i in range(0,len(result)):
        if string in result[i][1]:
            str_list.append(i)
    return str_list

#姓名查找 找到"民族"行[0]，找到最近的坐标[3] 3 0
#从OCR结果找与身份号码[2]最近的坐标[1],并返回行号
#查找客户姓名特有内部方法
def find_nearest_coordinate(result, res_str_index,point1,point2):
    index=0
    value=9999999
    for i in range(0,len(result)):
        if i == res_str_index:
            continue
        else:
            _dist=math.dist(result[i][0][point1],result[res_str_index][0][point2])
            if _dist<value and len(result[i][1])<6:
                index=i
                value=_dist
            pass
    return index

#查找身份证号 
def find_ID_index(result):
    id_list=[]
    _str_list=find_string(result, "身份号码")

    for i in _str_list:
        if len(result[i][1].split("："))>1:
            _id=result[i][1].split("：")[-1]
            _id=re.sub("[Xx]", "", _id)
            if _id.isdigit():
                id_list.append(i)
        elif len(result[i][1].split(" "))>1:
            _id=result[i][1].split(" ")[-1]
            _id=re.sub("[Xx]", "", _id)
            if _id.isdigit():
                id_list.append(i)

    for i in range(0,len(result)):
        _str=result[i][1]
        _str=re.sub("[Xx]", "", _str)
        if _str.isdigit():
            id_list.append(i)
    return id_list

#查找姓名行号
def find_name_index(result):
    str_list=find_string(result, "民族")
    _index=[]
    for i in str_list:
        _index.append(find_nearest_coordinate(result, i,3,0))
    return _index

#0,3
# for i in range(0,4):
#     #_i=find_nearest_coordinate(result, 20, i, 0)
#     _i=find_nearest_coordinate(result, 0, i, 0)
#     print(i,result[_i][1])
result=OCRImg(img_path)

def getPersons(result):
    _persons=[]
    str_list_id=find_ID_index(result)
    str_list_name=find_name_index(result)
    if len(str_list_name) != len(str_list_id):
        return []
    else:
        for _n_i in str_list_name:
            distanct=9999999
            _i=0
            for _i_i in str_list_id:
                _dist=math.dist(result[_n_i][0][0],result[_i_i][0][0])
                if _dist<distanct:
                    distanct=_dist
                    _i=_i_i
            _persons.append(Person(result[_n_i][1],result[_i][1]))
    return _persons

persons=getPersons(result)
for i in persons:
    print(i)

# print(time.strftime("%Y%m%d", time.localtime()))