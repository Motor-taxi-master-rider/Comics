from __future__ import print_function

"""This file contains mian project definitions for:



"""

import sys
import pandas as pd
from exceptions import Exception


def run_sracpy():
    '''Initialize the scrapy spider and start crawl all comics info
    '''
    from Comics import spiders
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    process = CrawlerProcess(get_project_settings())
    process.crawl(spiders.Comics())
    process.start()


def format_data(df):
    '''format dataframe data for further analysis
    '''
    df['update_time'] = df['update_time'].apply(lambda x: pd.Timestamp(x))
    return df


def read_df(file_path='./comics_output.csv'):
    df = pd.read_csv(file_path)
    return format_data(df)


def read_parms(*params):
    '''handle input sys params.

    commands:
    {scrapy,view,drag}  additional help
    scrapy [--rescrapy]                        run scrapy
    view [--index | --name] [--level {r,d}]    View scrapyed data
    drag [--index]                             Drag comics form website

    params: list sys.arg
    '''
    import argparse
    parser = argparse.ArgumentParser(version='v2.2')
    subparsers = parser.add_subparsers(dest='subparser_name',
                                       title='commands', help='additional help')

    # scrapy
    scrapy_parser = subparsers.add_parser('scrapy', help='run scrapy')
    scrapy_parser.add_argument('--rescrapy', '-r', action='store_true', default=False, dest="rescrapy",
                               help='Totallly rescapy')

    # view
    view_parser = subparsers.add_parser('view', help='View scrapyed data')
    group = view_parser.add_mutually_exclusive_group()
    group.add_argument('--index', '-i', type=int, nargs='+', dest="v_index",
                       help='View a list of index')
    group.add_argument('--name', '-n', action='store', dest="name",
                       help='Search a comic name')
    view_parser.add_argument('--level', '-l',  choices=('r', 'd'), default='r', dest="level",
                             help='Detail level: r for roughly(default); d for detailed')

    # drag
    delete_parser = subparsers.add_parser(
        'drag', help='Drag comics form website')
    delete_parser.add_argument('--index', '-i', type=int,
                               nargs='+', dest="d_index", help='Drag a list of index')
    main(parser.parse_args())


def main(params):
    '''main function.

    Drag comics form website

    params: dict argparse.args
    '''
    from Comic_dragger import Comic_dragger_starter

    def scrapy_command(p):
        '''conditionally run scrapy.

        if [--rescapy] or [-r], then totallly re-run spider, else make incremental crawl

        p: list argparse.args
        '''
        if p.rescrapy:
            pass
            # TODO: add total rescrapy function
        else:
            run_sracpy()

    def view_command(p):
        '''conditionally view dataset.

        if [-ld] then show detailed pandas dataset, else [-lr] then show simple dataset;

        if [--index] or [-i] then search for index, else [--name] or [-n] then search for name;

        p: dict argparse.args
        '''
        df = read_df()
        index = p.v_index
        name = p.name
        level = p.level
        if index:
            if level == 'd':
                print(df.ix[index])
            elif level == 'r':
                print(df.ix[index][['name', 'classification', 'author']])
            else:
                print('Unknown Level')
        elif name:
            # TODO: search for name
            if level == 'd':
                pass
            elif level == 'r':
                pass
            else:
                print('Unknown Level')
        else:
            print(df)

    def drag_command(p):
        '''conditionally drag comics' pictures of url through Comic_dragger.

        drag comics of listed indexs in [--index] or [-i]

        p: dict argparse.args
        '''
        from Comic_dragger import Comic_dragger_starter
        import threading
        index = p.d_index

        def worker(url):
            dragger = Comic_dragger_starter(url)
            dragger.start_dragger()

        if index:
            df = read_df()
            for item in set(index):
                t = threading.Thread(target=worker, args=(df.ix[item]['url'],))
                t.start()
        else:
            raise Exception

    command = params.subparser_name
    switcher = {
        'scrapy': scrapy_command,
        'view': view_command,
        'drag': drag_command,
    }
    try:
        switcher.get(command, None)(params)
    except Exception:
        pass


if __name__ == '__main__':
    read_parms(*sys.argv)
