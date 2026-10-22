# William Keilsohn
# August 10 2026

# Import Packages
import pandas as pd
from bs4 import BeautifulSoup as bsf4
import re

# Define Variables
cols = ['Question', '1', '2', '3', '4', 'Answer'] # 'Sentence',
page_splitter = '<hr class="wp-block-separator has-alpha-channel-opacity"/>'
key_splitter = '<p><strong>Answer Key:</strong></p>'
alt_page_splitter = '</p>\n<p><strong>New words:</strong></p>'

# Define functions    
def getSection(html_content):
    global page_splitter
    soup = bsf4(html_content, "html.parser")
    soup = str(soup.find('div',  class_='entry clearfix'))
    cut_soup = soup.split(page_splitter, maxsplit=1)[0]
    cut_soup = cut_soup.split(alt_page_splitter, maxsplit=1)[0] # Double checks when there is no bar.
    return cut_soup
 
def getAnswerKey(cut_soup):
    global key_splitter
    key_str = cut_soup.split(key_splitter)[1]
    raw_answer_ls = key_str.split('Question')
    answer_ls = []
    for i in raw_answer_ls:
        ans = re.search(r":\s*(\d+)", i)
        try:
            ans_raw_val = ans.group()
            ans_num_val = ans_raw_val.split(' ')[1]
            answer_ls.append(ans_num_val)
        except:
            pass # Sometimes grabs some extra starting characters
    return answer_ls
    
def makeQsoup(cut_soup):
    global key_splitter
    return cut_soup.split(key_splitter)[0]
    
def getAnswerOptions(q_cut_soup):
    options_df = pd.DataFrame(columns = ['1', '2', '3', '4'])
    pattern = r"<input(.*?)<"
    option_ls = re.findall(pattern, q_cut_soup, re.DOTALL)
    for i in option_ls:
        nums = re.findall(r'\d+', i)
        row_num = nums[0]
        col_num = nums[1]
        value = i.split('> ')[1]
        options_df.at[row_num, str(col_num)] = value
    return options_df
    
def getQuestions(q_cut_soup):
    pattern = r"<p>(.*?)<b"
    ques = re.findall(pattern, q_cut_soup, re.DOTALL)
    ques = [x for x in ques if any(char.isdigit() for char in x)]
    starter = [ques[0]] # Make sure the first question is preserved. 
    filtered_ques = [item for i, item in enumerate(ques) if item[0] not in [x[0] for x in ques[i + 1 :]]] # Some pages put an extra number in the sentences.
    ques = list(dict.fromkeys(starter + filtered_ques)) # Removes duplicates
    question_ls = []
    for i in ques:
        j = re.sub(r'\d+', '', i)
        j = j.split('</p>')[0]
        j = j.replace('<span class="auto-style"', '').replace('/span>', '').replace('=','').replace('"','').replace('-','')
        question_ls.append(j.replace('. ', ''))
    question_ls = [re.sub(r'[a-zA-Z]', '', x) for x in question_ls]
    return question_ls

def getSentences(q_cut_soup):  
    pattern = r"<p>(.*?)</p>"
    sents = re.findall(pattern, q_cut_soup, re.DOTALL)
    sents = [x for x in sents if 'span' in x]
    sents = [re.sub(r'[\x00-\x7F]', '', x) for x in sents]
    return sents
    
def compileQDF(cut_soup):
    answer_ls = getAnswerKey(cut_soup=cut_soup)
    q_cut_soup = makeQsoup(cut_soup=cut_soup)
    options_df = getAnswerOptions(q_cut_soup=q_cut_soup)
    question_ls = getQuestions(q_cut_soup=q_cut_soup)
    # sents_ls = getSentences(q_cut_soup=q_cut_soup) # Not sure how to add these to the table yet.
    options_df['Answer'] = answer_ls
    options_df.insert(0, 'Question', question_ls)
    return options_df