# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 12:54:33 2024

@author: LCY
"""

import pandas as pd
# import datetime
from DrissionPage import ChromiumPage, ChromiumOptions
import re
import subprocess


# 第一次运行需要
def firstRun():
    ChromiumOptions().use_system_user_path().save()
    co = ChromiumOptions().use_system_user_path()

class Person:
    def __init__(self,name='',IdCard='',phone=''):
        self.name=name
        self.IdCard=IdCard
        self.phone=phone
        pass
    pass

class PledgeInfo: 
    def __init__(self,clipboard_pd):
        self.persons=[]
        self.persons.append(Person(clipboard_pd.iloc[0][1],clipboard_pd.iloc[0][2],clipboard_pd.iloc[0][3]))
        if not pd.isna(clipboard_pd.iloc[0][4]):
            _names=clipboard_pd.iloc[0][4].splitlines()
            _Ids=str(clipboard_pd.iloc[0][5]).splitlines()
            _iphones=[]
            if pd.isna(clipboard_pd.iloc[0][6]):
                for i in range(0,len(_names)):
                    _iphones.append('0')
            else:
                _iphones=str(clipboard_pd.iloc[0][6]).splitlines()
                if len(_names)>len(_iphones):
                    for i in range(len(_iphones),len(_names)):
                        _iphones.append('0')
            for i in range(0,len(_names)):
                self.persons.append(Person(_names[i],_Ids[i],_iphones[i]))
                pass
            pass

        self.certificates=clipboard_pd.iloc[0][7].splitlines()
        self.contract=clipboard_pd.iloc[0][8]
        self.type=clipboard_pd.iloc[0][9]
        # self.starttime=str(datetime.datetime.strptime(clipboard_pd.iloc[0][10], '%Y/%m/%d').date()).replace('-', '')
        # self.endtime=str(datetime.datetime.strptime(clipboard_pd.iloc[0][11], '%Y/%m/%d').date()).replace('-', '')
        #persons电话号码补全
        for i in range(0,len(self.persons)):
            _i=i
            while self.persons[_i].phone=='0':
                _i=_i-1
            self.persons[i].phone=self.persons[_i].phone
        pass

#剪贴板数据变量 调用creatData函数创建
plinfo=''
#接管浏览器的类变量
page=''

bowserpath='C:\Program Files\Google\Chrome\Application\chrome.exe'
# --remote-debugging-port=9222 --remote-allow-origins=*

#转换剪贴板数据
def creatData():
    global plinfo
    plinfo=PledgeInfo(pd.read_clipboard(header=None,sep='	'))
    return plinfo


#初始化网页page对象
def initPage():
    global page
    co = ChromiumOptions().set_local_port(9222)
    page = ChromiumPage(co)

# 打开浏览器,并打开网页
def openbowser(_bowserpath=bowserpath,_url='https://www.jabdc.com'):
    cmd1 = _bowserpath + ' --remote-debugging-port=9222 --remote-allow-origins=*'
    subprocess.run(cmd1,shell=True ,creationflags=subprocess.CREATE_NO_WINDOW)
    initPage()
    page.get(_url)
    return 0


#点击新增业务
def newBusinessPage():
    initPage()
    tab=page.get_tab(page.find_tabs(url='jabdc'))
    tab.ele('text:新增').click()
    page.wait.load_start()
    return 0

#选择业务类型
def selectBusinessType():
    initPage()
    tab=page.get_tab(page.find_tabs(url='jabdc'))
    
    tab.ele('@placeholder:大类').click()
    if plinfo.type=='一般抵押':
        tab.ele('text:房屋抵押登记').click()
        tab.ele('@placeholder:小类').click()
        tab.ele('text:一般抵押').click()
    elif plinfo.type=='最高额抵押':
        tab.ele('text:房屋抵押登记').click()
        tab.ele('@placeholder:小类').click()
        tab.ele('text:最高额抵押').click()
    elif plinfo.type=='转本登记（预告转正式）':
        tab.ele('text:转本登记').click()
        tab.ele('@placeholder:小类').click()
        tab.ele('text:预售商品房抵押权预告转本登记').click()
    elif plinfo.type=='解押':
        tab.ele('tag=li@@text():房屋抵押注销登记').click()
        tab.ele('@placeholder:小类').click()
        tab.eles('tag=li@@text():房屋抵押注销登记')[-1].click()
        
    elif plinfo.type=='预告解押':
        tab.ele('text:预告登记').click()
        tab.ele('@placeholder:小类').click()
        tab.ele('text:抵押预告注销登记').click()
    
    year=re.findall(".*(赣（)(.*)(）).*",plinfo.certificates[0])
    num=re.findall(".*(第)(.*)(号).*",plinfo.certificates[0])
    
    
    tab.ele('@placeholder:证书类型').click()
    _lis=tab.eles('tag=li@@class=el-select-dropdown__item')
    if not year == []:
        _lis[-2].click()
    else:
        _lis[-1].click()
    
    
    if not (plinfo.type=='解押' or  plinfo.type=='预告解押'):
        tab.ele('text:确定').click()
        page.wait.load_start()
    else:
        if not year == []:
            year=year[0][1]
            num=num[0][1]
            _inputs=tab.ele('.zhTwo').eles('tag=input')
            _inputs[0].input(year)
            _inputs[1].input(num)
        else:
            tab.ele('tag=input@@placeholder:请输入他项权证').input(plinfo.certificates[0])
        tab.ele('text:确定').click()
        page.wait.load_start()
    return 0

#业务界面
def businessInput():
    initPage()
    tab=page.get_tab(page.find_tabs(url='jabdc'))
    '''
    '''
    #添加抵押人信息
    for per in plinfo.persons:
        tab.ele('text:添加抵押人').click()
        tab.ele('@placeholder:请输入姓名').input(per.name)
        tab.ele('@placeholder:请输入联系方式').input(per.phone)
        tab.ele('@@placeholder:请选择证件种类').click()
        tab.ele('tag=li@@class:el-select-dropdown__item@@text()=身份证').click()
        tab.ele('@placeholder:请输入身份证号').input(per.IdCard)
        _ele=tab.ele('text:确认')
        _ele.click()
        _ele.wait.hidden()
    
    
    
    #添加权证信息
    inputs=[]
    _year=re.findall(".*(赣（)(.*)(）).*",plinfo.certificates[0])
    if _year:
         for i in tab.eles('.zhTwo'):
             inputs.extend(i.eles('tag:input'))
         if len(plinfo.certificates)<=(len(inputs)/2):
             lisr_cer=[]
             for _cer in plinfo.certificates:
                 _y=re.findall(".*(赣（)(.*)(）).*",_cer)
                 _n=re.findall(".*(第)(.*)(号).*",_cer)
                 lisr_cer.append(_y[0][1])
                 lisr_cer.append(_n[0][1])
             for _i in range(0,len(inputs)):
                 inputs[_i].input(lisr_cer[_i%len(lisr_cer)])
    else:
        inputs=tab.eles('tag=input@@placeholder:证@!placeholder:身份证@!disabled=disabled@!readonly=readonly')
        for i in range(0,len(inputs)):
            inputs[i].input(plinfo.certificates[i])
    
    #添加抵押信息
    inputs=tab.ele('.yw_con').eles('tag:input')
    inputs[3].click()
    tab.ele('tag=li@@class:el-select-dropdown__item@@text()=1').click()
    inputs[4].input(plinfo.contract)
    #inputs[7].input('')
    return 0
'''
#newBusinessPage()

creatData()
selectBusinessType()
businessInput()

tab=page.get_tab(page.find_tabs(url='jabdc'))
inputs=tab.eles('tag=input@@placeholder:证@!placeholder:身份证@!disabled=disabled@!readonly=readonly')
print(inputs)
'''