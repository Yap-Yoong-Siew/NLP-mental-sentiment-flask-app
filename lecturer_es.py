from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import json
from random import choice
import joblib
import pickle
from sklearn.feature_extraction.text import CountVectorizer



with open('model.pkl', 'rb') as f:
    cv, model = pickle.load(f)


with open('db.json') as f:
    data = json.load(f)

app = Flask(__name__)

student_info = {
    "Name": "",
    "Matric_Number": "",
    "Year": "",
    "Course": "",
}

curr_question = list(data.keys())[0]
curr_response = data[curr_question]
final_answer = ""


@ app.route('/')
def home():
    messages = [
    "I feel a deep sense of peace and contentment today, I want this to continue.",
    "Dealing with anxiety has been a constant struggle in my life, I need help.",
    "Practicing self-care helps me feel more balanced and grounded, change is coming.",
    "I often find myself overwhelmed by extreme negative thoughts and emotions.",
    "Engaging in creative activities brings me joy and a sense of fulfillment.",
    "The weight of depression feels heavy and suffocating for me, I want to stop.",
    "Reaching out to loved ones for support makes a difference in my mental well-being.",
    "Social media often leaves me feeling inadequate and anxious, I feel light.",
    "Taking more time for relaxation and mindfulness boosts my mental resilience.",
    "Living with a mental illness is challenging, but I am committed to my recovery.",
    "Expressing gratitude daily helps shift my perspective and cultivates positivity.",
    "I experience moments of intense stress and panic that are hard to manage.",
    "Spending time in nature rejuvenates my spirit and brings me peace that I've wanted.",
    "Feeling disconnected from others is a common struggle I've always face.",
    "Engaging in regular physical exercise positively impacts my mental health.",
    "The stigma surrounding mental health still prevents many from seeking help."
]
    message = choice(messages)

    return render_template("home.html", message=message)


@ app.route("/get-to-know", methods=["GET", "POST"])
def get_info():
    if request.method == "POST":
        nlp_text = request.form["name"]
        # ML model goes here

        global issue
        issue = mental_health_issue_detector(nlp_text)

        return redirect("/answer")

    return render_template("information.html")

def mental_health_issue_detector(text, model=model, cv=cv):
  text = cv.transform([text]).toarray()
  prediction = model.predict(text)
  if prediction == 1:
    return True
  else:
    return False


@ app.route("/introduction", methods=["GET", "POST"])
def intro():
    if request.method == "POST":
        response = request.form["response-button"]

        if response == "I want to develop a Database":
            return redirect("/develop-db")

        global curr_response
        global curr_question

        next_decision = curr_response[response]
        question = list(next_decision.keys())[0]
        next_responses = next_decision[question]
        curr_response = next_responses
        curr_question = question

        return redirect("/question")

    else:
        responses = list(curr_response.keys())
        return render_template("introduction.html", name=student_info["Name"], main_question=curr_question, responses=responses)


@ app.route("/question", methods=["GET", "POST"])
def questions():
    if request.method == "POST":
        response = request.form["response-button"]

        global curr_response
        global curr_question
        global final_answer

        next_decision = curr_response[response]

        if isinstance(next_decision, dict):
            question = list(next_decision.keys())[0]
            curr_question = question
            next_responses = next_decision[question]
            curr_response = next_responses

            return render_template("questions.html", main_question=question, responses=next_responses)
        else:
            curr_question = response
            # final_answer = next_decision
            return redirect("/answer")

    return render_template("questions.html", main_question=curr_question, responses=curr_response)


@ app.route("/answer", methods=["GET", "POST"])
def answer():
    if request.method == "POST":

        global curr_question
        curr_question = "empty_text"
 

 
        return redirect("/get-to-know")

    global issue
    if issue:
        final_answer = "You might have mental health issue. Please seek help from professional."
    else:
        final_answer = "You don't have mental health issue."

    return render_template("answer.html", question=curr_question, answer=final_answer)


@ app.route("/develop-db", methods=["GET", "POST"])
def develop_db():
    db_data = data['What would you like to learn today?']['I want to develop a Database']
    db_rules = []
    db_rules.extend(rule for rule in db_data['sql'])
    db_rules.extend(rule for rule in db_data['nosql'])

    if request.method == "POST":
        rule_ans = request.form.to_dict()

        ans_text = {'sql': 'Database that you should use is SQL Database. Sample of SQL database are MySQL, Oracle and PostgreSQL.',
                    'nosql': 'Database that you should use is NoSQL Database. Sample of NoSQL database are MongoDB and Firestore.',
                    'Not valid': 'There is no database type that can fulfill your requirements. Please try again.',
                    None: 'Please insert atleast one requirement and try again.'}
        result_db = None
        for rule in db_rules:
            if rule_ans[rule] == 'Yes':
                if rule in db_data['sql']:
                    if result_db is None:
                        result_db = 'sql'
                    elif result_db != 'sql':
                        result_db = 'Not valid'
                        break
                else:
                    if result_db is None:
                        result_db = 'nosql'
                    elif result_db != 'nosql':
                        result_db = 'Not valid'
                        break
            elif rule_ans[rule] == 'No':
                if rule in db_data['sql']:
                    if result_db is None:
                        result_db = 'nosql'
                    elif result_db == 'sql':
                        result_db = 'Not valid'
                        break
                else:
                    if result_db is None:
                        result_db = 'sql'
                    elif result_db == 'nosql':
                        result_db = 'Not valid'
                        break
        result_db = ans_text[result_db]
        return redirect(url_for('.answer', question="What type of Database should I use?", answer=result_db))
    return render_template("develop_db.html", db_rules=db_rules)


app.run(host='0.0.0.0', port=80)

