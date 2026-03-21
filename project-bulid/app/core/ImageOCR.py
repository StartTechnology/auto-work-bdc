#使用硅基流动APi的免费大模型进行OCR作业
# THUDM/GLM-4.1V-9B-Thinking
# 密钥 sk-zhjfscwkpmrgsybhwdgugrfmjjzwcdoaizenvgrcouothsdo
from typing import List
import requests,asyncio,re,json
import base64
from enum import Enum
API_URL = "https://api.siliconflow.cn/v1/chat/completions"

API_MODEL=["Qwen/Qwen3-VL-32B-Instruct","Pro/moonshotai/Kimi-K2.5","Qwen/Qwen3-VL-235B-A22B-Instruct"]


API_KEY="sk-zhjfscwkpmrgsybhwdgugrfmjjzwcdoaizenvgrcouothsdo"

class StructKey(Enum):
    IdCard=r'{"name":"识别到的姓名(如无则为null)","id":"识别到的身份证号(如无则为null)"}'
    ContractNumber=r'{"contract":"识别到的合同编号(如无则为null)"}'
    LoanAmount=r'{"loan":"识别到的贷款金额数字(纯数字,int类型,如无则为0)"}'
    LoanTerm=r'{"start":"识别到的开始时间(格式:YYmmdd,如无则为null)","end":"识别到的结束时间(格式:YYmmdd,如无则为null)"}'
    RegistrationCertificate=r'{"id":"识别到的完整的抵押登记证明号(通常为"赣（*）*不动产证明第*号"或"**第*号",去除所有空格,如无则为null)"}'
    PropertyCertificate=r'{"id":"识别到的完整的房产证号(通常为"赣（*）*不动产*第*号"或"*房权证*第*号",去除所有空格,如无则为null)"}'


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
        "model": "API_MODEL",  # 模型名称
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{ImgToBase64(img_path)}","detail": "high"}},
                    {"type": "text",
                      "text": f"""请完成以下OCR结构化提取任务：
                            1. 从图片中精准提取指定字段，严格按照以下JSON模板返回结果数组：
                            {struct_key.value}
                            2. 仅返回标准JSON数组格式内容，不添加任何额外文字、注释或说明；
                            3. 如无对应字段，按模板中的默认值（null/0）填充；
                            4. 去除所有空格、换行符，保证JSON格式可直接解析。"""
                          #"OCR提取所有文字，严格返回json数组(如无结果返回空数组)结果："+struct_key.value
                     }
                ]
            }
        ],
        #"prompt":  "请OCR这张图片，并使用如下结构化返回标准json格式结果："+struct_key,
        "temperature":0.3,      # 生成随机性(0-2，建议0.7-1.0)
        "top_p": 0.9,            # 核心采样阈值(0-1，建议0.8-0.95)
        "max_tokens": 1024,      # 最大生成长度(建议512-2048)
        "stream": False, 
        "response_format": {'type': 'json_object'}
    }
    response=''
    for api_model in API_MODEL:
        payload["model"]=api_model
        try:
            response=requests.post(API_URL,headers=headers,json=payload,timeout=(3,30))
            if response.status_code==200:
                print(api_model)
                break
        except Exception as e:
            print(f"模型 {api_model} 请求异常：{str(e)}")
            continue


    if response=='':return [{'status':False}]
    if response.status_code==200:
        result= response.json()["choices"][0]['message']['content']
        print(result)
        result_match=re.match(r'.*?(\[.*?\])',result,re.DOTALL)
        result_value=''
        if result_match!=None:
            result_value=json.loads(result_match.group(1))
        elif re.match(r'.*?({.*?})',result,re.DOTALL)!=None:
            result_match=re.match(r'.*?({.*?})',result,re.DOTALL)           
            result_value= [json.loads(result_match.group(1))]
        return result_value
    else:
        print(f"请求失败，状态码：{response.status_code}，错误信息：{response.text}")
        return [{'status':False}]


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
 