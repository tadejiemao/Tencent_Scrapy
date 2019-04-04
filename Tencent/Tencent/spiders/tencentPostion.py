import scrapy
from Tencent.items import TencentItem


class TencentpositionSpider(scrapy.Spider):
    # ������
    name = 'tencentposition'
    # �������÷�Χ
    allowed_domains = ['tencent.com']
    url = "http://hr.tencent.com/position.php?&start="
    offset = 0
    # ��ʼurl
    start_urls = [url + str(offset)]
    
    def parse(self,response):
        for each in response.xpath('//tr[@class="even"] | //tr[@class="odd"]'):
            item = TencentItem()
            # ����
            item['positionname'] = each.xpath('./td[1]/a/text()')[0].extract()
            # ����
            item['positionlink'] = each.xpath('./td[1]/a/@href')[0].extract()
            # ���
            item['positiontype'] = each.xpath('./td[2]/text()').extract_first()
            # ��Ƹ����
            item['peoplenum'] = each.xpath('./td[3]/text()')[0].extract()
            # �����ص�
            item['worklocation'] = each.xpath('./td[4]/text()')[0].extract()
            # ʱ��
            item['publishtime'] = each.xpath('./td[5]/text()')[0].extract()
             
            yield item
         
        if self.offset <= 3350:
            self.offset += 10
#             
#         # ÿ�δ�����һҳ������֮�����·�����һҳҳ������
#         # self.offset����10��ͬʱƴ��Ϊ�µ�url�������ûص�����self.parse����Response
        yield scrapy.Request((self.url + str(self.offset)), callback = self.parse)       