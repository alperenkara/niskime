from flask import Flask, session, redirect, url_for, render_template, request
from helpers import *
import sqlite3
from passlib.hash import sha256_crypt

conn = sqlite3.connect("db.sqlite3",
                       check_same_thread=False
)

c = conn.cursor()

app = Flask(__name__)

app.config["SECRET_KEY"] = "secretkey"

BASE_URL = "http://127.0.0.1:5000/"

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST": 
        if not request.form.get("url"):
            return "Please fill out the form with required details."
        
        auto_code = random_str()
        
        codes = c.execute("SELECT * FROM urls WHERE auto_code=:auto_code OR code=:auto_code",{"auto_code" : auto_code}).fetchall()
        

        
        while len(codes) != 0:
            auto_code = random_str()
            codes = c.execute("SELECT * FROM urls WHERE auto_code=:auto_code OR code=:auto_code",{"auto_code": auto_code}).fetchall()
        
        c.execute("INSERT INTO urls (original_url, auto_code, code) VALUES (:o_url, :code, :code)",{"o_url":request.form.get("url"),"code":auto_code})
                  
        conn.commit()
        
        return render_template("success.html", BASE_URL = BASE_URL, auto_code = auto_code)
        
    else:
        return render_template("index.html")

# @login_required



@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        # check the form validation 
        if not request.form.get("email") or not request.form.get("password") or not request.form.get('confirmation'):
            return "please fill out the form elements."
        
        if request.form.get("password") != request.form.get("confirmation"):
            return "password confirmation has been not matched."
        # check the email whether it's already in the DB or not. 
        exist = c.execute("SELECT * FROM users WHERE email=:email", {"email":request.form.get("email")}).fetchall()
        
        if len(exist) != 0:
            return "The email has used before."
        # hash the password 
        
        pwhash = sha256_crypt.encrypt(request.form.get("password"))
        # put the variables into the DB
        c.execute("INSERT INTO users (email, password) VALUES (:email, :password)",
                  {"email":request.form.get("email"),
                   "password":pwhash})
        conn.commit()
        return ('seccessful return')
    else:
        return render_template("register.html")
    
@app.route("/login", methods =["GET", "POST"])

def login():
    
    if request.method == "POST": 
        # check from validation
        
        if not request.form.get("email") or not request.form.get("password"):
            return "please fill out the form elements."
        
        # check the user email if it's in the DB. 
        
        # it returns a list of tuples.
        
        # fetches all the rows of a query result. It returns all the rows as a list of tuples. An empty list is returned if there is no record to fetch.
        
        # # [(6, 'test@test.com', '$5$rounds=535000$vbUOCyTadP2EwbO/$BSAiRFL2lbfwfTGjdhG6DGzVgTTVbrg.BUNyUHfIG08')]
        
        user = c.execute("SELECT * FROM users WHERE email=:email", {"email": request.form.get("email")}).fetchall()
        
        if len(user) != 1:
            return "You aren't registered."
        
        # check password hash. 
        # [(6, 'test@test.com', '$5$rounds=535000$vbUOCyTadP2EwbO/$BSAiRFL2lbfwfTGjdhG6DGzVgTTVbrg.BUNyUHfIG08')]
        pwhash = user[0][2]
        
        if sha256_crypt.verify(request.form.get("password"),pwhash) == False: 
            return "Wrong Password"
        
        # Login to the system via user session
        session["user_id"] = user[0][0]
        
        # if it's a sucsefull event forward the user to the dashboard. 
        
        return redirect("/dashboard")
    
    else: 
        return render_template("login.html")
    
@app.route("/logout")

def logout():
    
    session.clear()
    
    return redirect(url_for("login"))


@app.route("/url/<string:code>")
def url(code):
    result = c.execute("SELECT original_url FROM urls WHERE code=:code", {"code":code}).fetchall()
    
    if len(result) != 1:
        return "404"
    return redirect(result[0][0])
    

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)