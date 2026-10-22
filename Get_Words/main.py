# William Keilsohn 
# August 10th 2026

# Import Packages
import os
import numpy as np
import pandas as pd
from random import choice, shuffle, randint
from time import sleep
from tqdm import tqdm

## Import Custom Scripts
from page_parser import *
from web_caller import *
# from table_sorter import *

# Define Variables
cwd = os.getcwd()
file = os.path.join(cwd, 'questions.xlsx')
cols = ['Question', '1', '2', '3', '4', 'Answer', 'Page'] #  'Sentence',

alt_file = os.path.join(cwd, 'failed_links.txt')
alt_link_df = pd.DataFrame(columns=['Question_Type', 'Link'])

kan_start = 'KAN'
voc_start = 'VOC'
gram_start = 'GRA'

## Page Extensions
base = 'https://japanesetest4you.com/'
kanji_link = 'japanese-language-proficiency-test-jlpt-n5-kanji-exercise-'
vocab_link = 'japanese-language-proficiency-test-jlpt-n5-vocabulary-exercise-'
grammar_link = 'japanese-language-proficiency-test-jlpt-n5-grammar-exercise-'

link_df = pd.DataFrame(columns=['Question_Type', 'Link'])

## Category Numbers 
kanji_num = 19
vocab_num = 24
grammar_num = 26

## Category Dataframes
kanji_df = pd.DataFrame(columns=cols)
vocab_df = pd.DataFrame(columns=cols)
grammar_df = pd.DataFrame(columns=cols)

# Define Functions
def pageListMaker(cat_length, cat_extension):
    global base
    cat_ls = []
    for i in range(0, cat_length):
        cat_ls.append(base + cat_extension + str(i + 1))
    return cat_ls

def addLinksToDF(link_ls, type_mark):
    global link_df
    for i in link_ls:
        new_row = [type_mark, i]
        link_df.loc[len(link_df)] = new_row

def prepareLinkDF():
    global kanji_num
    global vocab_num
    global grammar_num
    global kanji_link
    global vocab_link
    global grammar_link
    global link_df
    kanji_ls = pageListMaker(kanji_num, kanji_link)
    vocab_ls = pageListMaker(vocab_num, vocab_link)
    grammar_ls = pageListMaker(grammar_num, grammar_link)
    addLinksToDF(kanji_ls, kan_start)
    addLinksToDF(vocab_ls, voc_start)
    addLinksToDF(grammar_ls, gram_start)
    link_df = link_df.sample(frac=1, random_state=42).reset_index(drop=True) # Scrambling is optional, but helps create some randomness which makes it look less like a machine. 

# Run Application
if __name__ == '__main__':
    prepareLinkDF()
    link_df = link_df.sample(frac=1, random_state=42).reset_index(drop=True)
    pbar = tqdm(total = len(link_df))
    while len(link_df) > 0:
        link_df.reset_index(drop=True, inplace=True)
        row = link_df.sample()
        row_cat = row['Question_Type'].values[0]
        row_link = row['Link'].values[0]
        raw_soup = callPage(row_link)
        cut_soup = getSection(raw_soup)
        try: # The website is not formatted exactly the same. Thus it is just easier to skip malformed pages. 
            page_df = compileQDF(cut_soup)
            page_df['Page'] = [row_link] * 10
            if row_cat == kan_start:
                kanji_df = pd.concat([kanji_df, page_df], ignore_index=True)
            elif row_cat == voc_start:
                vocab_df = pd.concat([vocab_df, page_df], ignore_index=True)
            else:
                grammar_df = pd.concat([grammar_df, page_df], ignore_index=True)
        except Exception as e:
            alt_link_df = pd.concat([alt_link_df, row], ignore_index=True)
        row_index = row.index[0]
        link_df.drop(link_df.index[row_index], inplace=True)
        link_df = link_df.sample(frac=1, random_state=42).reset_index(drop=True) # Scramble remaining links again
        pbar.update(1)
        sleep(1) # Play Nice
    pbar.close()
    with pd.ExcelWriter(file, engine='openpyxl') as writer:
        kanji_df.to_excel(writer, sheet_name='Kanji', index=False)
        vocab_df.to_excel(writer, sheet_name='Vocab', index=False)
        grammar_df.to_excel(writer, sheet_name='Grammar', index=False)
    alt_link_df.to_csv(alt_file, sep='\t', index=False)