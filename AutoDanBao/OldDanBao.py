# -*- coding: utf-8 -*-
import pandas as pd
import DrissionPage

class CarDanBaoInfo:
    def __init__(self,_pd):
        self.contract=_pd.iloc[0][2]
        self.name=_pd.iloc[0][3]
        self.time=_pd.iloc[0][9]
    pass

#数据转化（从剪贴板）返回列表
def creatClipboardData():
    _list=[]
    _data=pd.read_clipboard(header=None,sep='	')
    for i in range(0,len(_data)):
        _list.append(CarDanBaoInfo(_data.iloc[[i]]))
    return _list

def initPage(port=9222):
    co = DrissionPage.ChromiumOptions().set_local_port(port)
    page = DrissionPage.ChromiumPage(co)
    return page

#旧担保系统录入抵押信息
def carPledge(car_info,port=9222):
    page=initPage(port)
    tab=page.get_tab(page.find_tabs(title='中国邮政储蓄银行担保管理系统'))
    
    if not tab.s_ele('tag=li@@class:tabs-selected@@text():抵质押登记'):
        if not tab.s_ele('tag=li@@class:menu4@@class:open@@text():权证出入库管理'):
            tab.ele('@@text()=权证出入库管理').click()
        tab.ele('@@class:menu1@@text()=抵质押登记').click()
        tab.wait.load_start()

    tab.ele('#contractNo').input(car_info.contract)
    _tab=tab.ele('tag=small@@text():抵质押登记')
    _tab.after('tag=a@@text():搜索').click()
    tab.wait.ele_displayed(_tab.after('#datagrid-row-r1-2-0'))
    _tab.after('#datagrid-row-r1-2-0').click()
    _tab.after('@@text()=维护').click()
    tab.wait.load_start()
    

    tab.wait.ele_displayed(tab.ele('@@text()=影像资料'))
    _tab=tab.ele('tag=small@@text():抵质押登记')
    _tab.after('#datagrid-row-r1-2-0').click()
    _tab.after('@@text()=修改').click()
    #tab.wait.load_start()
    
    
    tab.wait.ele_displayed(tab.ele('tag=small@@text():权证修改'))
    tab.ele('#mrtgEnrollInstType').after('tag=span',2).click()
    #tab.ele('#mrtgEnrollInstType').after('@@text()=交通运输管理部门').wait.displayed()
    tab.ele('#mrtgEnrollInstType').after('@@text()=交通运输管理部门').click()
    tab.ele('#enrollInstName').input('江西省吉安市公安局交通警察支队')
    tab.ele('#genEWarrantFlag').after('tag=span',2).click()
    #tab.ele('#genEWarrantFlag').after('@@text()=否').wait.displayed()
    tab.ele('#enrollDateExistDueStage').after('@@text()=否').click()
    tab.ele('#enrollDateExistDueStage').after('tag=span',2).click()
    #tab.ele('#enrollDateExistDueStage').after('@@text()=否').wait.displayed()
    tab.ele('#enrollDateExistDueStage').after('@@text()=否',2).click()
    tab.ele('#enrollDateString').input(car_info.time)
    tab.ele('@@text()=保存').click()
    tab.wait.ele_displayed(tab.ele('@@text():权证修改成功'))
    tab.ele('tag=a@@text()=确定').click()
    tab.ele('@@text()=返回').click()
    tab.wait.load_start()
    return 1

#旧担保系统录入抵押信息(多条信息)
def carPledges(list_car_info,port=9222):
    for _car_info in list_car_info:
        carPledge(_car_info,port)
    return 1

#旧担保系统入库 返回封包编号
def carRuKu(car_info,port=9222):
    page=initPage(port)
    tab=page.get_tab(page.find_tabs(title='中国邮政储蓄银行担保管理系统'))
    
    if not tab.s_ele('tag=li@@class:tabs-selected@@text():权证入库'):
        if not tab.s_ele('tag=li@@class:menu4@@class:open@@text():权证出入库管理'):
            tab.ele('@@text()=权证出入库管理').click()
        tab.ele('@@class:menu2@@text()=权证入库').click()
        tab.wait.load_start()
    
    
    _tab=tab.ele('tag=small@@text():权证入库')
    _tab.after('tag=a@@text():首次入库').click()
    tab.wait.load_start()
    
    tab.ele('@onclick=addPacket();').click()
    
    tab.wait.ele_displayed(tab.ele('@onclick=selectContract(this);'))
    tab.ele('@onclick=selectContract(this);').click()
    
    
    tab.wait.ele_displayed(tab.ele('@onclick=searchContract(\'searchForm\',\'grid\');'))
    _tab=tab.ele('@onclick=searchContract(\'searchForm\',\'grid\');')
    _tab.before('#contractNo').input(car_info.contract)
    _tab.click()
    tab.wait.ele_displayed(_tab.after('#datagrid-row-r1-2-0'))
    _tab.after('#datagrid-row-r1-2-0').click()
    tab.ele('tag=div@@style:overflow@@class:window-body').after('tag=a@@text():确定').click()


    tab.ele('@onclick=addWarrant();').click()
    tab.wait.load_start()
    #tab.wait.ele_displayed(tab.ele('@text()=权证信息'))
    #tab.wait.ele_displayed(tab.ele('#datagrid-row-r2-2-0'))
    tab.ele('#datagrid-row-r2-2-0').click()
    tab.ele('tag=div@@text()=权证信息').after('tag=a@@text():确定').click()

    tab.wait.ele_displayed(tab.ele('#datagrid-row-r4-2-0'))
    tab.ele('#datagrid-row-r4-2-0').click()
    tab.ele('tag=a@@text()=保存').click()
    
    tab.wait.ele_displayed(tab.ele('#datagrid-row-r3-2-0'))
    tab.ele('#datagrid-row-r3-2-0').click()
    packetNo=tab.ele('#datagrid-row-r3-2-0').child('@field:packetNo').text
    
    tab.ele('@onclick=subInStorage()').click()
    tab.ele('@text()=发起入库成功').after('tag=a@@text():确定').click()
    #tab.wait.load_start()
    return packetNo

#旧担保系统入库 返回字典 key:name value:封包编号
def carRuKus(list_car_info,port=9222):
    packetNos={}
    for car_info in list_car_info:
        packetNos[car_info.name]=carRuKu(car_info,port)
        print(car_info.name,packetNos[car_info.name])
    return packetNos

#carRuKu(creatClipboardData()[0])
#print(carRuKus(creatClipboardData()))
#carRuKus(creatClipboardData())
