# -*- coding: utf-8 -*-

import requests, os, time, json, re
from Framework.LogBase import LogBase
from bs4 import BeautifulSoup


class SpiderBase:
    config = {}
    request = requests

    def __init__(self):
        # 加载配置文件
        self.config = json.loads(LogBase.readText('./config.json'))

    # 普通日志写入
    def log(self, text):
        self.__writeText(self.config['logPath']['log'], text)

    # 错误日志写入
    def logError(self, text):
        self.__writeText(self.config['logPath']['error'], text)

    # 转换对象数据
    def htmlToObj(self, html):
        return BeautifulSoup(html, "html.parser")

    # 判断字符串是否属于该列表
    def isStrInList(self,str,list):
        for i in list:
            if i in str:
                return 1
        return 0

    # 判断是否活动地址
    def isUrlLink(self, url, decode='utf-8'):

        htmlRequest = self.request.get(url)

        if htmlRequest.status_code == 200:
            return 1
        else:
            return 0

    def getHtmlObj(self, url, decode='utf-8'):

        htmlRequest = self.request.get(url)
        html = htmlRequest.text.encode(htmlRequest.encoding).decode(decode)

        if htmlRequest.status_code == 200:
            return self.htmlToObj(html)
        else:
            return False

    def downPicReturn(self, item):
        if isinstance(item, dict):
            item2 = item
            for k, v in item2.items():
                if isinstance(v, str):
                    if v.find('.jpg') >= 0 or v.find('.jpeg') >= 0 or v.find('.gif') >= 0 or v.find('.png') >= 0:
                        if v.find('http:') == 0:
                            item[k] = self.downFile(v)
                        else:
                            item[k] = self.downPicReturn(v)
        elif isinstance(item, str):
            if item.find('.jpg') >= 0 or item.find('.jpeg') >= 0 or item.find('.gif') >= 0 or item.find('.png') >= 0:
                objHtml = BeautifulSoup(item, "html.parser")
                imglist = objHtml.findAll('img')
                for imgItem in imglist:
                    newSrc = self.downFile(imgItem['src'])
                    imgItem['src'] = newSrc
                item = objHtml.prettify()
        return item

    # 读取css样式文件内容获取图片地址 下载图片
    def getCssImgFile(self,files,url = ''):
        fileObject = open(self.config['imgPath'] + files , 'rb')
        try:
            allTheText = fileObject.read()
            fileObject.close()
            urlPathArr = re.findall(r"url\((.+?)\)", str(allTheText))
            for i in urlPathArr:
                self.downFile(url+i)
        finally:
            fileObject.close()

    # 通过 url 获取路径
    def getUrlPath(self, url):
        # 获取文件路径
        return re.match('http.*?://.*?/(.*)', url).group(1)

    # 文件下载
    def downFile(self, url, spath = ''):
        pathFile = url
        try:
            # 获取文件路径
            file=re.match('http.*?://.*?/(.*)', url).group(1)
            if file.find('/')==0:file=file[1:]
            pathFile = self.config['imgPath'] + file
            # 获取文件内容
            ir = requests.get(url)
            if ir.status_code == 200:
                path = os.path.dirname(pathFile)
                # 判断存放路径是否存在
                if not os.path.exists(path): os.makedirs(path)
                # 判断本地文件是否存在
                if not os.path.exists(pathFile):
                    # 写入文件
                    open(pathFile, 'wb').write(ir.content)
                    self.log(url + "下载成功")
                else:
                    self.log(url + "文件已存在：跳过")
            else:
                return None
        except:
            self.logError(url + "下载失败")
            return None

        return '/uploadfiles/' + pathFile.replace(self.config['imgPath'], '')

    # 写人文件信息
    def __writeText(self, path, text):
        if self.config['print']['logOrErrorPrint']:
            text = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "\t" + str(text)
        LogBase.writeTextDaybyDay(path, text)
