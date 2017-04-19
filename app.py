import sys
import pandas as pd
from exceptions import Exception


def run_sracpy():
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    process = CrawlerProcess(get_project_settings())
    process.crawl(spiders.Comics())
    process.start()


def format_data(df):
    df['update_time'] = df['update_time'].apply(lambda x: pd.Timestamp(x))
    return df


def read_df(file_path='./comics_output.csv'):
    df = pd.read_csv(file_path)
    return format_data(df)


def read_parms(*params):
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
    view_parser.add_argument('--level', '-l',  choices=('-r', '-d'), default='-r', dest="level",
                             help='Detail level: -r for roughly(default); -d for detailed')

    # drag
    delete_parser = subparsers.add_parser(
        'drag', help='Drag comics form website')
    delete_parser.add_argument('--index', '-i', type=int,
                               nargs='+', dest="d_index", help='Drag a list of index')
    main(parser.parse_args())
# def main(*script):
#     def is_number(s):
#         try:
#             int(s)
#             return True
#         except ValueError:
#             pass
#
#         try:
#             import unicodedata
#             unicodedata.numeric(s)
#             return True
#         except (TypeError, ValueError):
#             pass
#         return False
#     if(len(script) > 1):
#         if script[1] == '-s':
#             run_sracpy()
#         elif script[1] == '-v':
#             print(read_df())
#         elif is_number(script[1]):
#             df = read_df()
#             cds = Comic_dragger_starter(df.ix[int(script[1])]['url'])
#             cds.start_dragger()
#         else:
#             print('unknow command')
#     else:
#         print('Help:')
#         print('-v   view data source')
#         print('-s   re scrapy data')
#         print('-[number]   retrive item of index')


def main(params):
    from Comic_dragger import Comic_dragger_starter
    from Comics import spiders

    def scrapy_command(p):
        print(p.rescrapy)
        if p.rescrapy:
            pass
            # TODO add total rescrapy function
        else:
            run_sracpy()

    def view_command(p):
        print(p.v_index)
        print(p.name)
        print(p.level)
        index = p.v_index
        name = p.name
        level = p.level
        if index:
            if level == '-d':
                pass
            elif level == '-r':
                pass
            else:
                print('Unknow Level')
        elif name:
            if level == '-d':
                pass
            elif level == '-r':
                pass
            else:
                print('Unknow Level')
        else:
            raise Exception

    def drag_command(p):
        print(p.d_index)
        index = p.d_index
        if index:
            pass
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
        print(Exception)


if __name__ == '__main__':
    read_parms(*sys.argv)
