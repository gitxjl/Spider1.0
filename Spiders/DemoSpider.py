from Framework.SpiderBase import *
import re, bs4, os, string
from urllib import parse

class Demo2Spider(SpiderBase):

    inUrl = 'http://www.kaifakuai.com'
    httpFormat = ["http", "https"]
    filiter = ["javascrip:","taobao","javascript:void(0)","#","javascript:history.go"]
    cssFormat = [".css",".ico"]

    def start(self):
        url = self.inUrl + "/index.html"
        self.downFile(url)
        self.getHtmlCode(url)

    def getHtmlCode(self, url):
        self.log('开始获取：' + url)

        # 判断 url 是否正确
        if self.isStrInList(url, self.httpFormat) != 1:
            self.log('url not is url')
            return

        allHtmlCentent = self.getHtmlObj(url)
        strAllHtmlCentent = str(allHtmlCentent)
        urlPathArr = re.findall(r"url\((.+?)\)", strAllHtmlCentent)
        hrefPathArr = re.findall(r'href="(.+?)"', strAllHtmlCentent)
        srcPathArr = re.findall(r'src="(.+?)"', strAllHtmlCentent)

        srcPathArr = self.filteringIllegalURL(srcPathArr, self.inUrl)
        urlPathArr = self.filteringIllegalURL(urlPathArr, self.inUrl)
        hrefPathArr = self.filteringIllegalURL(hrefPathArr, self.inUrl)

        nhrefPathArr = []
        for i in hrefPathArr:
            if self.isStrInList(i, self.cssFormat) == 1:
                srcPathArr.append(i)
                continue
            if self.isStrInList(i, ['.html']) != 1:
                i = i + 'index.html'
            nhrefPathArr.append(i)

        self.setListsDownFiles(urlPathArr,self.inUrl)
        self.setListsDownFiles(srcPathArr, self.inUrl)

        for i in nhrefPathArr:
            if not self.isFileLocal(i):
                continue
            i = self.inUrl + i
            self.downFile(i)
            self.getHtmlCode(i)

    # 遍历 下载文件
    def setListsDownFiles(self, lists  ,Url  =  ""):
        for i in lists:
            if not self.isFileLocal(i):
                continue
            self.downFile(Url + i)

    # 过滤非法/不需要字段
    def filteringIllegalURL(self,lists ,domain = ''):
        nLists = []
        for i in lists:
            if self.isStrInList(i, self.filiter) == 1:
                continue
            if self.isStrInList(i, self.httpFormat) == 1:
                continue
            if len(i) < 3:
                continue
            nLists.append(i)
        return nLists
