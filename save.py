import itertools
import os
import shutil
import zipfile
from pathlib import Path
from inference_onnx import getfiles
from config import BaseConfig

def new_filename(filename):
    path = Path(BaseConfig.UPLOAD_FOLDER + '\\' + filename)
    if not path.exists():
        return filename
    for i in itertools.count(1):
        new_path = Path(
            BaseConfig.UPLOAD_FOLDER + '\\' + f'{i}' + str(filename[:-4]) + '.png')
        if not new_path.exists():
            return str(f'{i}' + filename[:-4]) + '.png'


def unpuck(i):
    adress = BaseConfig.UPLOAD_FOLDER + '\\' + i.filename[:-4]
    os.mkdir(adress)
    with zipfile.ZipFile(i, 'r') as zip_file:
        count = len(zip_file.infolist())
        zip_file.extractall(adress)
    for i in getfiles(adress):
        name = new_filename(i)
        shutil.copyfile(adress + '\\' + i, BaseConfig.UPLOAD_FOLDER + '\\' + name)
    shutil.rmtree(adress)
    return count
