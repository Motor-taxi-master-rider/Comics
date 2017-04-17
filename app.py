import pandas as pd
import sys
from exceptions import Exception
from Comic_dragger import Comic_dragger_starter
from Comics import spiders
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def run_sracpy():
    process = CrawlerProcess(get_project_settings())

    process.crawl(spiders.Comics())
    process.start()


def format_data(df):
    df['update_time'] = df['update_time'].apply(lambda x: pd.Timestamp(x))
    return df


def read_df(file_path='./comics_output.csv'):
    df = pd.read_csv(file_path)
    return format_data(df)


def main(*script):
    def is_number(s):
        try:
            int(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False
    if(len(script) > 1):
        if script[1] == '-s':
            run_sracpy()
        elif script[1] == '-v':
            print(read_df())
        elif is_number(script[1]):
            df = read_df()
            cds = Comic_dragger_starter(df.ix[int(script[1])]['url'])
            cds.start_dragger()
        else:
            print('unknow command')
    else:
        print('Help:')
        print('-v   view data source')
        print('-s   re scrapy data')
        print('-[number]   retrive item of index')


if __name__ == '__main__':
    main(*sys.argv)
