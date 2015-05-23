# coding: utf-8
import os

path = os.getcwd()
fileList = []

for root, dirs, files in os.walk(path):
    for file in files:
        if '.scss' in file:
            # fileList.append(os.path.join(root,file))
            os.chdir(root)
            print os.path.abspath('../../part')

print fileList

f = open(fileList[0], 'r')
importList = []
commentFlg = False


styl = f.read()
print styl

f.close()