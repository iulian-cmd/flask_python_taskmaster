# 🐍 Flask Task App — Simple Python CRUD

A minimal task management app built with **Flask** and **SQLite**, demonstrating basic CRUD operations.

---

## 🚀 Getting Started

### 1. Environment Setup

Ensure Python 3 and pip are installed. Then, create and activate a virtual environment:

```bash
# Create environment
python3 -m venv venv

# Activate on Windows PowerShell
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```bash
pip install flask flask-sqlalchemy
```

> Flask uses **Werkzeug** as the underlying WSGI server.

---

## 🏗 Project Structure

```
project/
├── app.py
├── static/
│   └── css/
│       └── main.css
├── templates/
│   ├── base.html
│   ├── index.html
│   └── update.html
└── README.md
```

---

## 🔧 app.py Overview

### Basic Setup

```python
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
```

### Database Model

```python
class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.id}>'
```

### Initialize Database

```bash
python
>>> from app import db
>>> db.create_all()
>>> exit()
```

---

## 🌐 Routes & Views

### Home Route

```python
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = ToDo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = ToDo.query.order_by(ToDo.date_created).all()
        return render_template('index.html', tasks=tasks)
```

### Delete Task

```python
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = ToDo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'
```

### Update Task

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
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)
```

---

## 🧩 Templates & Styling

### Jinja2 Basics

- `{% ... %}`: statements (e.g., `for`, `if`)
- `{{ ... }}`: expressions (e.g., `task.content`)
- `{# ... #}`: comments

### Base Template (`base.html`)

Define a base layout with blocks:

```html
<!doctype html>
<html lang="en">
<head>
  <title>{% block title %}Task Master{% endblock %}</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
</head>
<body>
  {% block content %}{% endblock %}
</body>
</html>
```

### Extending Template (`index.html`)

```html
{% extends 'base.html' %}

{% block content %}
  <form action="/" method="POST">
    <input type="text" name="content" />
    <input type="submit" value="Add Task" />
  </form>

  <table>
    {% for task in tasks %}
      <tr>
        <td>{{ task.content }}</td>
        <td>{{ task.date_created.date() }}</td>
        <td><a href="/delete/{{ task.id }}">Delete</a></td>
        <td><a href="/update/{{ task.id }}">Update</a></td>
      </tr>
    {% endfor %}
  </table>
{% endblock %}
```

---

## ✅ Run the App

```bash
python app.py
```

Visit: [http://localhost:5000](http://localhost:5000)

---

## 📄 License

MIT — Feel free to use and modify this project.

