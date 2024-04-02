# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 15:48:01 2024

@author: LCY
"""
import os
import subprocess

UIMPath="D:\\Umi-OCR_Paddle_v2.1.0\\Umi-OCR.exe"

imagePath = 'C:\\Users\\LCY\\Desktop\\te\\'


# 单个图片OCR至指定文件中(两个参数绝对路径)
def fileOCR(filepath,fileResult):
    # cmd1 = UIMPath+ " --path "+filepath+"  -->>"+fileResult
    
    cmd1 = UIMPath+ " --path "+filepath+"  -->>"+fileResult
    #os.system(cmd1)
    return subprocess.run(cmd1,shell=True ,creationflags=subprocess.CREATE_NO_WINDOW)


# 打开txt（） 如没有则创建文件并写入（），关闭
def writerFile(filePath,txt):
    file=open(filePath,'a')
    file.write(txt)
    file.close()


# 读取目录下所有一级文件夹数量返回列表
def listdir(dirs):
    listdirs = []
    for name in os.listdir(dirs):
        if os.path.isdir(os.path.join(dirs, name)):
            listdirs.append(name)
    return listdirs

#读取目录下所有一级文件数量，返回列表
def listfile(dirs):
    listfiles = []
    for name in os.listdir(dirs):
        if os.path.isfile(os.path.join(imagePath,dirs,name)):
            listfiles.append(name)
    return listfiles



# 遍历所有一级文件夹内图片OCR并保存至目录同级文件夹txt中（每个文件夹添加开始结束标识符）
def run():
    
    global UIMPath,imagePath
    UIMPath=str(UIMPath)
    imagePath=str(imagePath)
    resultFilePath = os.path.join(imagePath,"OCRResult.txt")
    
    for dirs in listdir(imagePath):
        writerFile(resultFilePath,"Start"+dirs+"\n")
        for files in listfile(os.path.join(imagePath, dirs)):
            fileOCR(os.path.join(imagePath, dirs,files),resultFilePath)
        writerFile(resultFilePath,"End"+dirs+"\n")
    return 0;
