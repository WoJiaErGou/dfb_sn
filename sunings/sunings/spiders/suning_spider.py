import scrapy
from sunings.items import SuningsItem
from scrapy import Selector
import requests
import re
import json
import time
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
class Suning_spider(scrapy.Spider):
    name = "sn_DFB"
    allowed_domain = ['suning.com']
    start_urls =['https://list.suning.com/0-20329-0.html']
    def parse(self, response):
        '''
        信息条数为3500+
        '''
        max_page = response.xpath(".//div[@id='filter-results']/div[@id='bottom_pager']/span[@class='page-more']/text()").extract()[0]
        results=response.xpath(".//span[@class='total-result']/strong[@id='totalNum']/text()").extract()[0]
        max_number = re.findall('共(.*?)页',max_page)[0]
        print('苏宁电饭煲搜索结果页面为'+max_number+'页')
        print('电饭煲一共有'+results+'个')
        for i in range(0,int(max_number)+1):
            pro_url='https://list.suning.com/0-20329-%d.html' % i
            print(pro_url)
            try:
                yield scrapy.Request(url=pro_url,callback=self.list_parse,dont_filter=True)
            except:
                time.sleep(3)
                yield scrapy.Request(url=pro_url, callback=self.list_parse, dont_filter=True)
            # break
    def list_parse(self,response):
        for url in response.xpath(".//div[@class='wrap']"):
            product_url_m=url.xpath(".//p[@class='sell-point']/a/@href").extract()[0]
            #商品的url提取
            product_url="https:"+product_url_m[:]
            #商品名称与之前不同，以列表得到，转化为字符串
            may_name_list=url.xpath(".//p[@class='sell-point']/a/text()").extract()
            may_name=''
            for each in may_name_list:
                may_name=may_name[:]+each
                if each != may_name_list[-1]:
                    may_name=may_name[:]+' '
            may_name=re.sub(r'\n','',may_name)
            if '' == may_name[-1]:
                may_name=may_name[:-2]
            print(may_name)
            #店铺名称
            shop_name=url.xpath(".//p[4]/@salesname").extract()[0]
            #产品ID
            ProductID=product_url_m.split('/')[-1].split('.')[0]
            #对应商品详情页的请求ID
            urlID=product_url_m.split('/')[-2]
            #实例化item
            # url='https://www.google.com.hk/'
            item=SuningsItem(ProductID=ProductID,urlID=urlID,may_name=may_name,shop_name=shop_name,product_url=product_url)
            request=scrapy.Request(url=product_url,callback=self.product_parse,meta={'item':item},dont_filter=True)
            yield request
    def product_parse(self,response):
        # print(response.url)
        item=response.meta['item']
        ProductID=item['ProductID']
        urlID=item['urlID']
        may_name=item['may_name']
        shop_name=item['shop_name']
        #品牌
        try:
            brand = Selector(response).re('"brandName":"(.*?)"')[0]
        except:
            try:
                brand=Selector(response).re('<li><b>品牌</b>：(.*?)</li>')[0]
            except:
                try:
                    brand=re.findall('"brandName":"(.*?)"',response.text)[0]
                except:
                    brand = None
        #去掉品牌括号内容
        if brand:
            if re.findall(r'（.*?）', brand):
                re_com = re.compile('（.*?）')
                brand = brand[:0] + re.sub(re_com, '', brand)
        if brand:
            if re.findall(r'\(.*?\)', brand):
                re_cn = re.compile('\(.*?\)')
                brand = brand[:0] + re.sub(re_cn, '', brand)
        #容量
        try:
            capacity=Selector(response).re('容量：(.*?)</li>')[0]
        except:
            try:
                capacity=Selector(response).re('容量</span> </div> </td> <td class="val">(.*?)</td>')[0]
            except:
                try:
                    capacity=re.findall('容量：(.*?)</li>',response.text)[0]
                except:
                    capacity=None
        #颜色
        try:
            color=Selector(response).re('颜色：(.*?)</li>')[0]
        except:
            try:
                color=Selector(response).re('颜色</span> </div> </td> <td class="val">(.*?)</td>')[0]
            except:
                try:
                    color=re.findall('颜色：(.*?)</li>',response.text)[0]
                except:
                    color=None
        #类型，商品型号
        try:
            p_Name = Selector(response).re('型号</span> </div> </td> <td class="val">(.*?)</td>')[0]
        except:
            try:
                p_Name=re.findall('型号</span> </div> </td> <td class="val">(.*?)</td>',response.text)[0]
                if p_Name==None:
                    p_Name=re.findall('型号</span> </div> </td> <td class="val">(.*?)</td>',response.text)[0]
            except:
                p_Name=None
        if p_Name:
            if brand:
                if brand in p_Name:
                    pass
                else:
                    p_Name=brand+p_Name[:]
        if p_Name:
            if re.findall(r'（.*?）', p_Name):
                re_com = re.compile('（.*?）')
                p_Name = p_Name[:0] + re.sub(re_com, '', p_Name)
        if p_Name:
            if re.findall(r'\(.*?\)', p_Name):
                re_cn = re.compile('\(.*?\)')
                p_Name = p_Name[:0] + re.sub(re_cn, '', p_Name)
        print(p_Name)

        #功能
        try:
            jiare=Selector(response).re('(加热方式：.*?)</li>')[0]
        except:
            try:
                jiare_may=Selector(response).re('加热方式</span> </div> </td> <td class="val">(.*?)</td>')[0]
                jiare='加热方式：'+jiare_may
            except:
                try:
                    jiare=re.findall('(加热方式：.*?)</li>',response.text)[0]
                except:
                    jiare=None
        print(jiare)
        try:
            kongzhi = Selector(response).re('(控制方式：.*?)</li>')[0]
        except:
            try:
                kongzhi_may = Selector(response).re('控制方式</span> </div> </td> <td class="val">(.*?)</td>')[0]
                kongzhi = '控制方式：' + kongzhi_may
            except:
                try:
                    kongzhi = re.findall('(控制方式：.*?)</li>', response.text)[0]
                except:
                    kongzhi = None
        print(kongzhi)
        try:
            yuyue = Selector(response).re('(预约功能：.*?)</li>')[0]
        except:
            try:
                yuyue_may = Selector(response).re('预约功能</span> </div> </td> <td class="val">(.*?)</td>')[0]
                yuyue = '预约功能：' + yuyue_may
            except:
                try:
                    yuyue = re.findall('(预约功能：.*?)</li>', response.text)[0]
                except:
                    try:
                        yuyue_may=Selector(response).re('预约定时</span> </div> </td> <td class="val">(.*?)</td>')[0]
                        yuyue='预约定时：'+yuyue_may
                    except:
                        yuyue = None
        print(yuyue)
        if jiare or kongzhi or yuyue:
            X_type=''
            if jiare:
                X_type=X_type[:]+jiare+' '
            if kongzhi:
                X_type=X_type[:]+kongzhi+' '
            if yuyue:
                X_type=X_type[:]+yuyue
            if len(X_type) < 1:
                X_type=None
        else:
            X_type=None
        #核心参数
        type='"'
        soup=BeautifulSoup(response.text,'lxml')
        try:
            ul = soup.find('ul', attrs={'class': 'cnt clearfix'})
            li = ul.find_all('li')
            for i in range(len(li)):
                type=type[:]+li[i].text
                if i < len(li)-1:
                    type=type[:]+' '
                if i == len(li)-1:
                    type=type[:]+'"'
        except:
            try:#部分核心参数格式更改
                div = soup.find('div', class_='prod-detail-container')
                ul = div.find('ul', attrs={'class': 'clearfix'})
                li = ul.find_all('li')
                for each in li:
                    li_li = each.find_all('li')
                    for i in range(len(li_li)):
                        type = type[:] + li_li[i].text
                        if i < len(li_li) - 1:
                            type = type[:] + ' '
                        if i == len(li_li) - 1:
                            type = type[:] + '"'
            except:
                type =None
        special=Selector(response).re('核心参数')
        print(special)
        if type == None:
            try:
                parameter_id=Selector(response).re('"mainPartNumber":"(.*?)"')[0]
            except:
                try:
                    parameter_id=re.findall('"mainPartNumber":"(.*?)"',response.text)[0]
                except:
                    parameter_id=None
                    type=None
            if parameter_id:
                try:
                    parameter_id=Selector(response).re('"mainPartNumber":"(.*?)"')[0]
                    parameter_url = 'https://product.suning.com/pds-web/ajax/itemParameter_%s_R0105002_10051.html' % parameter_id
                    para_response=requests.get(parameter_url).text
                    time.sleep(1)
                except:
                    print('尝试获取参数url失败！')
                try:
                    eles = re.findall('"snparameterdesc":"(.*?)"', para_response)
                    souls = re.findall('"snparameterVal":"(.*?)"', para_response)
                    try:
                        type = '"'
                        for i in range(len(eles)):
                            type=type[:]+eles[i] + ':' + souls[i]
                            if i < len(eles)-1 :
                                type=type[:]+' '
                            if i == len(eles)-1 :
                                type = type[:] + '"'
                    except:
                        type=None
                    try:
                        brand=re.findall('"snparameterdesc":"品牌","snparameterVal":"(.*?)"',para_response)[0]
                    except:
                        brand=None
                    try:
                        capacity=re.findall('"snparameterdesc":"容量","snparameterVal":"(.*?)"',para_response)[0]
                    except:
                        capacity=None
                    try:
                        p_Name=re.findall('"snparameterdesc":"型号","snparameterVal":"(.*?)"',para_response)[0]
                    except:
                        p_Name=None
                    if p_Name:
                        if brand:
                            if brand in p_Name:
                                pass
                            else:
                                p_Name = brand + p_Name[:]
                    if p_Name:
                        if re.findall(r'（.*?）', p_Name):
                            re_com = re.compile('（.*?）')
                            p_Name = p_Name[:0] + re.sub(re_com, '', p_Name)
                    if p_Name:
                        if re.findall(r'\(.*?\)', p_Name):
                            re_cn = re.compile('\(.*?\)')
                            p_Name = p_Name[:0] + re.sub(re_cn, '', p_Name)
                    print(p_Name)
                    try:
                        jiare_may=re.findall('"snparameterdesc":"加热方式","snparameterVal":"(.*?)"',para_response)[0]
                        jiare='加热方式：'+jiare_may
                    except:
                        jiare=None
                    try:
                        kongzhi_may = re.findall('"snparameterdesc":"控制方式","snparameterVal":"(.*?)"', para_response)[0]
                        kongzhi = '控制方式：' + kongzhi_may
                    except:
                        kongzhi=None
                    try:
                        yuyue_may = re.findall('"snparameterdesc":"预约功能","snparameterVal":"(.*?)"', para_response)[0]
                        yuyue = '预约功能：' + yuyue_may
                    except:
                        yuyue=None
                    if jiare or kongzhi or yuyue:
                        X_type = ''
                        if jiare:
                            X_type = X_type[:] + jiare + ' '
                        if kongzhi:
                            X_type = X_type[:] + kongzhi + ' '
                        if yuyue:
                            X_type = X_type[:] + yuyue
                        if len(X_type) < 1:
                            X_type = None
                    else:
                        X_type = None
                except:
                       type=None
        # 获取相关请求url
        keyword_url = 'https://review.suning.com/ajax/getreview_labels/general-000000000' + ProductID + '-' + urlID + '-----commodityrLabels.htm'
        comment_url = 'https://review.suning.com/ajax/review_satisfy/general-000000000' + ProductID + '-' + urlID + '-----satisfy.htm'
        price_url = 'https://pas.suning.com/nspcsale_0_000000000' + ProductID + '_000000000' + ProductID + '_' + urlID + '_10_010_0100101_20268_1000000_9017_10106_Z001.html'
        # 获取印象关键字
        try:
            keyword_response = requests.get(keyword_url).text
            keyword_text = json.loads(re.findall(r'\((.*?)\)', keyword_response)[0])
            keyword_list = keyword_text.get('commodityLabelCountList')
            key_str = '"'
            keyword = []
            for i in range(len(keyword_list)):
                key_str = key_str[:] + keyword_list[i].get('labelName')
                if i < len(keyword_list) - 1:
                    key_str = key_str[:] + ' '
                if i == len(keyword_list) - 1:
                    key_str = key_str[:] + '"'
            keyword.append(key_str)
        except:
            keyword = None
        # 获取评价信息
        try:
            comment_response = requests.get(comment_url).text
            comment_text = json.loads(re.findall(r'\((.*?)\)', comment_response)[0])
            comment_list = comment_text.get('reviewCounts')[0]
            # 差评
            PoorCount = comment_list.get('oneStarCount')
            twoStarCount = comment_list.get('twoStarCount')
            threeStarCount = comment_list.get('threeStarCount')
            fourStarCount = comment_list.get('fourStarCount')
            fiveStarCount = comment_list.get('fiveStarCount')
            # 评论数量
            CommentCount = comment_list.get('totalCount')
            # 好评
            GoodCount = fourStarCount + fiveStarCount
            # 中评
            GeneralCount = twoStarCount + threeStarCount
            # 好评度
            # 得到百分比取整函数
            if CommentCount != 0:
                goodpercent = round(GoodCount / CommentCount * 100)
                generalpercent = round(GeneralCount / CommentCount * 100)
                poorpercent = round(PoorCount / CommentCount * 100)
                commentlist = [GoodCount, GeneralCount, PoorCount]
                percent_list = [goodpercent, generalpercent, poorpercent]
                # 对不满百分之一的判定
                for i in range(len(percent_list)):
                    if percent_list[i] == 0 and commentlist[i] != 0 and CommentCount != 0:
                        percent_list[i] = 1
                nomaxpercent = 0  # 定义为累计不是最大百分比数值
                # 好评度计算url='http://res.suning.cn/project/review/js/reviewAll.js?v=20170823001'
                if CommentCount != 0:
                    maxpercent = max(goodpercent, generalpercent, poorpercent)
                    for each in percent_list:
                        if maxpercent != each:
                            nomaxpercent += each
                    GoodRateShow = 100 - nomaxpercent
                else:
                    GoodRateShow = 100
        except:
            PoorCount=0
            CommentCount=0
            GoodCount=0
            GeneralCount=0
            GoodRateShow=100
        # 有关价格
        try:
            price_response = requests.get(price_url).text
        except requests.RequestException as e:
            print(e)
            time.sleep(2)
            s=requests.session()
            s.keep_alive = False
            s.mount('https://',HTTPAdapter(max_retries=5))
            price_response=s.get(price_url).text
        if len(price_response)>900:
            try:
                price=re.findall('"refPrice":"(.*?)"',price_response)[0]
                PreferentialPrice=re.findall('"promotionPrice":"(.*?)"',price_response)[0]
                if len(price)<1:
                    price=re.findall('"netPrice":"(.*?)"',price_response)[0]
                if price:
                    if float(price)<float(PreferentialPrice):
                        tt=price
                        price=PreferentialPrice
                        PreferentialPrice=tt
            except:
                price=None
                PreferentialPrice=None
        else:
            time.sleep(3)
            price_response = requests.get(price_url).text
            if len(price_response)>900:
                try:
                    price = re.findall('"refPrice":"(.*?)"', price_response)[0]
                    PreferentialPrice = re.findall('"promotionPrice":"(.*?)"', price_response)[0]
                    if len(price) < 1:
                        price = re.findall('"netPrice":"(.*?)"', price_response)[0]
                    if price:
                        if float(price) < float(PreferentialPrice):
                            tt = price
                            price = PreferentialPrice
                            PreferentialPrice = tt
                except:
                    price = None
                    PreferentialPrice = None
            else:
                #作出失败判断并将url归入重试
                price_response=self.retry_price(price_url)
                if len(price_response)>500:
                    try:
                        price = re.findall('"refPrice":"(.*?)"', price_response)[0]
                        PreferentialPrice = re.findall('"promotionPrice":"(.*?)"', price_response)[0]
                        if len(price) < 1:
                            price = re.findall('"netPrice":"(.*?)"', price_response)[0]
                        if price:
                            if float(price) < float(PreferentialPrice):
                                tt = price
                                price = PreferentialPrice
                                PreferentialPrice = tt
                    except:
                        price = None
                        PreferentialPrice = None
                else:
                    PreferentialPrice=None
                    price=None
        #防止出现多个字段出现为空
        if type==None and brand==None and p_Name==None:
            yield None
        else:
            source='苏宁'
            item['p_Name'] = may_name
            item['X_name'] = p_Name
            item['type'] = type
            item['X_type'] = X_type
            item['price'] = price
            item['PreferentialPrice'] = PreferentialPrice
            item['brand'] = brand
            item['keyword'] = keyword
            item['PoorCount'] = PoorCount
            item['CommentCount'] = CommentCount
            item['GoodCount'] = GoodCount
            item['GeneralCount'] = GeneralCount
            item['GoodRateShow'] = GoodRateShow
            item['ProductID'] = ProductID
            item['shop_name'] = shop_name
            item['capacity'] = capacity
            item['color']=color
            item['source']=source
            yield item
    def retry_price(self,price_url):
        price_response_may = requests.get(price_url)
        time.sleep(5)
        price_response=price_response_may.text
        return price_response