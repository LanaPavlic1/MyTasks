from flask import Flask, render_template, request, jsonify
from pony.flask import Pony
from pony.orm import db_session, select
from models import Task

app = Flask(__name__)
app.config['PONY'] = {
    'provider': 'sqlite',
    'filename': 'tasks.db',
}

pony = Pony(app)

@app.route('/')
def index():
    with db_session:
        tasks = select(t for t in Task).order_by(Task.created_at)
    return render_template('main.html', tasks=tasks)


@app.route('/add_task', methods=['POST'])
def add_task():
    content = request.form.get('content')
    deadline = request.form.get('deadline')
    with db_session:
        task = Task(content=content, deadline=deadline)
    task_data = {
        'id': task.id,
        'content': task.content,
        'deadline': task.deadline.strftime('%Y-%m-%d') if task.deadline else None
    }
    return jsonify(task_data)


@app.route('/edit_task/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    content = request.form.get('content')
    deadline = request.form.get('deadline')
    completed = request.form.get('completed') == 'true'

    with db_session:
        task = Task.get(id=task_id)
        if task:
            task.content = content
            task.deadline = deadline
            task.completed = completed
            return jsonify({'message': 'Task edited successfully'})
        else:
            return jsonify({'message': 'Task not found'}), 404



@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    with db_session:
        task = Task.get(id=task_id)
        if task:
            task.delete()
            return jsonify({'message': 'Task deleted successfully'})
        else:
            return jsonify({'message': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
