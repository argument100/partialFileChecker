# coding: utf-8
import os, re, json

path = os.getcwd()
base = os.path.dirname(os.path.abspath(__file__))
extList = ['.styl', '.scss', '.sass', '.less']

pattern = re.compile('/\*([^/]|[^*]/)*\*/', re.DOTALL)
pattern2 = re.compile('//.*')


# ファイル内からimportを探す
def getImport(files, dict):
    id = files[0]
    root = files[1]
    name = files[2]
    ext = files[3]
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
        quotes = '"'
        filepath = ''
        filename = ''
        i = styl.find('@import', i)
        if i <= 0:
            break
        posS = styl.find(quotes, i, i + 10)
        # ダブルクォーテーションを使ってなかったらシングルに変更
        if posS <= 0:
            quotes = "'"
            posS = styl.find(quotes, i)
        posE = styl.find(quotes, posS + 1)
        pathname = styl[posS+1:posE]
        boundary = pathname.rfind('/')
        if boundary == -1:
            filepath = ''
            filename = pathname[boundary+1:]
        else:
            filepath = pathname[:boundary+1]
            filename = pathname[boundary+1:]

        key = os.path.abspath(filepath).replace(base, '') + '/' + filename + ext

        if key in dict:
            dict[key].append(id.replace(base, ''))
        else:
            dict[key] = [(id.replace(base, ''))]
        i = posE
    return dict

# 訪問リスト作成
def getFileList():
    fileList = []
    for root, dirs, files in os.walk(path):
        for file in files:
            for ext in extList:
                if ext in file:
                    fileList.append([os.path.join(root,file), root, file, ext])
                    break
    return fileList

# report作成
def makeReport(dict):
    # reportディレクトリが無かったら作って移動
    if os.path.exists(path + '/report/') == False:
        os.mkdir('report')
    os.chdir(path + '/report/')
    # str = ''
    # for k, v in dict.items():
    #     str += '\r\n'
    #     str += '■パーシャル名：' + k + '\r\n\r\n'
    #     for li in v:
    #         str += li + '\r\n'
    #     str += '\r\n'

    # report = open('report.txt', 'w')
    # report.write(str)
    # report.close()
    report = open('report.json', 'w')
    report.write(json.dumps(dict, sort_keys=True, indent=4))
    report.close()

def init():
    partialDict = {}
    fileList = getFileList()
    for list in fileList:
        partialDict = getImport(list, partialDict)
    os.chdir(path)
    makeReport(partialDict)

init()












