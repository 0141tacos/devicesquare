from flask import Flask
from flask import render_template, request, redirect


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def homepage():
    return render_template("homepage.html")