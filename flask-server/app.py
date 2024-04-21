from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import csv
import os
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

def getDiabetesData():
    data = pd.read_csv('datadb.csv')
    diabetes = pd.read_csv('diabetes.csv')

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(data.loc[:, data.columns != 'Outcome'], data['Outcome'], stratify=data['Outcome'], random_state=66)
    from sklearn.neighbors import KNeighborsClassifier
    training_accuracy = []
    test_accuracy = []
    # setting closest data points or nearest neighbors for testing 
    neighbors_settings = range(1, 11)
    for n_neighbors in neighbors_settings:
        # building the model
        knn = KNeighborsClassifier(n_neighbors=n_neighbors)
        knn.fit(X_train, y_train)
        # training set accuracy
        training_accuracy.append(knn.score(X_train, y_train))
        # test set accuracy
        test_accuracy.append(knn.score(X_test, y_test))

    knn = KNeighborsClassifier(n_neighbors=9)
    knn.fit(X_train, y_train)

    predictions = knn.predict(diabetes.loc[:, diabetes.columns != 'Outcome'])
    file_name = os.path.splitext('diabetes.csv')[0]
    for idx, prediction in enumerate(predictions):
        if prediction == 1:
            print(f"Person {idx+1} Has Diabetes")
        else:
            print(f"Person {idx+1} Does not have Diabetes")
    os.remove('diabetes.csv')

def getKidneyData():
    data = pd.read_csv('datakd.csv')
    kidney = pd.read_csv('kidney.csv')

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(data.loc[:, data.columns != 'Outcome'], data['Outcome'], stratify=data['Outcome'], random_state=66)
    from sklearn.neighbors import KNeighborsClassifier
    training_accuracy = []
    test_accuracy = []
    # setting closest data points or nearest neighbors for testing 
    neighbors_settings = range(1, 11)
    for n_neighbors in neighbors_settings:
        # building the model
        knn = KNeighborsClassifier(n_neighbors=n_neighbors)
        knn.fit(X_train, y_train)
        # training set accuracy
        training_accuracy.append(knn.score(X_train, y_train))
        # test set accuracy
        test_accuracy.append(knn.score(X_test, y_test))

    knn = KNeighborsClassifier(n_neighbors=9)
    knn.fit(X_train, y_train)

    predictions = knn.predict(kidney.loc[:, kidney.columns != 'Outcome'])
    file_name = os.path.splitext('kidney.csv')[0]
    for idx, prediction in enumerate(predictions):
        if prediction == 1:
            print(f"Person {idx+1} Has Kidney Issues")
        else:
            print(f"Person {idx+1} Does not have Kidney Issues")
    os.remove('kidney.csv')


def getCancerData():
    data = pd.read_csv('datac.csv')
    cancer = pd.read_csv('cancer.csv')

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(data.loc[:, data.columns != 'Outcome'], data['Outcome'], stratify=data['Outcome'], random_state=66)
    from sklearn.neighbors import KNeighborsClassifier
    training_accuracy = []
    test_accuracy = []
    # setting closest data points or nearest neighbors for testing 
    neighbors_settings = range(1, 11)
    for n_neighbors in neighbors_settings:
        # building the model
        knn = KNeighborsClassifier(n_neighbors=n_neighbors)
        knn.fit(X_train, y_train)
        # training set accuracy
        training_accuracy.append(knn.score(X_train, y_train))
        # test set accuracy
        test_accuracy.append(knn.score(X_test, y_test))

    knn = KNeighborsClassifier(n_neighbors=9)
    knn.fit(X_train, y_train)

    predictions = knn.predict(cancer.loc[:, cancer.columns != 'Outcome'])
    file_name = os.path.splitext('cancer.csv')[0]
    for idx, prediction in enumerate(predictions):
        if prediction == 1:
            print(f"Person {idx+1} Has Cancer")
        else:
            print(f"Person {idx+1} Does not have Cancer")
    os.remove('cancer.csv')

def write_person_data_to_csv(people_data, filename):
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='') as csvfile:  # Use 'a' mode to append to existing file
        csv_writer = csv.writer(csvfile)

        # Write headers if the file doesn't exist
        if not file_exists:
            headers = [key for key, _ in people_data[0]]
            csv_writer.writerow(headers)

        # Write data for each person
        for person in people_data:
            data = [value for _, value in person]
            csv_writer.writerow(data)



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign')
def sign():
    return render_template('sign.html')

@app.route('/framework', methods=['GET', 'POST'])
def framework():
    return render_template('framework.html')

@app.route('/report', methods=['GET', 'POST'])
def report():
    return render_template('report.html')

@app.route('/processdbinput', methods=['GET', 'POST'])
def processdbinput():
    if request.method == 'POST':
        age_input = request.form['age']
        bmi_input = request.form['bmi']
        glucose_input = request.form['glucose']
        iron_input = request.form['iron']
        calcium_input = request.form['calcium']
        def get_person_data_from_input():
            age = age_input
            bmi = bmi_input
            glucose = glucose_input
            iron = iron_input
            calcium = calcium_input
            return [('Age', age), ('BMI', bmi), ('Glucose', glucose), ('Iron', iron), ('Calcium', calcium), ('Outcome', 0)]
        patientdbdata = [get_person_data_from_input()]
        write_person_data_to_csv(patientdbdata, 'diabetes.csv')
        getDiabetesData()
        
    return render_template('report.html')

@app.route('/processkidneyinput', methods=['GET', 'POST'])
def processkidneyinput():
    if request.method == 'POST':
        age_input = request.form['age']
        bmi_input = request.form['bmi']
        electrolyte_input = request.form['electrolyte']
        creatine_input = request.form['creatine']
        nitrogen_input = request.form['nitrogen']
        def get_person_data_from_input():
            age = age_input
            bmi = bmi_input
            electrolyte = electrolyte_input
            creatine = creatine_input
            nitrogen = nitrogen_input
            return [('Age', age), ('BMI', bmi), ('Electrolyte', electrolyte), ('Creatine', creatine), ('Nitrogen', nitrogen), ('Outcome', 0)]
        patientdbdata = [get_person_data_from_input()]
        write_person_data_to_csv(patientdbdata, 'kidney.csv')
        getKidneyData()
    return render_template('report.html')

@app.route('/processcancerinput', methods=['GET', 'POST'])
def processcancerinput():
    if request.method == 'POST':
        age_input = request.form['age']
        bmi_input = request.form['bmi']
        whitebloodcell_input = request.form['wbc']
        cea_input = request.form['cea']
        af_input = request.form['af']
        def get_person_data_from_input():
            age = age_input
            bmi = bmi_input
            whitebloodcell = whitebloodcell_input
            cea = cea_input
            af = af_input
            return [('Age', age), ('BMI', bmi), ('Whiteblood', whitebloodcell), ('Cea', cea), ('AF', af), ('Outcome', 0)]
        patientdbdata = [get_person_data_from_input()]
        write_person_data_to_csv(patientdbdata, 'cancer.csv')
        getCancerData()
    return render_template('report.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username, password=password).first()

    if user:
        return render_template('index.html')
    else:
        return render_template('sign.html', error="Try Again: Invalid username or password")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    new_user = User(username=username, password=password, email=email)
    db.session.add(new_user)
    db.session.commit()

    return render_template('index.html')
    



if __name__ == "__main__":
    app.run(debug=True, port=4999)