import pandas as pd
import argparse
import numpy as np
from collections import Counter
import regex as re

# spaCy
import spacy
nlp = spacy.load("en_core_web_sm")


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

    def question_mining(self):
        # Since we have already detected all the questions in the titles, we now mining them
        # Output is a new dataframe, adding a new column of questions.
        self.df_has_Q = self.df_aggregate[self.df_aggregate.has_Q == 1]
        print('df_has_Q Shape is: {}'.format(self.df_has_Q.shape))
        titles = self.df_has_Q['title'].tolist()
        question_count_list = []

        question_info_list = []
        for index, title in enumerate(titles):
            # if index > 500: continue
            # title = title.lower()
            title = re.sub(r'\{', r'', title)
            title = re.sub(r'\}', r'', title)
            doc = nlp(title)
            output = '\n'.join([sent.text for sent in doc.sents])
            question_text = [sent.text for sent in doc.sents if re.search(r'\?', sent.text)]
            question_info = [[q, title, index] for q in question_text]
            question_info_list += question_info
            question_count = len(question_text)
            question_count_list.append(question_count)
            if question_count > 1:
                print(output)
                print('\n')

        self.question_info_df = np.array(question_info_list)
        self.question_info_df = pd.DataFrame(self.question_info_df, columns=['Question', 'Title', 'Index'])
        self.question_info_df.to_csv(self.opt.dataset_fp + '/' + 'question_info.csv')
        print('Question Info Done. Size: {}'.format(self.question_info_df.shape))
        print(Counter(question_count_list))
        return None

    def question_analyze(self):
        tag_list = list()
        question_list = self.question_info_df['Question'].tolist()
        for q in question_list:
            q_nlp = nlp(q)

            if q_nlp[0].text.lower() in ['what', 'when', 'how', 'why', 'which', 'where', 'who', 'whose']:
                tag_list.append('special')
            elif q_nlp[0].text.lower() in ['do', 'does', 'did', 'have', 'has', 'had', 'can', 'could', 'should', 'shall', 'is', 'are', 'will', 'would']:
                tag_list.append('general')
            elif re.search(r' or ', q):
                tag_list.append('choice')
            elif re.search(r'isn\'t', q):
                tag_list.append('disjunctive')
            else:
                tag_list.append('unknown')

        assert len(tag_list) == len(question_list)      
        self.question_info_df['type'] = pd.Series(np.array(tag_list), index=self.question_info_df.index)
        self.question_info_df.to_csv(self.opt.dataset_fp + '/' + 'question_info.csv')
        print(Counter(tag_list))
        print('Question Info Done.\n With Question Types added! Size: {}'.format(self.question_info_df.shape))

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
        # self.insights_question_detection()
        self.question_mining()
        self.question_analyze()
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
