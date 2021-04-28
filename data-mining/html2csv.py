import pandas as pd
import argparse
import numpy as np
from os import listdir
import regex as re


class html2csv():
    def __init__(self, opt):
        self.opt = opt

        # Initial the venue names
        df = pd.read_csv(opt.meta)
        df_filter = df[(df.Valid != 'no')]
        self.venue_name = df_filter['Dblp-abbr'].tolist()  # a list of venue name
        # ['cvpr', 'nips', 'iccv', 'eccv', 'aaai', 'icml', 'icra', 'www', 'chi', 'kdd', 'uss', 'ccs', 'icassp', 'ijcai', 'icse', 'sp', 'iclr', 'mm', 'infocom', 'acl', 'wsdm', 'iros', 'icc', 'sigmod', 'aistats', 'miccai', 'cikm', 'globecom', 'nsdi', 'sigcomm', 'emnlp', 'ndss', 'sigir', 'wacv', 'icde', 'icdcs', 'wcnc', 'icip', 'icdm', 'fg', 'pepm', 'isit', 'act', 'date', 'naacl', 'eurocrypt', 'soda', 'ijcnn', 'hpca', 'dac']
        self.dataset_fp = opt.dataset_fp


    def process_file(self, fp, venue, year):
        with open(fp, 'r') as f:
            lines = f.readlines()
        if re.search(r'Invalid URL, no such page.', '\n'.join(lines)):
            print('Invalid URL, no such page.')
            return []  # means there is nothing to return
        if len(re.findall(r'<span class="title" itemprop="name">', '\n'.join(lines))) < 3:
            print('No Title Found')
            return []

        regex_title = r'(?<=\<span class\=\"title\" itemprop\=\"name\"\>).+?(?=\<\/span\>)'
        titles = re.findall(regex_title, '\n'.join(lines))
        print('Done')
        l = []
        for item in titles:
            l.append([item, None, venue, year])
        return l

    def manage(self):
        # create a new dataframe
        # columns: title, questions, year, venue
        all_entries = []
        for venue in self.venue_name:
            dir_fp = self.dataset_fp + '/' + venue
            for f in listdir(dir_fp):
                fp = dir_fp + '/' + f
                year = re.findall(r'[0-9]+', f)[0]
                entries = self.process_file(fp, venue, year)
                all_entries += entries
                print('{} -- {}'.format(venue, year))
        all_entries_np = np.array(all_entries)
        df = pd.DataFrame(all_entries_np, columns=['title', 'question', 'year', 'venue'])
        df.to_csv(self.dataset_fp + '/' + 'all_titles.csv')
        print('dumped!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='html2csv')
    parser.add_argument('-meta', dest='meta', default='../datasets/metadata.csv',
                        help='Feel free to change to the location of your metadata.')
    parser.add_argument('-dataset_fp', dest='dataset_fp', default='../datasets',
                        help='Feel free to change to the location of your datasets.')
    opt = parser.parse_args()

    html2csv_process = html2csv(opt)
    html2csv_process.manage()

    print('Done!')
