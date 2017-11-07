from Framework.SpiderBase import *
import re, bs4, os, string
from urllib import parse

class Demo1Spider(SpiderBase):


    inUrl = 'http://www.kaifakuai.com/index.html'
    picFormat = [".jpg", ".jpeg", ".png", ".gif"]
    httpFormat = ["http", "https"]
    filiter = ["javascrip:","taobao","javascript:void(0)"]
    cssFormat = [".cs",".ico",".html"]
    isPass = ''
    number = 0
    saveHtml = []

    def start(self):
        self.getHtmlCode(self.inUrl)

    def getHtmlCode(self, url):
        urlPathArr = []
        hrefPathArr = []
        srcPathArr = []
        src_all = []  # 图片地址

        # 判断 url 是否正确
        if self.isStrInList(url, self.httpFormat) == 1:
            allHtmlCentent = self.getHtmlObj(url)
            strAllHtmlCentent = str(allHtmlCentent)
            urlPathArr = re.findall(r"url\((.+?)\)", strAllHtmlCentent)
            hrefPathArr = re.findall(r'href="(.+?)"', strAllHtmlCentent)
            srcPathArr = re.findall(r'src="(.+?)"', strAllHtmlCentent)

            # 下载页面内样式图片/脚本图片
            self.setListsDownFiles(urlPathArr,self.inUrl)

            # 下载页面内 图片/脚本文件
            self.setListsDownFiles(srcPathArr, self.inUrl)

            # 下载样式内 图片文件
            nCssPathArr = []
            nHrefPathArr = []
            for i in hrefPathArr:
                if self.isStrInList(i, ['.css']) == 1:
                    nCssPathArr.append(i)
                if self.isStrInList(i, self.filiter) == 1:
                    continue
                if self.inUrl == i:
                    continue
                if self.inUrl + "/" == i:
                    continue
                if self.isStrInList(i, self.httpFormat) == 1:
                    i = self.getUrlPath(i + '/')
                    if len(i) <= 1:
                        continue
                if self.isStrInList(i, self.cssFormat) != 1:
                    i = i + 'index.html'
                if self.isStrInList(i, self.saveHtml) == 1:
                    continue
                nHrefPathArr.append(self.inUrl + i)
                self.saveHtml.append(self.inUrl + i)

            # self.log(nHrefPathArr)
            # os._exit(0)

            # 下载页面文件
            self.setListsDownFiles(nHrefPathArr)

            # 下载样式内 图片文件
            for i in nCssPathArr:
                self.getCssImgFile(i, self.inUrl)
            self.number = self.number + 1
            self.log(self.number)

            # self.log(nHrefPathArr)
            # os._exit(0)

            for i in nHrefPathArr:
                if self.isStrInList(i, ['.html']) != 1:
                    continue
                self.isPass = i
                self.getHtmlCode(i)

    # 遍历 下载文件
    def setListsDownFiles(self, lists  ,Url  =  ""):
        for i in lists:
            if self.isStrInList(i, self.filiter) == 1:
                continue
            self.downFile(Url + i)