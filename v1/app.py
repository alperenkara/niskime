from flask import Flask, session, redirect, url_for, render_template, request
import helpers
import sqlite3
from passlib.hash import sha256_crypt

conn = sqlite3.connect("db.sqlite3",
                       check_same_thread=False
)

c = conn.cursor()

app = Flask(__name__)

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
    
    