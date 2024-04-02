# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 15:48:01 2024

@author: LCY
"""
import os
import re
import pandas as pd

imagePath = 'F:\\AutoWork\\image\\'



ruls=[['Start','End'],]

# 读取txt文件(绝对路径)
def fileRead(filePath):
    file = open(filePath,'r')
    result=file.readlines()
    file.close()
    return result


# 根据规则提取TXT文件中的列至dataFrame文件中
def getTxtToDataFrame(file,ruls):
    dirname=''
    dataframe=[]
    context=''
    for i in range(0,len(file)):
        if ruls[0][1] not in file[i]:
            if ruls[0][0] in file[i]:
                dirname = file[i].lstrip(ruls[0][0])
                dirname=dirname.rstrip('\n')
                pass
            else:
                context=context+file[i]
                pass
        else:  
            singleData=[dirname]
            _r=re.findall(".*(居民身份证/|信用代码/|信用代码|居民身份证)(.*)(\n).*", context)
            if _r: singleData.append(_r[0][1])
            else:
                singleData.append('')
                pass
            
            _r=re.findall(".*(赣)(.*)(\n).*", context)
            if _r: singleData.append("赣"+_r[0][1])
            else:
                singleData.append('')
            
            _r=re.findall(".*(机动车登记证书编号：|机动车登记证书编号\n|亏编号\n)(.*)(\n).*", context)
            if _r: singleData.append(_r[0][1])
            else:
                singleData.append('')
            
            _r=re.findall(".*(\n)(.*)(牌).*", context)
            if len(_r)>=2: singleData.append(_r[1][1]+'牌')
            else:
                singleData.append('')
            
            _r=re.findall(".*(3.登记口期|3.登记日期)(.*)(4.机动车|转移登记).*", context)
            if _r: singleData.append(_r[0][1])
            else:
                singleData.append('')
            
            _r=re.findall(".*(抵押登记百期|抵押登记日期)(.*)(\n).*", context)
            if _r: singleData.append(_r[0][1])
            else:
                singleData.append('')
            # print(singleData)
            dataframe.append(singleData)
            dirname=''
            context=''
        i=i+1
    return dataframe

# getTxtToDataFrame(fileRead(resultFilePath), ruls)


# dataFrame创建xlsx文件
'''
a= getTxtToDataFrame(fileRead(resultFilePath), ruls)
print(a)
'''

def run():
    global imagePath,resultFilePath
    imagePath=str(imagePath)
    resultFilePath = os.path.join(imagePath,"OCRResult.txt")

    df=pd.DataFrame(getTxtToDataFrame(fileRead(resultFilePath), ruls))
    df.to_excel(os.path.join(imagePath, 'result.xlsx'),sheet_name='data',index=False)
    return 0;
