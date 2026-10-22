# William Keilsohn
# August 13 2026

# Import Packages
import os
import numpy as np
import pandas as pd

## Import Custom Scripts
from question import *

# Define Variables
ques_asked = 0
ques_right = 0

# Run Application
if __name__=='__main__':
    run_checker = 1
    while run_checker > 0:
        x = getProcessQuestion()
        if x == 1:
            ques_asked += 1
            ques_right += 1
        elif x > 1:
            ques_asked += 1
        else:
            run_checker = 0
    score = round((ques_right / ques_asked) * 100, 2)
    results = '''
    Number of Questions Correct: {}
    Number of Questions Asked: {}
    Total Score: {}
    '''.format(ques_right, ques_asked, score)
    print(results)