import asyncio
from fastapi import APIRouter
from core import PushBusinessTask
from core.PushBusinessTask import BusinessInfo
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix='/pushtask',tags=["提交任务"])

class TaskInfo(BaseModel):
    business_info:Optional[BusinessInfo]=None
    path:Optional[str]=None

@router.post("/pushtask",summary='提交任务')
async def push_task(business_info:BusinessInfo):
    buss_info=await PushBusinessTask.readBusinessInfoFromCache(business_info.img_path)
    if not buss_info is None:
        business_info=buss_info
    else:
        await PushBusinessTask.cacheBusinessInfo(business_info)
    await PushBusinessTask.webSelectType(business_info.business_type,business_info.certificate)
    await PushBusinessTask.webInputInfo(business_info)
    await PushBusinessTask.webUploadImg(business_info)
    #PushBusinessTask.webSave()

#将业务信息写入wps
@router.post("/towps",summary='写入业务信息到wps表格')
async def push_task(post:TaskInfo):
    business_info:BusinessInfo=post.business_info
    path:str=post.path
    await PushBusinessTask.writeBusinessInfoToWps(business_info,path)