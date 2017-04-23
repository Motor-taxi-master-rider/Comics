import bin


class Comic_dragger_starter:
    '''class for comic_dragger api

    url: str url to crawl

    start: int start index

    end: int end index

    save_floder: floader name to store comics pictures
    '''
    def __init__(self, url,start=0, end=-1, save_floder=".\download"):
        self.url = url
        self.crawler = bin.comic_dragger(url=url)

    def start_dragger(self):
        self.crawler.start()
