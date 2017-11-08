from Framework.SpiderBase import *
import re, bs4, os, string
from urllib.parse import urlparse

class DemoSpider(SpiderBase):

    inUrl = 'http://www.kaifakuai.com'
    httpFormat = ["http", "https"]
    filiter = ["javascrip:","taobao","javascript:void(0)","#","javascript:history.go"]
    cssFormat = [".css",".ico"]
    domains = [] # 域名参数

    def start(self):
        # 获取域名
        urlParses = urlparse(self.inUrl)
        self.domains.append(urlParses.netloc)
        # 拼接地址，下载页面
        url = self.inUrl + "/index.html"
        self.downFile(url)
        # 执行获取文件
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
                i = i + '/index.html'
            nhrefPathArr.append(i)

        self.setListsDownFiles(urlPathArr,self.inUrl)
        self.setListsDownFiles(srcPathArr, self.inUrl)

        for i in nhrefPathArr:
            if not self.isFileLocal(i):
                continue
            if self.isStrInList(i, self.httpFormat) == 1:
                i = i
            else:
                i = self.inUrl + i
            self.downFile(i)
            self.getHtmlCode(i)

    # 遍历 下载文件
    def setListsDownFiles(self, lists  ,Url  =  ""):
        for i in lists:
            if not self.isFileLocal(i):
                continue
            if self.isStrInList(i, self.httpFormat) == 1:
                nUrl = i
            else:
                nUrl = Url + i
            self.downFile(nUrl)

    # 过滤非法/不需要字段
    def filteringIllegalURL(self,lists ,domain = ''):
        nLists = []
        for i in lists:
            if len(i) < 3:
                continue
            if self.isStrInList(i, self.filiter) == 1:
                continue
            if self.isStrInList(i, self.httpFormat) == 1:
                if self.isStrInList(i, self.domains) == 0:
                    continue
                if len(i) <= len(self.inUrl + "/"):
                    continue
            nLists.append(i)
        return nLists
