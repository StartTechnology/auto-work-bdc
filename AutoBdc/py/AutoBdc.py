# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 12:54:33 2024

@author: LCY
"""
import os
import pandas as pd
import DrissionPage
import re
import subprocess


bowserpath='C:\Program Files\Google\Chrome\Application\chrome.exe'
# --remote-debugging-port=9222 --remote-allow-origins=*

# 第一次运行需要,使用本地用户浏览器数据
def firstRun():
    DrissionPage.ChromiumOptions().use_system_user_path().save()
    return 1

class Person:
    def __init__(self,name='',IdCard='',phone=''):
        self.name=name
        self.IdCard=IdCard
        self.phone=phone
        pass
    pass


'''
数据类型：
存量抵押解押（默认） 
预告
'''
class PledgeInfo: 
    def __init__(self,_pd,_type=''):
        self.persons=[]
        if _type=='预告':
            #预告数据转换
            self.persons.append(Person(_pd.iloc[0][3],_pd.iloc[0][4],_pd.iloc[0][5]))
            if not pd.isna(_pd.iloc[0][6]):
                _names=_pd.iloc[0][6].splitlines()
                _Ids=str(_pd.iloc[0][7]).splitlines()
                _iphones=[]
                if pd.isna(_pd.iloc[0][8]):
                    for i in range(0,len(_names)):
                        _iphones.append('0')
                else:
                    _iphones=str(_pd.iloc[0][8]).splitlines()
                    if len(_names)>len(_iphones):
                        for i in range(len(_iphones),len(_names)):
                            _iphones.append('0')
                for i in range(0,len(_names)):
                    self.persons.append(Person(_names[i],_Ids[i],_iphones[i]))
                    pass
                pass
            pass
            self.house_contract=_pd.iloc[0][1]
            self.obligor=Person(_pd.iloc[0][9],_pd.iloc[0][10],_pd.iloc[0][11])
            self.contract=_pd.iloc[0][12]
            self.type='预告抵押登记'
        
        else:
            self.persons.append(Person(_pd.iloc[0][1],_pd.iloc[0][2],_pd.iloc[0][3]))
            if not pd.isna(_pd.iloc[0][4]):
                _names=_pd.iloc[0][4].splitlines()
                _Ids=str(_pd.iloc[0][5]).splitlines()
                _iphones=[]
                if pd.isna(_pd.iloc[0][6]):
                    for i in range(0,len(_names)):
                        _iphones.append('0')
                else:
                    _iphones=str(_pd.iloc[0][6]).splitlines()
                    if len(_names)>len(_iphones):
                        for i in range(len(_iphones),len(_names)):
                            _iphones.append('0')
                for i in range(0,len(_names)):
                    self.persons.append(Person(_names[i],_Ids[i],_iphones[i]))
                    pass
                pass
            self.certificates=_pd.iloc[0][7].splitlines()
            self.contract=_pd.iloc[0][8]
            self.type=_pd.iloc[0][9]
        # self.starttime=str(datetime.datetime.strptime(_pd.iloc[0][10], '%Y/%m/%d').date()).replace('-', '')
        # self.endtime=str(datetime.datetime.strptime(_pd.iloc[0][11], '%Y/%m/%d').date()).replace('-', '')
        #persons电话号码补全
        for i in range(0,len(self.persons)):
            _i=i
            while self.persons[_i].phone=='0':
                _i=_i-1
            self.persons[i].phone=self.persons[_i].phone
        pass


#转换剪贴板数据 返回DataForm
def creatClipboardData():
    return pd.read_clipboard(header=None,dtype=str,sep='	')

#初始化网页page对象,返回page
def initPage(port=9222):
    co = DrissionPage.ChromiumOptions().set_local_port(port)
    return DrissionPage.ChromiumPage(co)

# 打开浏览器,并打开网页
def openbowser(_bowserpath=bowserpath,_url='https://www.jabdc.com',port=9222):
    cmd1 = _bowserpath + f' --remote-debugging-port={port} --remote-allow-origins=*'
    subprocess.run(cmd1,shell=True ,creationflags=subprocess.CREATE_NO_WINDOW)
    page=initPage(port)
    page.get(_url)
    return 1


#点击新增业务
def newBusiness(port=9222):
    page=initPage(port)
    tab=page.get_tab(page.find_tabs(url='jabdc'))

    tab.ele('@@class:tabs-qh@@text(): 待提交 ').click()
    tab.ele('text:新增').click()
    page.wait.load_start()
    return 1

#选择业务类型
def selectBusinessType(plinfo,port=9222):
    page=initPage(port)
    tab=page.get_tab(page.find_tabs(url='jabdc'))
    
    tab.ele('@placeholder:大类').click()
    if plinfo.type=='一般抵押':
        tab.ele('text:房屋抵押登记').click()
        tab.ele('@placeholder:小类').click()
        tab.ele('text=一般抵押').click()
    elif plinfo.type=='最高额抵押':
        tab.ele('text:房屋抵押登记').click()
        tab.ele('@placeholder:小类').click()
        tab.ele('text=最高额抵押').click()
    elif plinfo.type=='转本登记（预告转正式）':
        tab.ele('text=转本登记').click()
        tab.ele('@placeholder:小类').click()
        tab.ele('text=预售商品房抵押权预告转本登记').click()
    elif plinfo.type=='解押':
        tab.ele('tag=li@@text():房屋抵押注销登记').click()
        tab.ele('@placeholder:小类').click()
        tab.eles('tag=li@@text():房屋抵押注销登记')[-1].click()
    elif plinfo.type=='预告解押':
        tab.ele('text:预告登记').click()
        tab.ele('@placeholder:小类').click()
        tab.ele('text:抵押预告注销登记').click()
    elif plinfo.type=='预告抵押登记':
        tab.ele('text:合并登记').click()
        tab.ele('@placeholder:小类').click()
        tab.ele('text:转移抵押预告合一登记(开发商、银行)').click()
        tab.ele('text:确定').click()
        page.wait.load_start()
        return 1
        

    
    year=re.findall(".*(赣（)(.*)(）).*",plinfo.certificates[0])
    num=re.findall(".*(第)(.*)(号).*",plinfo.certificates[0])
    #print(year[0][1],num[0][1])
    
    tab.ele('@placeholder:证书类型').click()
    _lis=tab.eles('tag=li@@class:el-select-dropdown__item')
    if not year == []:
        _lis[-2].click()
    else:
        _lis[-1].click()
    
    
    if not (plinfo.type=='解押' or  plinfo.type=='预告解押' or plinfo.type=='转本登记（预告转正式）'):
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

#挨个上传影像避免卡死
def up_img_onebyone(file,ele):
    for i in file:
        ele.click.to_upload(i)
        ele.wait(0.3)
    return 1
#上传影像
def upImage(image_path,tab):
    
    if image_path=="":
        return 1
    else:
        tab_img=tab.ele("tag=div@@class:annex_box")
        for i in os.listdir(image_path):
            image_path_dir=os.path.join(image_path,i)
            file_list=[]
            if os.path.isdir(image_path_dir):
                files=os.listdir(image_path_dir)
                for i_img in files:
                    image_path_dir_file=os.path.join(image_path_dir,i_img)
                    if os.path.isfile(image_path_dir_file):
                        file_list.append(image_path_dir_file)
                        pass
                    pass
                #上传文件
                if(len(file_list)==0):return 0
                
                if "不动产登记申请书" == i:
                    up_img_onebyone(file_list,tab_img.ele("tag=li@@text():不动产登记申请书").ele("tag=div@@class:el-upload--text"))
                elif "不动产抵押登记询问笔录"==i:
                    #tab_img.ele("tag=li@@text():询问笔录").ele("tag=div@@class:el-upload--text").click.to_upload(file_list)
                    up_img_onebyone(file_list,tab_img.ele("tag=li@@text():询问笔录").ele("tag=div@@class:el-upload--text"))
                elif "申请人身份证明"==i:
                    #tab_img.ele("tag=li@@text():申请人身份证明").ele("tag=div@@class:el-upload--text").click.to_upload(file_list)
                    up_img_onebyone(file_list,tab_img.ele("tag=li@@text():申请人身份证明").ele("tag=div@@class:el-upload--text"))
                elif "委托函"==i:                    
                    #tab_img.ele("tag=li@@text():委托函").ele("tag=div@@class:el-upload--text").click.to_upload(file_list)
                    up_img_onebyone(file_list,tab_img.ele("tag=li@@text():委托函").ele("tag=div@@class:el-upload--text"))
                elif "商品房预售合同"==i:
                    #tab_img.ele("tag=li@@text():预售合同").ele("tag=div@@class:el-upload--text").click.to_upload(file_list)
                    up_img_onebyone(file_list,tab_img.ele("tag=li@@text():预售合同").ele("tag=div@@class:el-upload--text"))
                elif "不动产登记证明"==i:
                    #tab_img.ele("tag=li@@text():不动产登记证明").ele("tag=div@@class:el-upload--text").click.to_upload(file_list)
                    up_img_onebyone(file_list,tab_img.ele("tag=li@@text():不动产登记证明").ele("tag=div@@class:el-upload--text"))
                elif "借款合同"==i:
                    up_img_onebyone(file_list,tab_img.ele("tag=li@|text():个人授信合同@|text():借款合同@|text():主债权合同").ele("tag=div@@class:el-upload--text"))
                    #tab_img.ele("tag=li@|text():个人授信合同@|text():借款合同@|text():主债权合同").ele("tag=div@@class:el-upload--text").click.to_upload(file_list)
                elif "房产证"==i:
                    up_img_onebyone(file_list,tab_img.ele("tag=li@@text():不动产权证书").ele("tag=div@@class:el-upload--text"))
                elif "抵押合同"==i:
                    up_img_onebyone(file_list,tab_img.ele("tag=li@@text():抵押合同").ele("tag=div@@class:el-upload--text"))
                    #tab_img.ele("tag=li@@text():抵押合同").ele("tag=div@@class:el-upload--text").click.to_upload(file_list)
                elif "不动产抵押权注销证明"==i:
                    up_img_onebyone(file_list,tab_img.ele("tag=li@@text():注销证明").ele("tag=div@@class:el-upload--text"))
                    #tab_img.ele("tag=li@@text():注销证明").ele("tag=div@@class:el-upload--text").click.to_upload(file_list)
                elif "关于抵押预告登记的约定"==i:
                    up_img_onebyone(file_list,tab_img.ele("tag=li@@text():约定").ele("tag=div@@class:el-upload--text"))
                    #tab_img.ele("tag=li@@text():约定").ele("tag=div@@class:el-upload--text").click.to_upload(file_list)
                elif "结婚证或具结保证书"==i:
                    up_img_onebyone(file_list,tab_img.ele("tag=li@@text():结婚证或具结保证书").ele("tag=div@@class:el-upload--text"))
                    #tab_img.ele("tag=li@@text():结婚证或具结保证书").ele("tag=div@@class:el-upload--text").click.to_upload(file_list)
                elif "其他"==i:
                    up_img_onebyone(file_list,tab_img.ele("tag=li@@text():其他").ele("tag=div@@class:el-upload--text"))
                    #tab_img.ele("tag=li@@text():其他").ele("tag=div@@class:el-upload--text").click.to_upload(file_list)
                    pass
                tab.wait(0.5)
                pass
        
#业务界面
def businessInput(plinfo,image_path="",port=9222):
    page=initPage(port)
    tab=page.get_tab(page.find_tabs(url='jabdc'))
    if plinfo.type=='解押' or plinfo.type=='预告解押':
        upImage(image_path,tab)
        return 1
    elif plinfo.type=='预告抵押登记':
        #预告业务界面
        tab.ele('@@text()=合同编号@@for:htbh').after('@placeholder:请输入合同编号').input(plinfo.house_contract)
        #添加权利人信息
        for per in plinfo.persons:
            tab.ele('text:添加权利人').click()
            tab.ele('@placeholder:请输入姓名').input(per.name)
            tab.ele('@placeholder:请输入联系方式').input(per.phone)
            tab.ele('@@placeholder:请选择证件种类').click()
            tab.ele('tag=li@@class:el-select-dropdown__item@@text()=身份证').click()
            tab.ele('@placeholder:请输入身份证号').input(per.IdCard)
            _ele=tab.ele('text:确认')
            _ele.click()
            _ele.wait.hidden()
        
        #添加义务人
        tab.ele('text:添加义务人').click()
        dialog_title=tab.ele('@@class:el-dialog__header@@text():义务人信息')
        dialog_title.after('@placeholder:请输入姓名').input(plinfo.obligor.name)
        dialog_title.after('@placeholder:请输入联系方式').input(plinfo.obligor.phone)
        #dialog_title.after('@@placeholder:请选择证件种类').input('营业执照')
        dialog_title.after('@@placeholder:请选择证件种类').click()
        tab.eles('tag=li@@class:el-select-dropdown__item@@text():营业执照')[-1].click()
        dialog_title.after('@placeholder:请输入证件号').input(plinfo.obligor.IdCard)
        _ele=dialog_title.after('text:确认')
        _ele.click()
        _ele.wait.hidden()

        tab.ele('text:银行合同编号').after('@placeholder:请输入合同编号').input(plinfo.contract)
        upImage(image_path,tab)
        return 1
    elif plinfo.type=='转本登记（预告转正式）':
            
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
            
            #添加抵押信息
            inputs=tab.ele('.yw_con').eles('tag:input')
            inputs[2].input(plinfo.contract)
            inputs[8].click()
            tab.ele('tag=li@@class:el-select-dropdown__item@@text()=1').click()
            upImage(image_path,tab)
            return 1

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
    upImage(image_path,tab)
    return 1


def codetest(port=9222):
    page=initPage(port)
    tab=page.get_tab(page.find_tabs(url='jabdc'))
    image_path=r"C:\Users\dkzx\Desktop\Lcy-抵押登记\影像\解押\20240418\黄舒岚"
    upImage(image_path,tab)
    print("完成")

#codetest()
#print(PledgeInfo(creatClipboardData(),'预告'))
#print(creatClipboardData().iloc[0][11])
'''
data=PledgeInfo(creatClipboardData())
newBusiness()
selectBusinessType(data)
businessInput(data)
'''
