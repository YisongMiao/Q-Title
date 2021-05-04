# Q-Title



## 1. Codebase Structure

- [data-curl](https://github.com/YisongMiao/Q-Title/tree/main/data-curl)

  Our study includes papers from two major sources: ACL for computational linguistic society, DBLP for other conferences (we choose Top 50 CS conference from [[link](https://www.guide2research.com/topconf/)])

  - [curl.sh](https://github.com/YisongMiao/Q-Title/blob/main/data-curl/curl.sh): A bash script that curl webpages (.html) from dblp for top 50 CS conferences in past 30 years.
  - We directly download its official full bib file from [[link](https://www.aclweb.org/anthology/anthology.bib.gz)].

- [data-mining](https://github.com/YisongMiao/Q-Title/tree/main/data-mining)

  - [html2csv.py](https://github.com/YisongMiao/Q-Title/blob/main/data-mining/html2csv.py): Convert the downloaded html file into an intermediate csv file.

    - Key metadata encoded in csv columns: 'title', 'question', 'venue', 'year'.

  - [bib2csv.py](https://github.com/YisongMiao/Q-Title/blob/main/data-mining/bib2csv.py): Convert the downloaded html bib into an intermediate csv file. 

    - Key metadata is the same as above: 'title', 'question', 'venue', 'year'.

  - [csv2question.py](https://github.com/YisongMiao/Q-Title/blob/main/data-mining/csv2questions.py): 

    This script is more about NLP than data mining :P

    In the class of `question_mining_process` we have following methods that being executed sequentially:

    - `question_detection`: from 350k+ paper titiles, we detect 4k+ questions that have a question in it.

      Input: the original panda dataframe from original csv files. 

      Output: a new panda dataframe that only contains titles that contain questions.

    - `insights_question_detection`: generate insights from `question_detection` method.

      Input: the dataframe from `question_detection`

      Output: question frequencies w.r.t. year/venue. 

    - `question_mining`: from 4k+ titles with questions, we extract the questions from the title.

      Input: The dataframe from `question_detection`

      Output: A new dataframe with a new column of `title`

      Key technology: `spacy`'s sentence segmentation.

    - `question_analyze`: Analyze questions.

      Input: The dataframe from `question_mining`

      Output: A new dataframe, adding a new column for the type of questions, we now have general questions, special questions, choice questions and disjunctive questions. 

    - `question_type_per_year_venue`

      Input: The dataframe from `question_analyze`.

      Output: Question types w.r.t. year/venue. 



## 2. Corpus Analysis

### 2.1 Corpus Metadata

In this development repo, we don't upload raw data file.

You can download the zip here: https://github.com/YisongMiao/Q-Title/blob/main/question_info.csv.zip

Or a csv file: https://yisong.me/publications/question_info.csv



In the csv file:

- **Number of Rows (each question in one row):** 4181

- **Columns:** 'Question', 'Title', 'Index', 'venue', 'year', 'type'
  - Question: in text format. 
  - Title: in text format. 
  - Index: from 0 to 4087, indicating the index of title. This is because some title has more than one questions. 
  - venue: The venue where the paper was presented. We have ACL events + other 
  - year: In range (1990, 2020)
  - type: With five options: general, special, choice, disjunctive, and unknown. 



### 2.2 Corpus Samples

Randomly seleted 20 samples. 



### 2.3 Error Analysis