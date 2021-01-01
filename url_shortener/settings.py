import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') # 'sqlite:///db.sqlite3' # os.environ.get('DATABASE_URL') #  #  # 
SQLALCHEMY_TRACK_MODIFICATIONS = False
ADMIN_USERNAME = os.environ.get('ADMIN_PASSWORD')
ADMIN_PASSWORD = os.environ.get('ADMIN_USERNAME')