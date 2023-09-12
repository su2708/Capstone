from glob import glob
img_list = glob('C:\\yolov5\\dataset\\train\\images\\*.jpg')
print(len(img_list))
val_list = glob('C:\\yolov5\\dataset\\test\\images\\*.jpg')
print(len(val_list))
test_list = glob('C:\\yolov5\\dataset\\valid\\images\\*.jpg')
print(len(test_list))

with open('C:\\yolov5\\dataset\\train.txt','w') as f:
  f.write('\n'.join(img_list)+'\n')
with open('C:\\yolov5\\dataset\\valid.txt','w') as f:
  f.write('\n'.join(val_list)+'\n')
with open('C:\\yolov5\\dataset\\test.txt','w') as f:
  f.write('\n'.join(test_list)+'\n')
  
  
import yaml
with open ('C:\\yolov5\\dataset\\data.yaml','r') as f :
  data = yaml.safe_load(f)
print(data)
data['train']='C:\\yolov5\\dataset\\train.txt'
data['val']='C:\\yolov5\\dataset\\val.txt'
data['test']='C:\\yolov5\\dataset\\test.txt'
with open('\\yolov5\\dataset\\data.yaml','w') as f :
  yaml.dump(data, f)
print(data)