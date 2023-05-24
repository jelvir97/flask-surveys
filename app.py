from flask import Flask,request, flash,render_template, redirect, session
from surveys import *
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY']  = "dogs"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']  = False
debug = DebugToolbarExtension(app)



@app.route('/')
def home_page():

    return render_template('home.html', surveys=surveys)

@app.route('/start_survey/<surv>',methods=['POST'])
def survey_start(surv):
    """iniztalizes response list within session"""
    session[f'{surv}_response'] = []
    responses = session[f'{surv}_response']
    return redirect(f'/{surv}/question/{len(responses)}')


@app.route('/<surv>/question/<num>', methods=['GET','POST'])
def question(surv, num):
    responses = session[f'{surv}_response']
    survey = surveys[surv]
    if int(num) == len(responses):
        if request.method == 'GET': 
            q = survey.questions[int(num)]
            print(num)
            return render_template('question.html', question=q.question, choices=q.choices,q_num=num,surv=surv)
        if request.method == 'POST':
            num = int(num)
            num +=1
            responses.append(request.form.get('response'))
            
            print('*********')
            for resp in responses:
                print(resp)
            print('*********')
            print(surv)
            session[f'{surv}_response'] = responses

            if num >= len(survey.questions):
                return redirect(f'/thankyou/{surv}')
            
            return redirect(f'/{surv}/question/{num}')
    else:
        print('*********')
        for resp in responses:
                print(resp)
        print('*********')
        flash("You are trying to access an invalid question. Please complete questions in order.")
        return redirect(f'{surv}/question/{len(responses)}')    
    
    

@app.route('/thankyou/<surv>')
def thankyou(surv):   
    survey = surveys[surv]
    responses = session[f'{surv}_response']
    
    questions_and_answers = {survey.questions[i].question : responses[i] for i in range(len(responses))}    
    return render_template('thankyou.html',questions_and_answers=questions_and_answers)


