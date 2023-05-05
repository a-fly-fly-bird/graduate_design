import os
import json

filenames = []
filePath = '/Users/lucas/Downloads/A区驾驶分心图像采集数据/11/face_img'
k = os.listdir(filePath)
for filename in k:
    filenames.append(filename.replace(".jpg", ""))

filenames.sort()

print(filenames)

file_name = 'dates.json' #通过扩展名指定文件存储的数据为json格式

with open(file_name,'w') as file_object:
    json.dump(filenames,file_object)