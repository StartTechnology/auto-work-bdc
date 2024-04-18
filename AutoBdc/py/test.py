import os

image_path=r"C:\Users\dkzx\Desktop\Lcy-抵押登记\影像\解押\20240417\曾小华"

image_list=os.listdir(image_path)

for i in image_list:
    image_path_dir=os.path.join(image_path,i)

    if os.path.isdir(image_path_dir):
        files=os.listdir(image_path_dir)
        for i_img in files:
            image_path_dir_file=os.path.join(image_path_dir,i_img)
            

            
            if os.path.isfile(image_path_dir_file):
                print(image_path_dir_file)
