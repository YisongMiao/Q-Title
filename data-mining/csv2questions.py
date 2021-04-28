import pandas as pd
import argparse
import numpy as np
from os import listdir
import regex as re


class question_mining():
    def __init__(self, opt):
        self.opt = opt

        self.df_acl = pd.read_csv(opt.acl_fp)
        self.df_other = pd.read_csv(opt.other_fp)

        self.df_aggregate = pd.concat([self.df_acl, self.df_other])

        print('Init Done')

    def question_detection(self):
        # A very simple and fast method to detect if there is a question in a title.
        # We leave mining the question to another method.
        self.has_Q = list()
        titles = self.df_aggregate['title'].tolist()
        for index, title in enumerate(titles):
            if index % 100000 == 0:
                print('Processing Index: {}'.format(index))
            if re.search(r'\?', title):
                self.has_Q.append(1)
            else:
                self.has_Q.append(0)
        assert len(self.has_Q) == self.df_aggregate.shape[0]
        self.df_aggregate['has_Q'] = pd.Series(np.array(self.has_Q), index=self.df_aggregate.index)
        print('Question detection done')
        # No return, directly store to self.has_Q and self.df_aggregate

    def insights_question_detection(self):
        # Objective: Get insights from the question detection method
        # Insight 1: Question frequency w.r.t. venue
        venues = list(set(self.df_aggregate['venue']))
        venue_list = []
        for _y in venues:
            title_number = self.df_aggregate[(self.df_aggregate.venue == _y)].shape[0]
            Q_number = self.df_aggregate[(self.df_aggregate.venue == _y) & (self.df_aggregate.has_Q == 1)].shape[0]
            ratio = round(1000 * float(Q_number) / title_number, 3)
            entry = [Q_number, title_number, ratio, str(_y)]
            venue_list.append(entry)

        venue_entries_np = np.array(venue_list)
        df = pd.DataFrame(venue_entries_np, columns=['Q_number', 'title_number', 'ratio', 'venue'])
        df.to_csv(self.opt.dataset_fp + '/' + 'insight_venue.csv')
        print('Insights done venue')

        # Insight 2: Question frequency w.r.t. time
        year_list = []
        for _y in range(1990, 2022):
            title_number = self.df_aggregate[(self.df_aggregate.year == _y)].shape[0]
            Q_number = self.df_aggregate[(self.df_aggregate.year == _y) & (self.df_aggregate.has_Q == 1)].shape[0]
            ratio = round(1000 * float(Q_number) / title_number, 3)
            entry = [Q_number, title_number, ratio, str(_y)]
            year_list.append(entry)

        year_entries_np = np.array(year_list)
        df = pd.DataFrame(year_entries_np, columns=['Q_number', 'title_number', 'ratio', 'year'])
        df.to_csv(self.opt.dataset_fp + '/' + 'insight_year.csv')
        print('Insights done year')

        year_list = []
        for _y in range(1990, 2022):
            title_number = self.df_aggregate[(self.df_aggregate.year == _y)].shape[0]
            Q_number = self.df_aggregate[(self.df_aggregate.year == _y) & (self.df_aggregate.has_Q == 1) & (self.df_aggregate.venue != 'acl-events')].shape[0]
            ratio = round(1000 * float(Q_number) / title_number, 3)
            entry = [Q_number, title_number, ratio, str(_y)]
            year_list.append(entry)

        year_entries_np = np.array(year_list)
        df = pd.DataFrame(year_entries_np, columns=['Q_number', 'title_number', 'ratio', 'year'])
        df.to_csv(self.opt.dataset_fp + '/' + 'insight_year_other.csv')
        print('Insights done year')

        year_list = []
        for _y in range(1990, 2022):
            title_number = self.df_aggregate[(self.df_aggregate.year == _y)].shape[0]
            Q_number = self.df_aggregate[(self.df_aggregate.year == _y) & (self.df_aggregate.has_Q == 1) & (
                        self.df_aggregate.venue == 'acl-events')].shape[0]
            ratio = round(1000 * float(Q_number) / title_number, 3)
            entry = [Q_number, title_number, ratio, str(_y)]
            year_list.append(entry)

        year_entries_np = np.array(year_list)
        df = pd.DataFrame(year_entries_np, columns=['Q_number', 'title_number', 'ratio', 'year'])
        df.to_csv(self.opt.dataset_fp + '/' + 'insight_year_acl.csv')
        print('Insights done year')

    def manage(self):
        # columns: title, questions, year, venue
        self.question_detection()
        self.insights_question_detection()
        print('Done')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='html2csv')
    parser.add_argument('-dataset_fp', dest='dataset_fp', default='../datasets',
                        help='Feel free to change to the location of your datasets.')
    parser.add_argument('-acl_fp', dest='acl_fp', default='../datasets/all_titles_acl.csv',
                        help='ACL events. Feel free to change to the location of your datasets.')
    parser.add_argument('-other_fp', dest='other_fp', default='../datasets/all_titles.csv',
                        help='Other venues than ACL. Feel free to change to the location of your datasets.')
    opt = parser.parse_args()

    question_mining_process = question_mining(opt)
    question_mining_process.manage()

    print('Done!')
