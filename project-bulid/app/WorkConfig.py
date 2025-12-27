import configparser
import pathlib,sys,os
import asyncio
import pandas as pd
sys.path.append(str(pathlib.Path(__file__).absolute().parent.parent))
import Config


WORKPATH=Config.getWorkPath()
WORK_CONFIG_PATH=pathlib.Path(WORKPATH)/'config'/'config.ini'
def update_init():
    global WORKPATH
    global WORK_CONFIG_PATH
    WORKPATH=Config.getWorkPath()
    WORK_CONFIG_PATH=pathlib.Path(WORKPATH)/'config'/'config.ini'

#获取业务文件路径xlsx
async def getBusinessXlsx()->str:
    config=configparser.ConfigParser()
    config.read(WORK_CONFIG_PATH, encoding='utf-8')
    return config['FilePath']['businessxlsx']

#修改业务文件路径xlsx
async def setBusinessXlsx(businessxlsx_path:str)->None:
    config = configparser.ConfigParser()
    config.read(WORK_CONFIG_PATH,encoding='utf-8')
    config.set('FilePath','businessxlsx',businessxlsx_path)
    with open(WORK_CONFIG_PATH,'w',encoding='utf-8') as f:
        config.write(f)

#读取影像归档目录
def getArchiveImgDir()->str:
    config=configparser.ConfigParser()
    config.read(WORK_CONFIG_PATH, encoding='utf-8')
    return config['ImageDir']['archiveimg']

#修改影像归档目录
async def setArchiveImgDir(archiveimg_dir:str)->None:
    config = configparser.ConfigParser()
    config.read(WORK_CONFIG_PATH,encoding='utf-8')
    config.set('ImageDir','archiveimg',archiveimg_dir)
    with open(WORK_CONFIG_PATH,'w',encoding='utf-8') as f:
        config.write(f)



#读取临时影像目录
def getTempImgDir()->str:
    config=configparser.ConfigParser()
    config.read(WORK_CONFIG_PATH, encoding='utf-8')
    return config['ImageDir']['tempimg']
#修改临时影像目录
async def setTempImgDir(tempimg_dir:str)->None:
    config = configparser.ConfigParser()
    config.read(WORK_CONFIG_PATH,encoding='utf-8')
    config.set('ImageDir','tempimg',tempimg_dir)
    with open(WORK_CONFIG_PATH,'w',encoding='utf-8') as f:
        config.write(f)

#读取xlsx配置文件 获取业务信息
'''
注释：前端页面要求格式
columns=[{title:'业务材料1',dataIndex:'abc 0'},{title:'业务材料2',dataIndex:'1'}}
data=[{0:'',1:''}]
'''
async def getBusinessConfig()->dict:
    config=configparser.ConfigParser()
    config.read(WORK_CONFIG_PATH, encoding='utf-8')
    businessconfig:str= config['FilePath']['businessconfig']
    df=pd.read_excel(businessconfig)
    #处理dataframe到前端数据
    colums_title=df.columns.to_list()
    colums_dict=[]
    data_dict=[]
    for i in range(0,len(colums_title)):
        colums_dict.append({'title':colums_title[i],'dataIndex':str(i)})

    for row in df.itertuples():
        _data_dict={}
        for i in range(1,len(colums_title)+1):
            _data_dict[str(i-1)]=row[i]
        data_dict.append(_data_dict)
    return {'columns':colums_dict,'data':data_dict}

#读取xlsx配置文件 修改业务信息 直接打开配置文件所在文件
def openBusinessConfig()->None:
    config=configparser.ConfigParser()
    config.read(WORK_CONFIG_PATH, encoding='utf-8')
    businessconfig:str= config['FilePath']['businessconfig']
    os.startfile(businessconfig)
    pass


#获取贷款种类
async def getLoanType()->list:
    config=configparser.ConfigParser()
    config.read(WORK_CONFIG_PATH, encoding='utf-8')
    businessconfig:str= config['FilePath']['businessconfig']
    df=pd.read_excel(businessconfig,1)
    return df.iloc[:,0].dropna().tolist()
#获取客户经理名称
async def getCustomerManager()->list:
    config=configparser.ConfigParser()
    config.read(WORK_CONFIG_PATH, encoding='utf-8')
    businessconfig:str= config['FilePath']['businessconfig']
    df=pd.read_excel(businessconfig,1)
    return df.iloc[:,1].dropna().tolist()
#获取担保范围(200字内)
async def getGuaranteeScope()->dict:
    config=configparser.ConfigParser()
    config.read(WORK_CONFIG_PATH, encoding='utf-8')
    businessconfig:str= config['FilePath']['businessconfig']
    df=pd.read_excel(businessconfig,2,index_col=0)
    return df.iloc[:,0].dropna().to_dict()

#获取开发商信息（合并登记用）
async def getDeveloperInfo():
    config=configparser.ConfigParser()
    config.read(WORK_CONFIG_PATH, encoding='utf-8')
    businessconfig:str= config['FilePath']['businessconfig']
    df=pd.read_excel(businessconfig,3,index_col=0,dtype={2:str})
    return list(map(lambda x:list(x),df.to_records()))


if __name__=='__main__':
    result= asyncio.run(getDeveloperInfo())
    print(result)
