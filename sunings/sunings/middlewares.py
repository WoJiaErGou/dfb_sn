# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy.exceptions import IgnoreRequest
from scrapy import signals
from sunings.settings import suning_user_agent
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random
import pandas as pd
class Exceptions(object):
    def __init__(self):
        self.errorlist=[]
        self.reason=[]

    @classmethod
    def from_crawler(cls, crawler):
        ex=cls()
        crawler.signals.connect(ex.spider_closed,signals.spider_closed)
        return ex
    def process_exception(self, request, exception, spider):
        print(exception)
        if request.url in self.errorlist:
            print('该URL已经存在！')
            raise IgnoreRequest
        else:
            self.errorlist.append(request.url)
            self.reason.append(exception)
            raise IgnoreRequest
    def spider_closed(self,spider):
        df=pd.DataFrame(columns=['url','reason'],index=None)
        df.url=self.errorlist
        df.reason=self.reason
        df.to_csv('error.csv',mode='w',index=None)

class SuningsSpiderMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class SuningUseragentMiddleware(UserAgentMiddleware):
    '''
    设置User-Agent
    '''
    def process_request(self, request, spider):
        agent=random.choice(suning_user_agent)
        if agent:
            request.headers.setdefault('User-Agent',agent)
