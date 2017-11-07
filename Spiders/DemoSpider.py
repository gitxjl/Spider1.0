from Framework.SpiderBase import *
import re, bs4, os, string
from urllib import parse


class DemoSpider(SpiderBase, UrlBase):
    inUrl = 'http://www.kaifakuai.com'
    picFormat = [".jpg", ".jpeg", ".png", ".gif"]
    httpFormat = ["http", "https"]
    filiter = ["javascript:", "taobao"]
    suffix = ["index.html"]
    cssFormat = [".css"]
    isPass = 0

    def start(self):
        self.getHtmlCode(self.inUrl)

    def getHtmlCode(self, url):

        html_all = []  # html 页面地址
        src_all = []  # 图片地址
        link_all = []  # 样式 ico 文件地址
        script_all = []  # 脚本地址
        setHtmlUrlLists = []  # 再次访问地址
        cssPathLists = []  # 样式文件地址

        # 判断 url 是否正确
        if self.isStrInList(url, self.httpFormat) == 1:

            allHtmlCentent = self.getHtmlObj(url)

            aLabelAll = allHtmlCentent.findAll('a')
            imgLabelAll = allHtmlCentent.findAll('img')
            linkLabelAll = allHtmlCentent.findAll('link')
            scriptLabelAll = allHtmlCentent.findAll('script')

            # href 获取
            for val in aLabelAll:
                href = val['href']
                if len(href) < 2:
                    continue
                if self.isStrInList(href, self.filiter) == 1:
                    continue
                if self.isStrInList(href, self.httpFormat) == 1:
                    htmlUrl = href
                else:
                    if self.isStrInList(href, self.suffix) == 1:
                        htmlUrl = href
                        self.log(href)
                    else:
                        htmlUrl = self.inUrl + href + 'index.html'
                        setHtmlUrlLists.append(htmlUrl)
                html_all.append(htmlUrl)

            # img src 获取
            for val in imgLabelAll:
                src = val['src']
                if len(src) < 1:
                    continue
                if self.isStrInList(src, self.filiter) == 1:
                    continue
                if self.isStrInList(src, self.httpFormat) == 1:
                    srcUrl = src
                else:
                    srcUrl = self.inUrl + src
                src_all.append(srcUrl)

            # link 获取
            for val in linkLabelAll:
                link = val['href']
                if len(link) < 1:
                    continue
                if self.isStrInList(link, self.filiter) == 1:
                    continue
                if self.isStrInList(link, self.httpFormat) == 1:
                    linkUrl = link
                else:
                    linkUrl = self.inUrl + link
                    cssPathLists.append(link)
                link_all.append(linkUrl)

            # script 获取
            for val in scriptLabelAll:
                if 'src="' not in str(val):
                    continue
                src = val['src']
                if self.isStrInList(src, self.filiter) == 1:
                    continue
                if self.isStrInList(src, self.httpFormat) == 1:
                    scriptUrl = src
                else:
                    scriptUrl = self.inUrl + src
                script_all.append(scriptUrl)

            # 下载图片
            self.setListsDownFiles(src_all)

            # 下载 html 页面
            self.setListsDownFiles(html_all)

            # 下载样式 ico
            self.setListsDownFiles(link_all)

            # 下载样式内 图片文件
            for i in cssPathLists:
                if self.isStrInList(i, self.cssFormat) != 1:
                    continue
                self.getCssImgFile(i, self.inUrl)

            # 下载js 文件
            self.setListsDownFiles(script_all)

            # 循环下载其他页面
            for i in setHtmlUrlLists:
                if i == self.inUrl: self.isPass = 1
                if self.isPass and i == self.inUrl == 1: continue
                self.getHtmlCode(i)

    # 遍历 下载文件
    def setListsDownFiles(self, lists):
        for i in lists:
            self.downFile(i)
