import torch
import torch.nn as nn
import torch.nn.functional as F
import cv2
from PIL import Image
import numpy as np
model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', pretrained=True)
model.conv1 = nn.Conv2d(1, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
net = nn.Sequential(  nn.BatchNorm2d(1),
                      model,
                      nn.Linear(1000, 1000,bias=True),
                      # nn.BatchNorm1d(1000),
                      nn.LeakyReLU(0.1),
                      nn.Dropout(0.7),
                      nn.Linear(1000, 2)
                      )


def predict(file):
    net.eval()
    net.load_state_dict(torch.load('catNdog.pth',map_location=torch.device('cpu')))

    img = Image.open(file)          
    img = np.array(img)
    img = cv2.resize(img,(224,224))
    img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)

    result = net(torch.reshape(torch.tensor(img,dtype=torch.float32),\
        (-1,1,224,224)))[0]
    return torch.argmax(result).item()