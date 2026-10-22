# William Keilsohn
# August 12, 2026

# Import packages
import os
import numpy as np
import pandas as pd

# Define Variables
cwd = os.getcwd()
file = os.path.join(cwd, 'questions.xlsx')

kan_df = pd.read_excel(file, engine='openpyxl', sheet_name='Kanji')
voc_df = pd.read_excel(file, engine='openpyxl', sheet_name='Vocab')
# gram_df = pd.read_excel(file, engine='openpyxl', sheet_name='Grammar') # Grammar has unique questions, so I'll deal with it later... maybe...

question_df = pd.concat([kan_df, voc_df])
question_df.drop(columns=['Page'], inplace=True)

# Define Functions
def askQuestion(question_sub_df):
    print(question_sub_df['Question'].values[0])
    options_dic = {x: question_sub_df[str(x)].values[0] for x in range(1,5)}
    for key, value in options_dic.items():
        option = '{}: {}'.format(key, value)
        print(option)
    user_ans = input('Please select an option: ') # User should enter a single number.
    return user_ans
    
def processAnswer(user_ans, ques_ans, ques_index):
    global question_df
    if user_ans > 4 or user_ans <= 0:
        return 0
    elif user_ans == ques_ans:
        print('Correct')
        question_df.drop(index=ques_index, inplace=True)
        return 1
    else:
        print('Incorrect')
        print('The correct answer is: {}'.format(ques_ans))
        return 2
        
def processFlaskAnswer(user_ans, ques_ans, ques_index):
    global question_df
    if user_ans == ques_ans:
        question_df.drop(index=ques_index, inplace=True)
        return 1
    else:
        return 0

def getProcessQuestion():
    global question_df
    question_df = question_df.sample(frac=1, random_state=42).reset_index(drop=True)
    question = question_df.sample()
    ans = question['Answer'].values[0]
    user_ans = int(askQuestion(question))
    return processAnswer(user_ans, ans, question.index[0])   
    
def getQuestion():
    global question_df
    question_df = question_df.sample(frac=1, random_state=42).reset_index(drop=True)
    question = question_df.sample()
    return question
    
# Run Application
# if __name__ == '__main__':
    # x = 1
    # while x > 0:
        # x = getProcessQuestion()