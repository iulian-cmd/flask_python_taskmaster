# import the flask
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# create the app
app = Flask(__name__)
# create the config file that tells us where the database is located
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# initialize database by passing the app as argument (without .py)
db = SQLAlchemy(app)

# creating a class with the model of the database


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer,  default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # create a function that return a string every time we create an element
    def __ref__(self):
        return '<Task %R>' % self.id

# use the decorator @ to assign the routing


@app.route('/')
def index():
    return render_template('index.html')


#
if __name__ == "__main__":
    app.run(debug=True)
