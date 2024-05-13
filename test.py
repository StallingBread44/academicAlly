from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

todos = {}


@app.get('/')
def home():
    return render_template('Website.html', todos = todos)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        print(request.form.get('userInput'))
        return redirect(url_for('home'))
    return render_template('Website.html')