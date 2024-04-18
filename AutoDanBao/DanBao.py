# -*- coding: utf-8 -*-
import os
import glob
import pandas as pd
import DrissionPage


'''
DanBaoInfo类型_type
house:一手房
car:车贷
'''
#存量房抵押信息
class DanBaoInfo:
    def __init__(self,_pd,_type=''):

        if _type=='car':
            self.type='纸质权证'
        elif pd.isna(_pd.iloc[0][1]):
            self.type='纸质权证'
        elif _pd.iloc[0][1]=='电子权证':
            self.type='电子权证'
        else:
            self.type='纸质权证'

        self.contract=_pd.iloc[0][2]

        if  _type=='house':
            self.name=_pd.iloc[0][6]
            self.certificates=_pd.iloc[0][7]
            self.certificates_type=_pd.iloc[0][8]
            self.money=_pd.iloc[0][9]
            self.stsartTime=_pd.iloc[0][10]
            self.endTime=None
        elif _type=='car':
            self.name=_pd.iloc[0][3]
            self.certificates=_pd.iloc[0][7]
            self.certificates_type='机动车登记证'
            self.money=_pd.iloc[0][8]
            self.stsartTime=_pd.iloc[0][9]
            self.endTime=_pd.iloc[0][10]
        else:
            self.name=_pd.iloc[0][4]
            self.certificates=_pd.iloc[0][6]
            self.certificates_type='抵押登记证明'
            self.money=_pd.iloc[0][7]
            self.stsartTime=_pd.iloc[0][9]
            self.endTime=_pd.iloc[0][10]
        
#从文件夹及其内部文件夹内找到含有名字的文件 返回list
def findFileList(file_path,file_name):
    f_p=glob.glob(str(file_path)+'\\'+'*'+file_name+'*')
    f_p.extend(glob.glob(str(file_path)+'\\'+r'**\*'+file_name+'*'))
    return f_p

#数据转化（从剪贴板）返回列表
def creatClipboardData(type=''):
    _list=[]
    _data=pd.read_clipboard(header=None,sep='	')
    for i in range(0,len(_data)):
        _list.append(DanBaoInfo(_data.iloc[[i]],type))
    return _list
#接管浏览器
def initPage(port=9222):
    co = DrissionPage.ChromiumOptions().set_local_port(port)
    page = DrissionPage.ChromiumPage(co)
    return page

#担保系统录入抵押信息
def dataPledge(data_info,dir_path,port=9222):
    
    page = initPage(port)
    tab=page.get_tab(page.find_tabs(title='担保管理系统'))

    _title = tab.ele('tag=span@@text():首页@@class:tags-view-item').parent()
    if not _title.child('@@text():抵质押登记@@class:active'):
        if not tab.s_ele('@@role:menuitem@@text():权证管理@@class:is-opened'):
            tab.ele('@@role:menuitem@@text():权证管理').click()
        tab.ele('@@role:menuitem@@text()=抵质押登记').click()
    else:
        if tab.ele('tag=button@@text()=返回'):
            tab.ele('tag=button@@text()=返回').click()

    tab.wait.ele_displayed(tab.ele('tag=input@@placeholder:请输入合同编号'))
    tab.ele('tag=input@@placeholder:请输入合同编号').input(data_info.contract)
    tab.ele('tag=button@@text():查询').click()
    
    
    tab.wait.ele_displayed(tab.ele('@@text()= 抵押登记 '))
    是否推送业务=True
    try:
        tab.ele('@@text()= 签收 ').click()
        tab.wait.ele_displayed(tab.ele('tag=p@@text():签收成功'))
        tab.ele('tag=p@|text():签收成功@|text():不能做签收操作').after('tag=button@@text():确定').click()
        tab.wait.load_start()
    except:
        是否推送业务=False
        pass
    tab.ele('@@text()= 抵押登记 ').click()

    
    
    tab.wait.ele_displayed(tab.ele('@class:zOperatingLeft'))
    tab.ele('@text():新增').click()
    
    
    tab.wait.ele_displayed(tab.ele('tag=label@@text():权证类型@@class:el-form-item__label'))
    
    tab.ele('tag=label@@text():权证类型@@class:el-form-item__label').after('@@class:el-input').click()
    
    tab.ele(f'tag=li@@text()={data_info.certificates_type}@@class:el-select-dropdown__item').click()
    
    #文件上传 路径函数
    f_p=findFileList(dir_path,data_info.name)

    if len(f_p)<10:
        for i in range(0,len(f_p)):
            tab.set.upload_files(f_p[i])
            tab.ele('tag=label@@text():影像上传@@class:el-form-item__label').after('tag=button',2).click()
            tab.wait.upload_paths_inputted()
            tab.wait.load_start()
    elif len(f_p)==0:
        print('未找到文件')
    else:
        print('存在超过10个同名文件')
        return 0
    
    for i in f_p:
        tab.ele(f'tag=tr@@text():{os.path.basename(i)}').ele('tag=input@@placeholder:请选择').click()
        tab.eles('tag=li@@text()=他项权证@@class:el-select-dropdown__item')[-1].click()
    tab.eles(f'tag=tr@@text():{os.path.basename(f_p[0])}')[-1].ele('tag=button@@text():ocr识别').click()
    tab.wait.load_start()

    tab.ele('tag=label@@text():登记机构类型@@class:el-form-item__label').after('@@class:el-input').click()
    tab.ele('tag=li@@text()=不动产登记中心@@class:el-select-dropdown__item').click()
    
    tab.ele('tag=label@@text():是否存在登记到期日@@class:el-form-item__label').after('@@class:el-input').click()
    tab.ele('tag=li@@text()=土地管理部门@@class:el-select-dropdown__item').after(('tag=li@@text()=是@@class:el-select-dropdown__item')).click()

    
    tab.ele('tag=label@@text():是否电子权证@@class:el-form-item__label').after('@@class:el-input').click()
    if data_info.type=='电子权证':
        tab.eles('tag=li@@text()=是@@class:el-select-dropdown__item')[1].click()
    else:
        tab.eles('tag=li@@text()=否@@class:el-select-dropdown__item')[1].click()

    
    tab.ele('tag=label@@text():权证编号@@class:el-form-item__label').after('@@class:el-input').input(data_info.certificates)
    tab.ele('tag=label@@text():登记金额@@class:el-form-item__label').after('@@class:el-input').input(data_info.money*10000)
    
    tab.ele('tag=label@@text()=登记日期@@class:el-form-item__label').after('tag=input').input(data_info.stsartTime)
    _e=tab.ele('tag=label@@text()=登记到期日期@@class:el-form-item__label')
    _e.after('tag=input').input(data_info.endTime)
    _e.click()
    tab.ele('tag=button@@text()=保存').click()
    
    if 是否推送业务:
        tab.wait.ele_displayed(tab.ele('tag=p@@text():抵质押登记权证已经创建成功'))
        tab.ele('tag=p@@text():抵质押登记权证已经创建成功').after('tag=button@@text():确定').click()
        tab.wait.load_start()
        tab.ele(f'tag=tr@@text():{data_info.certificates}').ele('.el-checkbox').click()
        tab.ele('tag=button@@text():完结反馈业务').click()
        tab.wait.ele_displayed(tab.ele('@@text():推送成功'))
        tab.ele('@@class=el-message-box@@text():推送成功').ele('tag=button@@text():确定').click()
    
    tab.wait.load_start()
    tab.ele('tag=button@@text()=返回').click()

    return 1

#担保系统录入抵押信息(多条信息)
def dataPledges(list_data_info,dir_path,port=9222):
    for _data_info in list_data_info:
        dataPledge(_data_info,dir_path,port)
    return 1

#担保系统入库  返回封包编号
def dataRuKu(data_info,port=9222):
    page = initPage(port)
    tab=page.get_tab(page.find_tabs(title='担保管理系统'))

    _title = tab.ele('tag=span@@text():首页@@class:tags-view-item').parent()
    if not _title.child('@@text():抵质押登记@@class:active'):
        if not tab.s_ele('@@role:menuitem@@text():权证管理@@class:is-opened'):
            tab.ele('@@role:menuitem@@text():权证管理').click()
        tab.ele('@@role:menuitem@@text()=抵质押登记').click()
    else:
        if tab.ele('tag=button@@text()=返回'):
            tab.ele('tag=button@@text()=返回').click()

    tab.wait.ele_displayed(tab.ele('tag=input@@placeholder:请输入合同编号'))
    tab.ele('tag=input@@placeholder:请输入合同编号').input(data_info.contract)
    tab.ele('tag=button@@text():查询').click()
    
    tab.wait.load_start()
    #tab.wait.ele_displayed(tab.ele('tag=a@@text()= 抵押登记 '))
    tab.ele('tag=a@@text()= 抵押登记 ').click()

    if data_info.type=='电子权证':
        tab.wait.ele_displayed(tab.ele(f'@@text()={data_info.certificates}'))
        tab.ele(f'@@text()={data_info.certificates}').before('.el-checkbox').click()
        tab.ele('tag=button@@text()=电子权证入库').click()
        tab.wait.ele_displayed(tab.ele('@@text():入库吗'))
        tab.ele('@@class=el-message-box@@text():入库吗').ele('tag=button@@text():确定').click()
        tab.wait.ele_displayed(tab.ele('@@text():入库成功'))
        tab.ele('@@class=el-message-box@@text():入库成功').ele('tag=button@@text():确定').click()
        tab.wait.load_start()
        tab.ele('tag=button@@text()=返回').click()
        return data_info.type
    elif data_info.type=='纸质权证':
        tab.ele('tag=button@@text():跳转纸质权证首次入库').click()
        tab.wait.ele_displayed(tab.ele('@aria-label:封包信息'))
        tab.ele('@aria-label:封包信息').ele('tag=button@@text():新增').click()
        tab.wait.ele_displayed(tab.ele('@aria-label:封包详细信息'))
        tab.ele('@aria-label:封包详细信息').ele(f'@@text()={data_info.certificates}').before('.el-checkbox').click()
        tab.ele('@aria-label:封包详细信息').ele('tag=button@@text():确定').click()
        tab.ele('@aria-label:封包信息').ele('tag=button@@text():确定').click()
        tab.wait.load_start()
        packetNos=tab.ele(f'tag=td@@text():{data_info.contract}').before('tag=td').text
        tab.ele(f'tag=tr@@text():{data_info.contract}').ele('.el-checkbox').click()
        tab.ele('tag=button@@text():发起入库').click()
        return packetNos
    
    pass

#担保系统入库(多条信息)
def dataRukus(list_data_info,port=9222):
    for _data_info in list_data_info:
        print(_data_info.name,dataRuKu(_data_info,port))
    return 1

#dataPledges(creatClipboardData('house'),r'C:\Users\dkzx\Desktop\权证交接\20240327')

#dataPledges(creatClipboardData(),r'C:\Users\dkzx\Desktop\权证交接\20240321')

def codetest():
    page=initPage()
    tab=page.get_tab(page.find_tabs(title='担保管理系统'))
    #tab.wait.ele_displayed(tab.ele('tag=a@@text()= 抵押登记 '))
    li=tab.eles('tag=a@@text()= 抵押登记 ')
    for i in li:
        print(i)
#codetest()

#dataRuKu(creatClipboardData('house')[0])
#file_path=r'C:\Users\dkzx\Desktop\权证交接\20240402'
#data_list=creatClipboardData()
#dataPledges(data_list,file_path)
#dataRukus(data_list)
#packageNo=dataRuKu(data_list[0])
#print(data_list[0].name,packageNo)