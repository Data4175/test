# Здесь будет код веб-приложения
from random import randint
from flask import Flask, session, redirect, url_for, request, render_template
from db_scripts import get_question_after, get_quiz, check_answers
from random import shuffle
import os

def start_quiz(quiz_id):
    session['quiz'] = quiz_id
    session['question'] = 0
    session['answers'] = 0
    session['total'] = 0

def end_quiz():
    session.clear()

def quiz_form():
    quiz = get_quiz()
    return render_template('start.html', quiz_list=quiz)

def question_form(question):
    answers_list = [question[2], question[3], question[4], question[5]]
    shuffle(answers_list)
    return render_template('test.html', quest_id=question[0], question=question[1], answers=answers_list)

def save_answers():
    answer = request.form.get('ans_text')
    question_id = request.form.get('q_id')
    session['question'] = question_id
    session['total'] += 1
    if check_answers(question_id, answer):
        session['answers'] += 1
        print('Правильно')

def index():
    # session['question'] = 0
    # session['quiz'] = randint(1, 3)
    if request.method == 'GET':
        start_quiz(-1)
        return quiz_form()
    else:
        quiz_id = request.form.get('quiz')
        start_quiz(quiz_id)
        return redirect(url_for('test'))


    # return '<a href="/test">Викторина</a>'

def test():
    if not ('quiz' in session) or int(session['quiz']) < 0:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            save_answers()
        result = get_question_after(session['question'], session['quiz'])
        if result is None or len(result) == 0:
            return redirect(url_for('result'))
        else:
            return question_form(result)

def result():
    data = render_template('result.html', true_answers=session['answers'], answers=session['total'])
    end_quiz()
    return data

folder = os.getcwd()
app = Flask(__name__, template_folder=folder, static_folder=folder)

app.add_url_rule('/', 'index', index, methods=['get', 'post'])
app.add_url_rule('/test', 'test', test, methods=['get', 'post'])
app.add_url_rule('/result', 'result', result)

app.config['SECRET_KEY'] = 'Quiz'

if __name__ == '__main__':
    app.run(host=('0.0.0.0'))
