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



## 2. Q-Title: Corpus Analysis

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



### 2.2 Corpus Samples in Q-Title:

Randomly seleted 30 samples. 

| Question                                                     | Title                                                        | Index | venue      | year | type    |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ----- | ---------- | ---- | ------- |
| Yes we can!?                                                 | Yes we can!? Annotating English modal verbs                  | 933   | acl-events | 2012 | unknown |
| What does the power industry need from the EDA industry and what is the EDA industry doing about it? | Panel: What does the power industry need from the EDA industry and what is the EDA industry doing about it? | 3883  | date       | 2011 | special |
| How Much Data Do You Need?                                   | How Much Data Do You Need? About the Creation of a Ground Truth for Black Letter and the Effectiveness of Neural OCR | 87    | acl-events | 2020 | special |
| How Far from Optimal Is Fast and Frugal?.                    | On the Accuracy of Bounded Rationality: How Far from Optimal Is Fast and Frugal?. | 1626  | nips       | 2005 | special |
| Does estimation trump compression?                           | Learning Markov distributions: Does estimation trump compression? | 3786  | isit       | 2016 | general |
| How Does Channel Coding Affect the Design of Uplink SCMA Multidimensional Constellations? | How Does Channel Coding Affect the Design of Uplink SCMA Multidimensional Constellations? | 3691  | wcnc       | 2020 | special |
| Do you remember this source code?                            | Do you remember this source code?                            | 2732  | icse       | 2018 | general |
| How Hard Is the Manipulative Design of Scoring Systems?.     | How Hard Is the Manipulative Design of Scoring Systems?.     | 2691  | ijcai      | 2019 | special |
| Which PKI (public key infrastructure) is the right one?      | Which PKI (public key infrastructure) is the right one? (panel session). | 2467  | ccs        | 2000 | special |
| Easy as ABC?                                                 | Easy as ABC? Facilitating Pictorial Communication via Semantically Enhanced Layout | 1106  | acl-events | 2008 | unknown |
| CM(1, 2) or CM(2, 2)?                                        | Which constant modulus criterion is better for blind adaptive filtering: CM(1, 2) or CM(2, 2)? [equalizer example]. | 2552  | icassp     | 2005 | choice  |
| When must all terminals talk?                                | Achieving SK capacity in the source model: When must all terminals talk? | 3839  | isit       | 2014 | special |
| When Does Diversity of Agent Preferences Improve Outcomes in Selfish Routing? | When Does Diversity of Agent Preferences Improve Outcomes in Selfish Routing? | 2658  | ijcai      | 2018 | special |
| Does Vertical Bring more Satisfaction?                       | Does Vertical Bring more Satisfaction?: Predicting Search Satisfaction in a Heterogeneous Environment. | 3272  | cikm       | 2015 | general |
| The Usual Suspects?                                          | The Usual Suspects? Reassessing Blame for VAE Posterior Collapse. | 1801  | icml       | 2020 | unknown |
| Where to park?                                               | Where to park? minimizing the expected time to find a parking space. | 1854  | icra       | 2015 | special |
| Far but Near or Near but Far?                                | Far but Near or Near but Far?: The Effects of Perceived Distance on the Relationship between Geographic Dispersion and Perceived Diversity. | 2095  | chi        | 2016 | choice  |
| ; Where are we today?!                                       | Summarization and Evaluation; Where are we today?!           | 1145  | acl-events | 2007 | unknown |
| Can it Work?                                                 | Cognitive Radio in a Frequency Planned Environment: Can it Work? | 3347  | globecom   | 2007 | general |
| Is this app safe?                                            | Is this app safe?: a large scale study on application permissions and risk signals. | 2001  | www        | 2012 | general |
| is this even the right question?                             | Lightweight vs. heavyweight processes: is this even the right question? | 2799  | icse       | 2002 | general |
| Is actuation redundancy a good solution for pick-and-place?  | Towards 100G with PKM. Is actuation redundancy a good solution for pick-and-place? | 1840  | icra       | 2010 | general |
| Support or Oppose?                                           | Support or Oppose? Classifying Positions in Online Debates from Reply Activities and Opinion Expressions | 1045  | acl-events | 2010 | choice  |
| Who's Better?                                                | Who's Better? Who's Best? Pairwise Deep Ranking for Skill Determination. | 1483  | cvpr       | 2018 | special |
| What good are strong specifications?                         | What good are strong specifications?                         | 2769  | icse       | 2013 | special |
| Do You See What I See?                                       | Do You See What I See? Differential Treatment of Anonymous Users. | 3462  | ndss       | 2016 | general |
| Culture or fluency?                                          | Culture or fluency?: unpacking interactions between culture and communication medium. | 2308  | chi        | 2011 | choice  |
| Expect the Unexpected?                                       | Expect the Unexpected? The Processing of Possibility Hedges in Medical Diagnoses and Medical Advice | 433   | acl-events | 2018 | unknown |
| Fluency, Adequacy, or HTER?                                  | Fluency, Adequacy, or HTER? Exploring Different Human Judgments with a Tunable MT Metric | 1074  | acl-events | 2009 | choice  |
| Given Obstacles?                                             | Feasibility: Can Humanoid Robots Overcome Given Obstacles?   | 1867  | icra       | 2005 | unknown |



### 2.3 Insights and Discussions

Please refer to our slides for full insights and discussions. [[Slides@Google](https://docs.google.com/presentation/d/1d0xlTMaDiJ_x_VW1rEop4HEhbAZ5piqsC0lPZmGy7bg/edit?usp=sharing)]

We only show key images here.

Frequency of questions w.r.t. years:

![]()



Frequency of questions w.r.t. venues:

![]()