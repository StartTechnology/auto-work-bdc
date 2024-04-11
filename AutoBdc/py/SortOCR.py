import os
import shutil
import time
from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()

img_path=r"E:\文档\郭丽华 刘桂根\IMG_0007.jpg"

result, elapse = engine(img_path, use_det=False, use_cls=False, use_rec=True)
for i in result:
    print(i)
#print(result)
#print(elapse)




#file_path = ""
#folder_path = "./_delete_"

def move_file_to_folder(file_path, folder_path):
    try:
        shutil.move(file_path, folder_path)
        print(f"Moved {file_path} to {folder_path}")
    except Exception as e:
        print(f"Error moving file: {e}")


print(time.strftime("%Y%m%d", time.localtime()))