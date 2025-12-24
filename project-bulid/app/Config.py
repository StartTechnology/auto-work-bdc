import configparser
import os,pathlib
import asyncio
#配置文件相关操作 IO操作 异步
 
#配置文件内容
#工作目录  业务默认配置xlsx 

#配置文件地址
CONFIG_DIR_PATH=pathlib.Path(__file__).parent.resolve()/'config'
CONFIG_PATH = pathlib.Path(CONFIG_DIR_PATH)/'config.ini'


#创建默认配置
def initdefaultConfig() ->None:
    config_path= pathlib.Path(CONFIG_PATH)
    config_path.parent.mkdir(parents=True,exist_ok=True)
    config=configparser.ConfigParser()
    if not config_path.exists():
        config['FilePath']={
            'WorkPath':r"D:\work",
            'DefaultBusinessConfig':config_path.parent/'业务参数.xlsx',
            'SQLitePath':''
        }
        with open(CONFIG_PATH,'w', encoding='utf-8') as f:
            config.write(f)
    else:
        config.read(CONFIG_PATH, encoding='utf-8')
        config.set('FilePath','DefaultBusinessConfig', str((config_path.parent/'业务参数.xlsx').resolve()) )
        pass
#创建工作文件夹的默认配置
async def initdefaultWorkConfig()->bool:
    work_path:str= getWorkPath()
    if os.path.isdir(work_path):
        #创建配置文件目录
        work_config_path:str=os.path.join(work_path,'config','config.ini')
        pathlib.Path(work_config_path).parent.mkdir(parents=True,exist_ok=True)
        #创建默认的配置文件
        work_config=configparser.ConfigParser()

        work_config['ImageDir']={
            'TempImg': os.path.join(work_path,'tempImg'),
            'ArchiveImg':os.path.join(work_path,'归档影像'),
        }
        work_config['FilePath']={
            'BusinessConfig':pathlib.Path(work_path)/'config'/'业务参数.xlsx',
            'BusinessXlsx':os.path.join(work_path,'抵质押登记.xlsx')
        }
        work_config['SQL']={
            'Sqlite3':''
        }
        with open(work_config_path,'w', encoding='utf-8') as f:
            work_config.write(f)
        #复制默认的业务参数到工作目录的config中
        config=configparser.ConfigParser()
        config.read(CONFIG_PATH, encoding='utf-8')
        print(pathlib.Path(work_config['FilePath']['BusinessConfig']))
        (pathlib.Path(work_config['FilePath']['BusinessConfig'])).write_bytes(pathlib.Path(config['FilePath']['DefaultBusinessConfig']).read_bytes())
        #创建相关目录
        (pathlib.Path(work_path)/'tempImg').mkdir(exist_ok=True)
        (pathlib.Path(work_path)/'归档影像').mkdir(exist_ok=True)
        from core import WorkConfig
        WorkConfig.update_init()
        return True
    else:
        return False


#修改工作目录
async def setWorkPath(work_path:str)->None:
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH,encoding='utf-8')
    config.set('FilePath','WorkPath',work_path)
    with open(CONFIG_PATH,'w',encoding='utf-8') as f:
        config.write(f)
    await initdefaultWorkConfig()

#返回配置文件的工作目录项
def getWorkPath()->str:
    config=configparser.ConfigParser()
    config.read(CONFIG_PATH, encoding='utf-8')
    return config['FilePath']['WorkPath']

#获取业务参数


if __name__=="__main__":
    #asyncio.run(initdefaultConfig())
    print(asyncio.run(initdefaultConfig()))
    pass

