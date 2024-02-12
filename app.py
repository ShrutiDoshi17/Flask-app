from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)  #set up our application and __name__ ref this file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'    #this is telling are app where are database located
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self): 
        return'<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])   #when we brouse url we don't get 404, and here it will pass url str
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()  #this will put all db content in order and return all of them, can also take first()
        return render_template('index.html', tasks = tasks)  #writing just name of file no folder
    
@app.route('/delete/<int:id>')   
def delete(id):
    task_to_delete  = Todo.query.get_or_404(id)
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'
    
@app.route('/update<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    
    if request.method == 'POST': 
        task.content = request.form['content']
        
        try:
            db.session.comit()
            return redirect('/')    #back to our home page
        
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)   
    

if __name__ == "__main__":
    app.run(debug = True)  #errors in webpage then we can see
   
