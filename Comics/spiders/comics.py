# coding:utf-8

import scrapy
from bs4 import BeautifulSoup


class Comics(scrapy.Spider):

    name = "comics"
    allowed_domains = ["http://www.tazhe.commh/9068/"]

    def start_requests(self):
        urls = ['http://www.tazhe.com/mh/9068/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
#

    def parse(self, response):
        content = response.body
        if not content:
            self.log('parse body error.')
            return

        soup = BeautifulSoup(content, "html5lib")

        listcon_tag = soup.find('li', class_='li')
        if len(listcon_tag) < 1:
            self.log('extract comics list error')
            return

        com_a_list = listcon_tag.find_all('a', attrs={'href': True})
        if len(listcon_tag) < 1:
            self.log('Can not find <a> that contain href attribute.')
            return

        commics_url_list = []
        base = 'http://www.tazhe.com'
        for tag_a in com_a_list:
            url = base + tag_a['href']
            commics_url_list.append(url)

        print('\n>>>>>>>>>>>>>>>>>>> current page comics list <<<<<<<<<<<<<<<<<<<<')
            print(comics_url_list)

        for url in comics_url_list:
            print('>>>>>>>>  parse pages:' + url)
            yield scrapy.Request(url=url, callback=self.comics_parse)

    def comics_parse(self, response):
        content = response.body
        if not content:
            self.log('parse body error.')
            return

        soup = BeautifulSoup(content, "html5lib")

        img_tag = soup.find(id='qTcms_pic')
        img_url = img_tag['src']
        self.log('img url:' + img_url)

        title = img_tag['alt'].split()[1] + \
            soup.find(id='qTcms_select_i')['value']

        soup.select(".next nth-of-type(1)")
