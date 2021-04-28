import pandas as pd
import argparse
import numpy as np
import regex as re


class bib2csv():
    def __init__(self, opt):
        self.opt = opt

        #Initialize the dataset
        self.dataset_fp = self.opt.dataset_fp
        self.bib_fp = self.opt.bib_fp


    def process_file(self):
        l = []
        with open(self.bib_fp, 'r') as f:
            lines = f.readlines()

        title_lines = [l for l in lines if re.search(r'    title =', l)]
        year_lines = [l for l in lines if re.search(r'    year =', l)]
        assert len(title_lines) == len(year_lines)
        titles = [re.findall(r'(?<=\").+?(?=\")', title) for title in title_lines]
        nell_index = [index for index, title in enumerate(title_lines) if re.findall(r'(?<=\").+?(?=\")', title) == []]
        years = [re.findall(r'(?<=\").+?(?=\")', year)[0] for year in year_lines]
        l = [[titles[index][0], None, 'acl-events', years[index]] for index in range(len(years)) if index not in nell_index]

        return l

    def manage(self):
        # create a new dataframe
        # columns: title, questions, year, venue
        all_entries = self.process_file()
        all_entries_np = np.array(all_entries)
        df = pd.DataFrame(all_entries_np, columns=['title', 'question', 'venue', 'year'])
        df.to_csv(self.dataset_fp + '/' + 'all_titles_acl.csv')
        print('dumped!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='bib2csv')
    parser.add_argument('-dataset_fp', dest='dataset_fp', default='../datasets',
                        help='Feel free to change to the location of your datasets.')
    parser.add_argument('-bib_fp', dest='bib_fp', default='../datasets/anthology.bib',
                        help='Feel free to change to the location of your datasets.')
    opt = parser.parse_args()

    bib2csv_process = bib2csv(opt)
    bib2csv_process.manage()

    print('Done!')
