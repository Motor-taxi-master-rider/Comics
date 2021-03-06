from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import logging
import re
import os
from os import path as osp
import urllib2


class comic_dragger:
    '''
    url: str url to crawl

    start: int start index

    end: int end index

    save_floder: str floder name to store comics pictures
    '''

    def __init__(self, url, start=0, end=-1, save_floder=".\download"):
        self.code = "utf-8"
        self.__url = url
        self.__start = start
        self.__end = end
        self.__save_floder = save_floder
        self.__commic_title = 'undefined'
        self.__chapter_list = []
        self.__browser = webdriver.PhantomJS()
        self.get_chapter_list()

    def get_chapter_list(self):
        '''connect to comics url and get url list of each chapter.
        '''
        print 'connect to %s...' % self.__url
        self.__browser.get(self.__url)

        print 'start parsing %s...\n' % self.__url
        self.__commic_title = self.__browser.find_elements_by_css_selector(
            '.title h1')[0].text
        chapter_elem_list = self.__browser.find_elements_by_css_selector(
            '#play_0 ul li a')
        chapter_elem_list.reverse()

        self.__chapter_list = []
        for chapter_elem in chapter_elem_list:
            self.__chapter_list.append(
                (chapter_elem.text, chapter_elem.get_attribute('href')))

        if self.__start >= len(self.__chapter_list) or (0 <= self.__end < self.__start):
            raise Exception('illegal index position')

    def download_chapter(self, chapter_idx, save_folders=None):
        '''Traversal all page of selected chapter and download image.



        '''
        bad_chars = "\\/:*?\"<>|"
        rgx = re.compile('[%s]' % bad_chars)

        chapter = self.__chapter_list[chapter_idx]
        chapter_title = chapter[0]
        chapter_url = chapter[1]
        save_folders = osp.join(
            self.__save_floder, rgx.sub(' ', save_folders.encode(self.code)).decode(self.code), rgx.sub(' ', chapter_title.encode(self.code)).decode(self.code))
        # print('dragging %s...' %
        # chapter_title.encode(self.code))
        print('dragging %s - %s...' % (self.__commic_title, chapter_title))

        logging.info('#### START DOWNLOAD CHAPTER %d %s ####' %
                     (chapter_idx, chapter_title))

        if not osp.exists(save_folders):
            os.makedirs(save_folders)

        self.__browser.get(chapter_url)

        index = 1
        miscatch = 0
        while True and miscatch <=3:
            image_url = self.__browser.find_element_by_css_selector(
                '#qTcms_pic').get_attribute('src')
            #if uncaught image, add count
            if image_url == 'http://www.tazhe.com/static/images/nopic.jpg':
                miscatch += 1
                continue
            save_image_name = osp.join(
                save_folders,  str(index) + '.' + osp.basename(image_url).split('.')[-1])
            self.download(image_url, save_image_name)

            self.__browser.find_element_by_css_selector('a.next').click()
            #stop dragging
            try:
                self.__browser.find_element_by_css_selector('#bgDiv')
                break
            except NoSuchElementException:
                index += 1
                pass

    @staticmethod
    def download(url, save_path, try_time=3, timeout=30):
        '''download comic picture of a page

        url: str image url

        try_time: int max try time

        timeout: int name to store comics pictures
        '''
        while try_time > 0:
            try:
                content = urllib2.urlopen(url, timeout=timeout).read()
                with open(save_path, 'wb') as fp:
                    fp.write(content)
                break
            except Exception, et:
                logging.error(et, exc_info=True)
                try_time -= 1
                if try_time == 0:
                    logging.error('cannot download: %s to %s' %
                                  (url, save_path))

    def start(self):
        '''start dragging
        '''
        start = self.__start if self.__start >= 0 else 0
        end = self.__end if self.__end >= 0 else len(self.__chapter_list)

        for chapter_idx in xrange(start, end):
            self.download_chapter(chapter_idx, self.__commic_title)
