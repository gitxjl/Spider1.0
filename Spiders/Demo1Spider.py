from Framework.SpiderBase import *
import re, bs4, os, string
from urllib import parse

class Demo1Spider(SpiderBase):
    picFormat = [".jpg", ".jpeg", ".png", ".gif"]
    httpFormat = ["http", "https"]
    filiter = ["javascript:","taobao"]
    suffix = ["index.html"]
    inUrl = 'http://www.kaifakuai.com'
    cssFormat = [".css",".ico",".html"]
    htmlLists = []
    isPass = 0

    attrLists = ['src','href']

    def start(self):
        self.getHtmlCode(self.inUrl)

    def getHtmlCode(self, url):
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
            self.setListsDownFiles(srcPathArr,self.inUrl)

            # 下载样式内 图片文件
            nCssPathArr = []
            nHrefPathArr = []
            for i in hrefPathArr:
                if self.isStrInList(i, ['.css']) == 1:
                    nCssPathArr.append(i)
                if self.isStrInList(i, self.filiter) == 1:
                    continue
                if self.isStrInList(i, self.httpFormat) == 1:
                    i = self.getUrlPath(i + '/')
                    if len(i) <= 1:
                        continue
                if self.isStrInList(i, self.cssFormat) != 1:
                    i = i + 'index.html'
                nHrefPathArr.append(self.inUrl + i)

            # 下载页面文件
            self.setListsDownFiles(nHrefPathArr)

            # 下载样式内 图片文件
            for i in nCssPathArr:
                self.getCssImgFile(i, self.inUrl)

            for i in nHrefPathArr:
                if self.isStrInList(i, ['.html']) != 1:
                    continue
                self.getHtmlCode(i)

    # 遍历 下载文件
    def setListsDownFiles(self, lists ,iUrl = ""):
        for i in lists:
            self.downFile(iUrl + i)