# William Keilsohn
# August 14 2026

# Import Packages
import os
from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap5

## Import Custom Scripts
from question import *

# Declare Instances
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = 'Kimigayo' # Don't EVER do this in PROD!!!

## Flask Safety Stuff
if(__name__=='__main__'):
    app.run(debug=True) # Set this to False for PROD

# Define Routes
@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')
    
@app.route("/results")
def results(total_ques=0):
    total_ques = session.get('total_ques')
    ques_corr = session.get('ques_corr')
    try:
        total_ques = session.get('total_ques')
    except:
        return redirect(url_for('index'))
    if total_ques == 0:
        return redirect(url_for('index')) # Nothing to see here.
    ques_corr = session.get('ques_corr')
    ans_corr_per = round(ques_corr / total_ques, 2) * 100
    if ans_corr_per < 80:
       res_mood_color = "#c20e0e"
    else:
       res_mood_color = "#0ec211"
    return render_template('results.html', ques_corr=ques_corr, ans_corr_per=ans_corr_per, total_ques=total_ques, res_mood_color=res_mood_color)
        
@app.route("/quiz", methods=['GET', 'POST'])  
def quiz():
    if request.method == 'POST':
        if 'exit_quiz' in request.form:
            return redirect(url_for('results'))
        else:
            user_ans = int(request.form.get('ans_button'))
            ques_ans = int(session.get('q_a'))
            ques_index = int(session.get('q_i'))
            cor_val = processFlaskAnswer(user_ans, ques_ans, ques_index)
            if cor_val > 0:
                flash("Correct", "success")
            else:
                flash("Incorrect", "danger")
            session['total_ques'] += 1
            session['ques_corr'] += cor_val
    else:
        session['total_ques'] = 0
        session['ques_corr'] = 0
    try:
        pg_question = getQuestion()
        q_body = pg_question['Question'].values[0]
        q_o_1 = pg_question['1'].values[0]
        q_o_2 = pg_question['2'].values[0]
        q_o_3 = pg_question['3'].values[0]
        q_o_4 = pg_question['4'].values[0]
        session['q_a'] = int(pg_question['Answer'].values[0])
        session['q_i'] = pg_question.index[0]
        return render_template('quiz.html', q_body=q_body, q_o_1=q_o_1, q_o_2=q_o_2, q_o_3=q_o_3, q_o_4=q_o_4)
    except:
        return redirect(url_for('results')) # Out of questions.
