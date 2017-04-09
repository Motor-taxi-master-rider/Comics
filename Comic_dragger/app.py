import bin

if __name__ == '__main__':

    url = 'http://www.tazhe.com/mh/9170/'

    crawler = bin.comic_dragger(url=url)
    crawler.start()
