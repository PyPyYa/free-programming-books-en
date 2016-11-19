import scrapy
import re


class FreeBookItem(scrapy.Item):
    name = scrapy.Field()
    topics = scrapy.Field()


class FreeBookSpider(scrapy.Spider):

    name = 'freebook_list'
    allowed_domains = [
        "https://github.com/vhf/free-programming-books"
    ]
    start_urls = [
        "https://github.com/vhf/free-programming-books/blob/master/free-programming-books.md"
    ]

    def parse(self, response):

        index = response.xpath('//h3[a/@id="user-content-index"]')
        index_list = index.xpath('following-sibling::ul[1]')
        index_list_items = index_list.xpath('li')

        for li in index_list_items:
            name = li.xpath('a/text()')[0].extract()

            if name:
                sublist = li.xpath('ul')
                if sublist:
                    sublist_items = sublist.xpath('li/a/text()').extract()
                    yield FreeBookItem(
                        name=name,
                        topics=sublist_items
                    )
                else:
                    yield FreeBookItem(
                        name=name
                    )
