import string
from random import choice
from datetime import datetime

from .extensions import db

class Link(db.Model):
    id = db.Column(db.Integer, primary_key = True) # primary
    original_url = db.Column(db.String(512)) # input URL
    short_url = db.Column(db.String(5), unique = True) # shortened URL 
    visits = db.Column(db.Integer, default = 0 ) # user visit
    date_created  = db.Column(db.DateTime, default = datetime.now) # date 
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.short_url = self.generate_short_link
        
        
    def generate_short_link(self):
        characters = string.digits + string.ascii_letters
        short_url = ''.join(choices(characters,k=5)) # 5 characters from random choices
        
        link = self.query.filter_by(short_url=short_url).first() # checking DB about shortened url
        
        if link: # if the short URL has been used before, it will generate a new one. 
            return self.generate_short_link() 
        
        return str(short_url)