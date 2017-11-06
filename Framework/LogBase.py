import time, os, re


class LogBase:
    def __init__(self):
        pass

    def readText(filePath, encoding='utf-8'):

        f = open(filePath, 'r', encoding=encoding)
        strOut = ''
        for line in f.readlines():
            strOut += re.sub('([^:]//.*"?$)|(/\*(.*?)\*/)', '', line)
        f.close()
        return strOut

    def writeText(filePath, text):

        path = os.path.dirname(filePath)
        if not os.path.exists(path):
            os.makedirs(path)

        f = None

        if not os.path.isfile(filePath):
            f = open(filePath, 'w', encoding='utf-8')
        else:
            f = open(filePath, 'a', encoding='utf-8')
        print(text)
        f.write(text + "\n")
        f.close()

    def writeTextDaybyDay(path, text, extension='log'):

        date = time.strftime('%Y-%m-%d', time.localtime(time.time()))

        filePath = os.path.join(path, date + '.' + extension)

        LogBase.writeText(filePath, text)
