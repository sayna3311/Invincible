from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import time
import cv2 as cv
from Model import Model
import argparse

def get_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--jpp', type=str, default='checkpoints/jpp.pb', help='model checkpoint for JPPNet')
    parser.add_argument('--gmm', type=str, default='checkpoints/gmm.pth', help='model checkpoint for GMM')
    parser.add_argument('--tom', type=str, default='checkpoints/tom.pth', help='model checkpoint for TOM')
    parser.add_argument('--image', type=str, default='image.jpeg', help='input image')
    parser.add_argument('--cloth', type=str, default='cloth.jpeg', help='cloth image')
    opt = parser.parse_args()
    return opt

opt = get_opt()
model = Model(opt.jpp, opt.gmm, opt.tom, use_cuda=False)

cloth = np.array(Image.open(opt.cloth))
plt.imshow(cloth)
plt.show()

image = np.array(Image.open(opt.image))
plt.imshow(image)
plt.show()

start = time.time()
result,trusts = model.predict(image, cloth, need_pre=False, check_dirty=True)
if result is not None:
    end = time.time()
    print("time:"+str(end-start))
    print("Confidence"+str(trusts))
    plt.imshow(result)
    plt.show()
    cv.imwrite('result.jpeg', result)
