### Python task app with Flask












Create folder name static

Create folder name templates
import render_template in app.py
create index.html in template folder
in the app.py in the routing we change "Hello World" with render_template('index.html')

In the index.html we write something like Hello World 2. When server refresh we can see that Hello World 2 is displayed.

We need to use template inheritance to avoid writing boiling plate template each time
For that we create base.html in templates and start writing blocks with jinja2 template syntax (module for jinja2 must be installed). 

```
Delimiters in jinja2
{%....%} are for statements
{{....}} are expressions used to print to template output
{#....#} are for comments which are not included in the template output
#....## are used as line statements
```

After creating template in base with lines like {% block head %} {% endblock %} we delete boiler plate in index.html and we write
{% extends 'base.html' %} and use the blocks from the base templates.
{% comment %} inherits the template from base.html {% endcomment %}        {% extends 'base.html' %}

{% comment %} Starting of the head block {% endcomment %}     {% block head %}     etc.
We put <title> in the head block

In the static folder we create css folder  and file main.css. We link the main.css in the base.html like this 

```
<link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
```


Function url_for must be imported in app.py


### Database
in the app.py we import sql alchemy
We create the config file that tells us where the database is located

```
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db' 
```

(/// is relative path and //// is absolute path)     //// 4 on Linux

We initialize the database with 

```
db=SQLAlchemy(app)
```

Next we create the model by writing a class

```
class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer,  deafault=0)
    date_created = dbColumn(db.DateTime, default=datetime.utcnow)
```

import datetime from datetime in the app.py

We create a function which will return a string every time we create an element:

```
def __ref__(self):
    return '<Task %R>' % self.id
```

Creating the database: we go in the terminal type python3, in python3 we type:

```
from app import db  
db.create_all() 
exit()
```

that will create the test.db database in the main folder

In the body of the index we create a div with class content where we put the Task Master layout.

in the routing we add methods POST and GET like this

```
@app.route('/', methods=['POST', 'GET'])
```

in the index.html we create a form like this:

```
<form action="/" method="POST"> 
  <input type="text" name="content" id="content" /> 
  <input type="submit" value="Add Task" />
</form>
```



We start creating conditions by importing request in app.py
import request.

if the request that's set to the route is POST do smth:

```
    if request.method == 'POST':
    return "Hello"  // it returns Hello no matter what we input 
    else:
    return render_template('index.html)
```

We start create the logic in the return of the if statement:

```
task.content = request.form['content']
```

We create a model for the task

```
new_task = ToDo(content=task.content)
```

Now we push the content of the task to the test database. Start by importing redirect.

```
try:
db.session.add(new_task)
db.session.commit()
return redirect('/')

except: 
return "There was an issue adding your task"
```

In the else statement we add
```
tasks = ToDo.query.order_by(ToDo.date_created).all()
```
this is going to look at all of the database content in order they were created.
We have to add tasks=tasks to the return template arguments.

In index we create a block for 

```
{% for task in tasks%}

{% endfor %}
```
In the first containing td we put 

```
      <td>{{ task.content}}</td>
```

and in the second 

```
      <td>{{ task.date_created.date() }}</td>
```

