from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from werkzeug.utils import redirect
# from app import db



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #3 /// is a relative path while 4 is an absolute path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app) #initialise database

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    completed = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods = ['POST', 'GET'])
def home():
    if request.method == 'POST':
        task_content = request.form['content']
        if len(task_content) < 1:
            task_content = None
        new_task = Todo(content = task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return redirect('/')

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('home.html', tasks = tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting that task"

@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form["content"]

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue udating the task"

    else:
        return render_template('/update.html', task = task)

if __name__ == '__main__':
    app.run(debug = True)
 




