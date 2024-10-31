from flask import Flask, jsonify, request
from datetime import datetime, timezone
from flask_sqlalchemy import  SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
db = SQLAlchemy(app)

#Todo list structure
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    job_description = db.Column(db.String(80), nullable = False)
    completed  = db.Column(db.Boolean, default = False)
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

#create a database
with app.app_context():
    db.create_all()

#Create job in to-do-list
@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.json
    new_todo = Todo(job_description = data['job_description'])
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({"message": "New job created!"}), 201

#get the list of jobs in to-do-list
@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([{"id": todo.id, 
                     "job_description": todo.job_description, 
                     "completed": todo.completed, 
                     'date_created': todo.date.strftime("%Y-%m-%d %H:%M:%S")} 
                     for todo in todos])

#update an item in the to-do-list
@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    data = request.json
    todo = Todo.query.get(id)
    if not todo:
        return jsonify({"error": "Job not found"}), 404
    
    # Update only provided fields
    if 'job_description' in data:
        todo.job_description = data['job_description']
    if 'completed' in data:
        todo.completed = data['completed']
    
    # Update date_created to reflect the last modification time
    todo.date_created = datetime.utcnow()
    
    db.session.commit()
    return jsonify({"message": "Job List updated!"})

#Delete an item from the list
@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get(id)
    if not todo:
        return jsonify({"error": "Job not found"}), 404
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"message": "Job deleted!"})



