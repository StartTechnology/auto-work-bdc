#使用硅基流动APi的免费大模型进行OCR作业
# THUDM/GLM-4.1V-9B-Thinking
# 密钥 sk-zhjfscwkpmrgsybhwdgugrfmjjzwcdoaizenvgrcouothsdo
from typing import List
import requests,asyncio,re,json
import base64
from enum import Enum
API_URL = "https://api.siliconflow.cn/v1/chat/completions"

API_MODEL="THUDM/GLM-4.1V-9B-Thinking"
API_MODEL_BACKUP="deepseek-ai/deepseek-vl2"

API_KEY="sk-zhjfscwkpmrgsybhwdgugrfmjjzwcdoaizenvgrcouothsdo"

class StructKey(Enum):
    IdCard=r'{"name":(识别到的姓名),"id":(识别到的身份证号)}'
    ContractNumber=r'{"contract":(识别到的合同编号)}'
    LoanAmount=r'{"loan":(识别到的贷款金额数字,int类型)}'
    LoanTerm=r'{"start":(识别到的开始时间,格式:YYmmdd),"end":(识别到的结束时间,格式:YYmmdd)}'
    RegistrationCertificate=r'{"id":(识别到的完整的抵押登记证明号，通常为"赣（*）*不动产证明第*号"或"**第*号",去除所有空格))}'
    PropertyCertificate=r'{"id":(识别到的完整的房产证号，通常为"赣（*）*不动产*第*号"或"*房权证*第*号",去除所有空格)}'


def ImgToBase64(img_path:str):
    with open(img_path,'rb') as imgfile:
        return base64.b64encode(imgfile.read()).decode('utf-8')


#大模型OCR一张图片（只能一次一张）
async def ModelOcrImg(img_path:str,struct_key:StructKey):
    # 构造请求头
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    # 构造请求体
    payload = {
        "model": API_MODEL,  # 模型名称
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{ImgToBase64(img_path)}"}},
                    {"type": "text", "text": "请OCR这张图片，并使用如下结构化返回标准json数组格式(如无结果则返回空数组)结果："+struct_key.value}
                ]
            }
        ],
        #"prompt":  "请OCR这张图片，并使用如下结构化返回标准json格式结果："+struct_key,
        "temperature": 0.7,      # 生成随机性(0-2，建议0.7-1.0)
        "top_p": 0.9,            # 核心采样阈值(0-1，建议0.8-0.95)
        "max_tokens": 1024,      # 最大生成长度(建议512-2048)
        "stream": False, 
        "detail": "high",  # 关键参数：控制输出精度
        "response_format ": {'type': 'json_object'}
    }
    try:
        response=requests.post(API_URL,headers=headers,json=payload,timeout=(5,10))
    except:
        payload["model"]=API_MODEL_BACKUP
        response=requests.post(API_URL,headers=headers,json=payload)

    if response.status_code==200:
        result= response.json()["choices"][0]['message']['content']
        print(result)
        result_match=re.match(r'.*?(\[.*?\])',result,re.DOTALL)
        if result_match!=None:
            return json.loads(result_match.group(1))
        elif re.match(r'.*?({.*?})',result,re.DOTALL)!=None:
            result_match=re.match(r'.*?({.*?})',result,re.DOTALL)           
            return [json.loads(result_match.group(1))]

    else:
        print(f"请求失败，状态码：{response.status_code}，错误信息：{response.text}")


async def OCRImgList(img_list:List[str],struct_key:StructKey):
    ocr_tasks=list(map(lambda item:asyncio.create_task(ModelOcrImg(item,struct_key)),img_list))
    ocr_result= await asyncio.gather(*ocr_tasks)
    result=[]
    for item in ocr_result:
        result.extend(item)
    return list(filter(lambda x:x is not None,result))

if __name__ == "__main__":
    img_path=[r"D:\Program\bdc-service\work\测试数据\20251202\IMG_0005 - 副本 (2).jpg",r"D:\Program\bdc-service\work\测试数据\20251202\IMG_0005 - 副本.jpg",r"D:\Program\bdc-service\work\测试数据\20251202\IMG_0005.jpg"]
    img_path1=r"D:\Program\bdc-service\work\tempimg\借款合同\IMG_0009.jpg"
    res=asyncio.run(ModelOcrImg(img_path1,StructKey.LoanAmount))
    #res=asyncio.run(ModelOcrImg(img_path[0],StructKey.IdCard))
    print(res)
 