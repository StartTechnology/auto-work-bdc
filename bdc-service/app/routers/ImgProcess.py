from fastapi import APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel
from core import ImageProgram,ImageOCR


router=APIRouter(prefix='/img',tags=["ImageProcess影像处理"])

#POST请求参数类
class ImgProcessPOST(BaseModel):
    path:str|None=None
    category:str|None=None
    file_list:list[str]|None=None
    category_list:list[str]|None=None
    ocr_type:int|None=None

#读取图片信息
@router.post('/gettempimg',summary='获取临时文件夹下的图片[名称、地址、分类]')
async def getTempImg(dir:ImgProcessPOST)->list:
    return await ImageProgram.getImg(dir.path)


#根据链接返回图片
@router.get('/getimg',summary='获取图片')
async def getImg(dir:str):
    return FileResponse(path=dir)


@router.post('/setimgcategory',summary='设置图片分类(路径)')
async def setImgCategory(post:ImgProcessPOST):
    await ImageProgram.selectFileToCategory(post.path,post.category)


@router.post('/syncimgcategory',summary='同步图片分类目录')
async def syncImgCategory(post:ImgProcessPOST):
   await ImageProgram.synchroniseCatalogues(post.path,post.category_list)

@router.post('/clearcategoryimg',summary='清空某个分类图片(目录绝对路径)')
async def clearCategoryImg(post:ImgProcessPOST):
   await ImageProgram.moveToParent(post.path)
@router.post('/delcategoryimg',summary='删除某个分类中的某张图片')
async def delCategoryImg(post:ImgProcessPOST):
   await ImageProgram.moveFilesToParents(post.file_list)


@router.post('/ocrimgs',summary='大模型识别图片信息')
async def ocrImgs(post:ImgProcessPOST):
    match post.ocr_type:
        case 1:
            #身份证
            return await ImageOCR.OCRImgList(post.file_list,ImageOCR.StructKey.IdCard)
        case 2:
            #合同号
            return await ImageOCR.OCRImgList(post.file_list,ImageOCR.StructKey.ContractNumber)
        case 3:
            #贷款金额
            return await ImageOCR.OCRImgList(post.file_list,ImageOCR.StructKey.LoanAmount)
        case 4:
            #贷款期限
            return await ImageOCR.OCRImgList(post.file_list,ImageOCR.StructKey.LoanTerm)
        case 5:
            #抵押登记证明编号
            return await ImageOCR.OCRImgList(post.file_list,ImageOCR.StructKey.RegistrationCertificate)
        case 6:
            #房产证编号
            return await ImageOCR.OCRImgList(post.file_list,ImageOCR.StructKey.PropertyCertificate)
        
#影像归档
@router.post('/archiveimg',summary='影像归档')
async def archive(post:ImgProcessPOST)->str:
    return await ImageProgram.imageArchive(post.path,post.category,post.file_list)