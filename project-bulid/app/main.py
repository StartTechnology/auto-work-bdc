from fastapi.staticfiles import StaticFiles
import uvicorn,json
#创建默认参数
import Config
Config.initdefaultConfig()


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#导入路由
from routers.Setting import router as setting_router
from routers.ImgProcess import router as img_router
from routers.Pushtask import router as pushtask_router



app=FastAPI()
#添加路由
app.include_router(setting_router)
app.include_router(img_router)
app.include_router(pushtask_router)

#去除跨域访问限制
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#服务联通测试
@app.get("/home")
def home():
    return json.dumps(["hello","world"])

#挂载前端Vue项目（静态文件）
app.mount("/", StaticFiles(directory="./static",html=True), name="page")

if __name__=='__main__':
    uvicorn.run(app,host="0.0.0.0",port=8002,reload=False)
    #print(home())