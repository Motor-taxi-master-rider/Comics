import bin


class Comic_dragger_starter:
    def __init__(self, url):
        self.url = url
        self.crawler = bin.comic_dragger(url=url)

    def start_dragger(self):
        self.crawler.start()
