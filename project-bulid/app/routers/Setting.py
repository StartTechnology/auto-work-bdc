
from fastapi import APIRouter
from pydantic import BaseModel

from core import WorkConfig
import Config
router=APIRouter(prefix='/setting',tags=["Setting设置"])

#POST请求参数类
class SettingPOST(BaseModel):
    path:str=''
#获取工作目录
@router.get('/getworkdir',summary='获取工作目录')
async def getWorkDir()->str:
    return Config.getWorkPath()
#获取临时图片目录
@router.get('/gettempdir',summary='获取临时图片目录')
async def getTempDir()->str:
    return  WorkConfig.getTempImgDir()
#获取图片归档目录
@router.get('/getarchivedir',summary='获取图片归档目录')
async def getArchiveDir()->str:
    return WorkConfig.getArchiveImgDir()


#设置工作目录
@router.post('/setworkdir',summary='设置工作目录')
async def setWorkDir(set:SettingPOST)->None:
    await Config.setWorkPath(set.path)
#获取业务参数
@router.get('/getbusinessconfig',summary='获取业务参数')
async def getBusinessConfig()->dict:
    return await WorkConfig.getBusinessConfig()
#设置业务参数 打开业务配置的文件
@router.get('/openbusinessconfig',summary='获取业务参数')
async def openBusinessConfigFile()->None:
    WorkConfig.openBusinessConfig()
#获取贷款种类种
@router.get('/getloantype',summary='获取贷款种类')
async def getLoanType()->list:
    return await WorkConfig.getLoanType()
#获取担保范围
@router.get('/getguaranteescope',summary='获取担保范围')
async def getGuaranteeScope()->dict:
    return await WorkConfig.getGuaranteeScope()
#获取客户经理
@router.get('/getcustomermanager',summary='获取客户经理')
async def getCustomerManager()->list:
    return await WorkConfig.getCustomerManager()
#获取开发商信息
@router.get('/getdevelopers',summary='获取开发商信息')
async def getDevelopers():
    return await WorkConfig.getDeveloperInfo()

#获取业务xlsx地址
@router.get('/getbusinessxlsx',summary='获取业务xlsx地址')
async def getBusinessXlsx()->str:
    return await WorkConfig.getBusinessXlsx()

#设置业务xlsx地址
@router.post('/setbusinessxlsx',summary='设置业务xlsx地址')
async def setBusinessXlsx(set:SettingPOST)->None:
   await WorkConfig.setBusinessXlsx(set.path)