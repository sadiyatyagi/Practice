from flask import Flask, jsonify, request
from data import tasks
app = Flask(__name__)

# Get all tasks
@app.route('/show-tasks', methods=['GET'])
def get_tasks():
    
    return jsonify({'tasks': tasks})

# Get a specific task
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is not None:
        return jsonify({'task': task})
    else:
        return jsonify({'message': 'Task not found'}), 404

@app.route('/tasks', methods=['GET'])
def get_task_by_query():
    
    task_id = request.args.get('id', type=int)

    done_status = request.args.get('done', type=bool)

    # Logic to handle querying tasks based on id and title
    if task_id is not None:
        task = next((task for task in tasks if task['id'] == task_id), None)

    
        if task is not None:
            if done_status:
                return jsonify({'task': task, "done": "This task will be completed."})
            else:
                return jsonify({'task': task, "done": "This task will not be completed."})

    return jsonify({'message': 'Task not found'}), 404

@app.route('/tasks/create-task', methods=['POST'])
def create_task_bydata():
    # Get data from request body
    task_data = request.json
    
    # Check if all required fields are present
    if 'id' not in task_data or 'title' not in task_data or 'description' not in task_data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Extract data
    task_id = task_data['id']
    title = task_data['title']
    description = task_data['description']
    
    # Create new task
    new_task = {
        'id': task_id,
        'title': title,
        'description': description,
        'done': False
    }
    
    # Append new task to tasks list
    tasks.append(new_task)
    
    # Return response
    return jsonify({'task': new_task}), 


@app.route('/tasks/update-task/<int:task_id>', methods=['PUT'])
def update_task_bydata(task_id):

    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is not None:
       
        # Get data from request body
        task_data = request.json
        
        # Check if all required fields are present
        if 'id' not in task_data or 'title' not in task_data or 'description' not in task_data or 'done' not in task_data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        task.update(task_data)


        # Return response
        return jsonify({'task': task}), 201


    else:
        return jsonify({'message': 'Task not found'}), 404
    

@app.route('/tasks/delete-task/<int:task_id>', methods=['DELETE'])
def delete_task_bydata(task_id):
   
    global tasks   
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is not None:
        tasks = [task for task in tasks if task['id'] != task_id]
        return jsonify({'message': 'Task deleted'}),201

    else:
        return jsonify({'message': 'Task not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)