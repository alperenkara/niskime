from functools import wraps 
from flask import request, redirect, url_for, session
import random 
import string 

def login_required(f):
    @wrap(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None: 
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def random_str(digit = 4):
    chars = ""
    for i in range(digit):
        chars += random.choice(string.ascii_letters + string.digits)
    return chars 