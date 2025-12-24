import asyncio,pathlib,datetime
import tkinter as tk
from tkinter import filedialog
from core import WorkConfig
#图片格式
IMG_TYPES = [
    '.jpg', '.jpeg', '.png', '.gif', '.webp', 
    '.bmp', '.tif', '.tiff', '.svg', 'pdf'
]

#返回目录内所有的图片信息和图片地址 图片分类 绝对路径 无
async def getImg(dir:str)->list:
    return_list=[]
    for item in pathlib.Path(dir).iterdir():
        if item.is_file():
            if item.suffix in IMG_TYPES:
                return_list.append({'name':item.name,'path':str(item.resolve()),'categories':''})
        elif item.is_dir():
            file_list=filter(lambda x:x.suffix in IMG_TYPES,item.iterdir())
            return_list.extend( list(map(lambda _item:{'name':_item.name,'path':str(_item.resolve()),'categories':item.name},file_list)) )
    return return_list

#创建和解散分类目录 绝对路径
async def synchroniseCatalogues(dir:str,category:list[str])->None:
    dir_path:pathlib.Path= pathlib.Path(dir)
    now_category:list[str]=[path.name for path in dir_path.iterdir() if path.is_dir()]
    
    #新增分类和删除的分类
    new_category:list[str]=list(set(category)-set(now_category))
    del_category:list[str]=list(set(now_category)-set(category))
    #创建新文件夹
    list(map(lambda item:(dir_path/item).mkdir(exist_ok=True),new_category))
    for del_cat in del_category:
        await moveToParent(str((dir_path/del_cat).resolve()))
        (dir_path/del_cat).rmdir()
    pass

#清空目录传入的目录，将文件移动到上级目录 绝对路径
async def moveToParent(dir:str)->None:
    dir_path=pathlib.Path(dir)
    parent_path=dir_path.parent
    list(map(lambda item:item.rename(parent_path/item.name),dir_path.iterdir()))

#将传入的文件列表中的文件移动到上级目录
async def moveFilesToParents(files:list[str])->None:
    for file in files:
        file_path=pathlib.Path(file)
        if file_path.is_file():
            parent=file_path.parent.parent
            file_path.rename(parent/file_path.name)


#使用默认的tkinter打开文件选择框 移动目录到分类
async def selectFileToCategory(dir:str,category:str)->None:
    # 隐藏主窗口
    root = tk.Tk()
    root.withdraw()
    # 设置主窗口为顶层窗口（强制置顶）
    root.attributes('-topmost', True)
    root.lift()  # 提升窗口层级

    # 强制窗口获取焦点（跨平台兼容）
    root.focus_force()
    
    # 设置默认路径和文件类型筛选
    default_path = dir
    file_types = [
         ("所有文件", "*.*")
    ]
    # 打开多选文件对话框
    file_paths = filedialog.askopenfilenames(
        title=f"选择{category}",
        initialdir=default_path,
        filetypes=file_types,
        multiple=True  # 启用多选（可选，默认False）
    )
    file_list=list(file_paths) if file_paths else []
    for file in file_list:
        file_path=pathlib.Path(file)
        new_dir=pathlib.Path(dir)/category
        new_dir.mkdir(parents=True,exist_ok=True)
        file_path.rename(new_dir/file_path.name)

#影像归档
async def imageArchive(dir:str,business_type:str,customer_name:list[str])->str:

    dir_path=pathlib.Path(dir)
    achive_dir=WorkConfig.getArchiveImgDir()
    now=datetime.datetime.now()
    customer_name.append(now.strftime('%H%M%S'))
    achive_dir_path=pathlib.Path(achive_dir)/business_type/now.strftime('%Y%m%d')/' '.join(customer_name)
    achive_dir_path.mkdir(parents=True,exist_ok=True)
    list(map(lambda item:item.rename(achive_dir_path/item.name),dir_path.iterdir()))
    return str(achive_dir_path.resolve())

if __name__=='__main__':
    now=datetime.datetime.now()
    print(now.strftime('%Y-%m-%d %H:%M:%S'))
    print(now.strftime('%Y%m%d'))
    print(now.strftime('%H%M%S'))
    a=['不动产登记申请书', '申请人身份证明', '委托函', '房产证', '借款合同', '其他（可选）']
    a.append(now.strftime('%H%M%S'))

    print(' '.join(a))

    # cate=['不动产登记申请书', '申请人身份证明', '委托函', '房产证', '借款合同', '其他（可选）']
    # dir=r"D:\Program\bdc-service\work\tempimg"

    #list(map(lambda item:(pathlib.Path(dir)/str(item)).mkdir(parents=True,exist_ok=True),cate))
    #print((pathlib.Path(dir)/cate[0]).mkdir(exist_ok=True))
    #a=asyncio.run(getImg(r"D:\Program\bdc-service\work\tempimg"))
    #a=asyncio.run(synchroniseCatalogues(dir,cate))
    #a=asyncio.run( str(list(pathlib.Path(dir).iterdir())[0]) )
    
    #print( pathlib.Path(dir).parent.name )
    pass    