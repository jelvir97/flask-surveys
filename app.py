from flask import Flask,request, flash,render_template, redirect
from surveys import *
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY']  = "dogs"
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS']  = False
debug = DebugToolbarExtension(app)

responses = []


@app.route('/')
def home_page():
    survey_title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('home.html', survey_title=survey_title, instructions=instructions)

@app.route('/question/<num>', methods=['GET','POST'])
def question(num):
    if int(num) == len(responses):
        if request.method == 'GET': 
            q = satisfaction_survey.questions[int(num)]
            return render_template('question.html', question=q.question, choices=q.choices,q_num=num)
        if request.method == 'POST':
            num = int(num)
            num +=1
            responses.append(request.form.get('response'))
            for resp in responses:
                print(resp)
            if num >= len(satisfaction_survey.questions):
                return redirect('/thankyou')
            return redirect(f'/question/{num}')
    else:
        flash("You are trying to access an invalid question. Please complete questions in order.")
        return redirect(f'/question/{len(responses)}')    
    
    

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')


