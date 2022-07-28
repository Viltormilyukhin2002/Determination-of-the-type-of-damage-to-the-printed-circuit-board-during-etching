'''
Created on May 31, 2022

@author: esamkin
'''
import os

import cv2
import numpy as np
import onnxruntime as ort
from config import BaseConfig

CLASSES = {
    3: ['11', 'DEFECT'],
    5: ['13', 'DEFECT'],
    15: ['22', 'NORM'],
    4: ['12', 'NORM'],
    20: ['4', 'NORM'],
    23: ['7', 'DEFECT'],
    24: ['8', 'NORM'],
    11: ['19', 'NORM'],
    16: ['23', 'DEFECT'],
    2: ['10', 'NORM'],
    1: ['1', 'NORM'],
    6: ['14', 'NORM'],
    12: ['2', 'NORM'],
    9: ['17', 'DEFECT'],
    8: ['16', 'DEFECT'],
    10: ['18', 'DEFECT'],
    22: ['6', 'DEFECT'],
    21: ['5', 'NORM'],
    13: ['20', 'NORM'],
    7: ['15', 'DEFECT'],
    18: ['25', 'DEFECT'],
    14: ['21', 'NORM'],
    17: ['24', 'DEFECT'],
    19: ['3', 'NORM'],
    25: ['9', 'DEFECT'],
    0: ['0', 'NORM']
}


def getfiles(dirpath):
    a = [s for s in os.listdir(dirpath)
         if os.path.isfile(os.path.join(dirpath, s))]
    a.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
    return a


def read_imges(img, cad, mean=0, std=1):
    img = cv2.imread(img, 0)
    cad = cv2.imread(cad, 0)
    assert (img.shape == (64, 64)) and (cad.shape == (64, 64)), 'размерности не соответствуют входу сети'
    return np.expand_dims((np.stack((img, cad,), axis=0) - mean) / std, axis=0).astype(np.float32)


def post_proc(a, t=1):
    # a = np.exp(a/t)
    a = a.clip(min=0)
    return a / np.sum(a, axis=-1)


def script(n):
    files = getfiles(BaseConfig.UPLOAD_FOLDER)
    model = "vgg.onnx"
    test_dir = os.path.expanduser(BaseConfig.UPLOAD_FOLDER)  # папка с тестовыми изобр.
    mean = np.array([[[129.979]], [[140.136]]])
    std = np.array([[[77.293]], [[126.872]]])

    session = ort.InferenceSession(model, None)
    result = {}
    for img in files[-n:]:
        if img.find('Image.png') == -1:
            continue
        img_ = os.path.join(test_dir, img)
        cad = img_.replace('Image', 'Cad')
        if not os.path.exists(cad):
            # пропускаем файлы без пары
            continue
        data = read_imges(img_, cad, mean, std)
        result[img] = post_proc(session.run([], {'data': data})[0])
    # for k,v in result.items():
    # predicted_class = np.argmax(v)
    # print(v)
    # имя файла, метка класса, расперделение уверенности в ответе
    # print(f"{k}\t{CLASSES[predicted_class]}\t{v.flatten()[predicted_class]}")
    return result.items()
