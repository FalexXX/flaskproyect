import os
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(80), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
    


# SHOW TABLE AND ADD A NEW TASK
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        task_priority = int(request.form['priority'])
        task_status = request.form.get('status') == 'true'

        new_task = Todo(content=task_content,priority=task_priority,status=task_status)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks = tasks)


# DELETE TASK THROUGHT ID
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

# UPDATE TASK WITH FORM'S INFORMATION
@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        # Convert priority from string to integer
        task_priority = int(request.form['priority'])
        task.priority = task_priority
        # Convert status from string to boolean
        task_status = request.form.get('status') == 'true'
        task.status = task_status
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)

# DELETE DATABASE
@app.route('/delete-db')
def delete_database():
    db_path = os.path.join(app.root_path, './instance/test.db')
    if os.path.exists(db_path):
        os.remove(db_path)
        return 'Database deleted successfully'
    else:
        return 'Database file does not exist'


if __name__ == '__main__':
    app.run(debug=True)