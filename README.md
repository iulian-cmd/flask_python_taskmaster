### Python task app with Flask. A basic CRUD app.

Install Python and pip. We use pip if we use packages for python2 and pip3 if we use packages for python3.

Create a folder for the project. 

Creating the virtual environment is done by executing the command `venv`:

```python
python3 -m venv /path/to/new/virtual/environment
```

Activate the environment:

```python
.\venv\Scripts\Activate.ps1
```

The terminal in the IDE should look like this:

```python
(venv) PS C:\Users\user\Documents\_python\FlaskIntroduction> 
```

Install the requirements in the environment:

```python
pip3 install flask flask-sqlalchemy
```

The install includes werkzeug which is the wsgi server `flask` is based on.



In the project folder we create app.py

Inside we import flask

```python
from flask import Flask
```

We setup our application:

```python
app = Flask(__name__)
```

Create an index route:

```
@app.route('/')
```

We create a function index which return a string for the moment. See if that works.

```python
def index():
​	return "Hello World!"
```

This is a boilerplate code that protects users from accidentally invoking the script when they didn't intend to. It is called also a guard script. Or an idiom of python.

```python
if __name__ == "__main__":
	app.run(debug=True)
```

We can test if the app is running at this point by typing:

```python
python3 app.py
```

Create folder name static

Create folder name templates. Import render_template in app.py. Create index.html in template folder.

In the app.py in the routing we change "Hello World" with:

```python
render_template('index.html')
```

In the index.html we write something like Hello World 2. When server refreshes we can see that Hello World 2 is displayed.

We need to use template inheritance to avoid writing boiling plate template each time
For that we create base.html in templates and start writing blocks with jinja2 template syntax (module for jinja2 must be installed). 

```jinja2
Delimiters in jinja2
{%....%} are for statements
{{....}} are expressions used to print to template output
{#....#} are for comments which are not included in the template output
#....## are used as line statements
```

After creating template in base with lines like {% block head %} {% endblock %} we delete boiler plate in index.html and we write
{% extends 'base.html' %} and use the blocks from the base templates.
		

```jinja2
{% comment %} inherits the template from base.html {% endcomment %}       

 {% extends 'base.html' %}

{% comment %} Starting of the head block {% endcomment %}    

 {% block head %}     etc.
```

We put <title> in the head block

In the static folder we create css folder  and file main.css. We link the main.css in the base.html like this 

```python
<link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
```


Function url_for must be imported in app.py


### Database
in the app.py we import sql alchemy
We create the config file that tells us where the database is located

```python
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db' 
```

(/// is relative path and //// is absolute path)     //// 4 on Linux

We initialize the database with 

```sqlite
db=SQLAlchemy(app)
```

Next we create the model by writing a class

```sqlite
class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer,  deafault=0)
    date_created = dbColumn(db.DateTime, default=datetime.utcnow)
```

import datetime from datetime in the app.py

We create a function which will return a string every time we create an element:

```python
def __ref__(self):
    return '<Task %R>' % self.id
```

Creating the database: we go in the terminal type python3, in python3 we type:

```sqlite
from app import db  
db.create_all() 
exit()
```

that will create the test.db database in the main folder

In the body of the index we create a div with class content where we put the Task Master layout.

in the routing we add methods POST and GET like this

```python
@app.route('/', methods=['POST', 'GET'])
```

in the index.html we create a form like this:

```python
<form action="/" method="POST"> 
  <input type="text" name="content" id="content" /> 
  <input type="submit" value="Add Task" />
</form>
```

We start creating conditions by importing request in app.py

```python
from flask import request.
```

if the request that's set to the route is POST do smth:

```python
if request.method == 'POST':
    return "Hello"  // it returns Hello no matter what we input 
else:
    return render_template('index.html)
```

We start create the logic in the return of the if statement:

```python
task_content = request.form['content']
```

We create a model for the task

```python
new_task = ToDo(content=task_content)
```

Now we push the content of the task to the test database. Start by importing redirect.

```python
try:
db.session.add(new_task)
db.session.commit()
return redirect('/')

except: 
return "There was an issue adding your task"
```

In the else statement we add
```python
tasks = ToDo.query.order_by(ToDo.date_created).all()
```
this is going to look at all of the database content in order they were created.
We have to add tasks=tasks to the return template arguments.

In index we create a block for 

```python
{% for task in tasks%}

{% endfor %}
```
In the first containing td we put 

```python
      <td>{{ task.content}}</td>
```

and in the second 

```python
      <td>{{ task.date_created.date() }}</td>
```
For delete and update functions we need to create new routes.
we will select which task to delete or update with the help of task id.

For delete:
```python
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = ToDo.query.get_or_404(id)

try:
    db.session.delete(task_to_delete)
    db.commit()
    return redirect('/')
except:
    return "There was a problem deleting that task"
```
add this to the index.html at the corresponding td

```python
<a href="/delete/{{ task.id }}">Delete</a>
```

For update:
create new template called update.html in templates
The form inside the update.html should look like this 

```python
 <form action="/update/{{ task.id }}" method="POST">
      <input
        type="text"
        name="content"
        id="content"
        value="{{ task.content }}"
      />
      <input type="submit" value="Update" />
  </form>
```

```python
@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = ToDo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue updating your task"
    else:
    return render_template('update.html', task=task)
```

