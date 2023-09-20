import torch
import numpy as np
from PIL import Image

# yolov5 모델 불러오기
model_path = '/home/pi4/Capstone/yolov5/phone_best.pt'
model = torch.load(model_path)
model.eval() # 모델을 추론 모드로 설정