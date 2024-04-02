# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 12:54:33 2024

@author: LCY
"""

import subprocess
from DrissionPage import ChromiumPage, ChromiumOptions
import DanBao
import pandas.io.clipboard as cb

# 第一次运行需要
def firstRun():
    ChromiumOptions().use_system_user_path().save()
    co = ChromiumOptions().use_system_user_path()

bowserpath=r'D:\PSBCBrowser\Program\PSBCBrowser.exe'
bowserpath1='\"C:\Program Files\Google\Chrome\Application\chrome.exe\"'
# --remote-debugging-port=9222 --remote-allow-origins=*

# 打开浏览器,并打开网页
def openbowser(_bowserpath=bowserpath1,_url='https://22.230.88.182/login.html'):
    cmd1 = _bowserpath + ' --remote-debugging-port=9222 --remote-allow-origins=*'
    subprocess.run(cmd1,shell=True ,creationflags=subprocess.CREATE_NO_WINDOW)
    co = ChromiumOptions().set_local_port(9222)
    page = ChromiumPage(co)
    page.get(_url)
    return 0


#点击自动化用印
def useY():
    co = ChromiumOptions().set_local_port(9222)
    page = ChromiumPage(co)
    tab=page.get_tab(page.find_tabs(title='印章'))
    if tab.s_ele('#tabsPageHeaderContent').child('@title:人工授权用印'):
        tab.ele('#tabsPageHeaderContent').child('@title:人工授权用印').click()
        pass
    else:
        if tab.s_ele('tag=h3@@text()=自动化用印@@aria-selected=false'):
            tab.ele('tag=h3@@text()=自动化用印@@aria-selected=false').click()
        if tab.s_ele('tag=span@@id=2Tree_10_switch@@class:center_close'):
            tab.ele('tag=span@@id=2Tree_10_switch').click()
        tab.ele('#2Tree_12_span').click()
    
    tab.ele('tag=input@@data-index=0').click()
    tab.ele('tag=button@@text():用印@@data-trancode=505011').click()

    page.wait.ele_displayed(page.ele('tag=div@@class:dialogContent'))
    #_f=page.ele('tag=div@@class:dialogContent')
    tab.ele('#btn_submit_dialog').click()
    # page.wait.load_start()
    # page.wait(5)
    page.wait.ele_displayed(page.ele('@text():请确认已放入凭证'))
    page.ele('@text():请确认已放入凭证').parent().child('@text():已放入').click()

file_path=r'C:\Users\dkzx\Desktop\权证交接\20240402'
#openbowser()
#DanBao.dataPledges(DanBao.creatClipboardData(),file_path)
DanBao.dataPledges(DanBao.creatClipboardData('house'),file_path)
#useY()