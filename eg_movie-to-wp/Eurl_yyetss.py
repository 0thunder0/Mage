import urllib,os,time,random,zhconv,re
from pyquery import PyQuery as pq

class mv_plugin:
    #默认设置：可输入去重用的文件，
    def __init__(self,*args):
        UA=[
           "Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1",
            "Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTMLlikeGecko)Version/5.1Safari/534.50",
            "Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTMLlikeGecko)Version/5.1Safari/534.50",
            "Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTMLlikeGecko)Chrome/17.0.963.56Safari/535.11",
            "Mozilla/5.0(Macintosh;IntelMacOSX10.6;rv:2.0.1)Gecko/20100101Firefox/4.0.1",
            "Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0;",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML like Gecko Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML like Gecko) Maxthon/3.0 Safari/534.12",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML like Gecko Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML like Gecko) Chrome/14.0.835.163 Safari/535.1",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0(compatible;MSIE8.0;WindowsNT6.0;Trident/4.0)",
            "Mozilla/4.0(compatible;MSIE7.0;WindowsNT6.0)",
            "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Trident/4.0;SE2.XMetaSr1.0;SE2.XMetaSr1.0;.NETCLR2.0.50727;SE2.XMetaSr1.0)",
            "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;TheWorld)",
            "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;TencentTraveler4.0)",
            "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Maxthon2.0)",
            "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;AvantBrowser)",
            "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;360SE)",
            "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1)",
            "Mozilla/4.0(compatible;MSIE6.0;WindowsNT5.1)",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)"
        ]
        self.headers={"User-Agent":random.choice(UA)}
        #如果有缓存文件，则提取内容到  self.cacheD
        self.cacheD=[]
        if len(args)>0:
            self.cacheFile=args[0]
            if not os.path.isfile(self.cacheFile):
                os.mknod(self.cacheFile)
            with open(self.cacheFile,'r+') as f:
                self.cacheD=f.readlines()
            for n in range(len(self.cacheD)):
                self.cacheD[n]=self.cacheD[n].replace('\n','')
        #设置屏蔽字
        self.shieldWord=[]
        if len(args)>1:
            with open(args[1],'r+') as f:
                self.shieldWord=f.readlines()
            for w in range(len(self.shieldWord)):
                self.shieldWord[w]=self.shieldWord[w].replace('\n','')
            
    def categoryParse(self):
        urls='http://www.yyetss.com'
        req=urllib.request.Request(urls,headers=self.headers)
        data = urllib.request.urlopen(req).read()
        data=pq(data)
        catItems=data('.index-new-list').items()
        detailUrl=[]
        for item in catItems:
            contentUrl=item('a').attr('href')
            if not re.search(urls,contentUrl):
                contentUrl=urls+contentUrl
            #print(contentUrl)
            yield contentUrl

    def contentParse(self,urls): 
        url=urls
        title=''
        feature_img=''
        imgs=[]
        staff=''
        plot=''
        downloadArea=''
        category=''
        # ______________
        #  print(url)
        req=urllib.request.Request(url,headers=self.headers)
        page_source=urllib.request.urlopen(req).read()
        data=pq(page_source)
        #  print(data)
        title=data('.page-header').text()
        feature_img=data('.container:eq(2) .row .col-sm-9 .row .col-sm-3 img').attr('src')
        plot=data('.container:eq(2) .row .col-sm-9 .row:eq(1)').text()
        #plot=shield(plot)
        #downloadArea=data('.container:eq(2) .row .col-sm-9 .row:eq(3)').html()
        
        Areas=data('.container:eq(2)  .tab_set_info').items()
        for A in Areas:
            As=A('li').items()
            downloadArea=downloadArea+'<p>下载地址：</p><hr>'
            for Ass in As:
                downloadArea=downloadArea+Ass.html()+'<hr>'

        category=data('.breadcrumb li:eq(1)').text()
        #  print(url)
        #  print(title)
        #  print(feature_img)
        #  print(imgs)
        #  print(staff)
        #  print(plot)
        #  print(downloadArea)
        #  print(category)
        return url,title,feature_img,imgs,staff,plot,downloadArea,category
    
    def shield(self,*args):
        for content in args:
            for i in self.shieldWord:
                content=content.repalce(i,'')
            
if __name__=='__main__':
    mv=mv_plugin()
    urlList=mv.categoryParse()
    n=0
    while True:
        url=next(urlList)
        print(url)
        try:
            plot=mv.contentParse(url)
            print(plot)
        except:
            print('这里出现错误')
