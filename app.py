# coding: utf-8
import os, re

path = os.getcwd()
fileList = []
partialList = []
ext = '.styl'

pattern = re.compile('/\*([^/]|[^*]/)*\*/', re.DOTALL)
pattern2 = re.compile('//.*')

# 訪問リスト作成
for root, dirs, files in os.walk(path):
    for file in files:
        if ext in file:
            fileList.append([os.path.join(root,file), root, file])

# ファイル内からimportを探す
def getImport(files):
    id = files[0]
    root = files[1]
    name = files[2]
    importList = []
    i = 0


    # ディレクトリ移動
    os.chdir(root)
    f = open(id, 'r')
    styl = f.read()
    f.close()
    # コメントアウト分を削除
    styl = pattern.sub('', styl)
    styl = pattern2.sub('', styl)
    # print styl

    # @importを探す
    while True:
        filepath = ''
        filename = ''
        i = styl.find('@import', i)
        if i <= 0:
            break
        posS = styl.find('"', i)
        posE = styl.find('"', posS + 1)
        pathname = styl[posS+1:posE]
        boundary = pathname.rfind('/')
        if boundary == -1:
            filepath = ''
            filename = pathname[boundary+1:]
        else:
            filepath = pathname[:boundary+1]
            filename = pathname[boundary+1:]

        importList.append(os.path.abspath(filepath) + '/' + filename + ext)
        i = posE
    return [id, importList]

for list in fileList:
    partialList.append(getImport(list))

str = ''
for lists in partialList:
    str += '\r\n'
    str += '■ファイルの名前：' + lists[0] + '\r\n\r\n'
    for li in lists[1]:
        str += li + '\r\n'
    str += '\r\n'

os.chdir(path)

report = open('report.txt', 'w')
report.write(str)
report.close()














