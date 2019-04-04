import scrapy
from Tencent.items import TencentItem


class TencentpositionSpider(scrapy.Spider):
    # 爬虫名
    name = 'tencentposition'
    # 爬虫作用范围
    allowed_domains = ['tencent.com']
    url = "http://hr.tencent.com/position.php?&start="
    offset = 0
    # 起始url
    start_urls = [url + str(offset)]
    
    def parse(self,response):
        for each in response.xpath('//tr[@class="even"] | //tr[@class="odd"]'):
            item = TencentItem()
            # 名字
            item['positionname'] = each.xpath('./td[1]/a/text()')[0].extract()
            # 连接
            item['positionlink'] = each.xpath('./td[1]/a/@href')[0].extract()
            # 类别
            item['positiontype'] = each.xpath('./td[2]/text()').extract_first()
            # 招聘人数
            item['peoplenum'] = each.xpath('./td[3]/text()')[0].extract()
            # 工作地点
            item['worklocation'] = each.xpath('./td[4]/text()')[0].extract()
            # 时间
            item['publishtime'] = each.xpath('./td[5]/text()')[0].extract()
             
            yield item
         
        if self.offset <= 3350:
            self.offset += 10
#             
#         # 每次处理完一页的数据之后，重新发送下一页页面请求
#         # self.offset自增10，同时拼接为新的url，并调用回调函数self.parse处理Response
        yield scrapy.Request((self.url + str(self.offset)), callback = self.parse)       