import json
from flask import Flask, request
import redis

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/task', methods=['POST'])
def create_task():
    data = request.get_json()

    # Get the list of existing result keys
    existing_results = r.keys('result:*')

    if not existing_results:
        # If no existing results, reset the task_counter to 0
        r.delete('task_counter')
        task_id = 1
    else:
        # If there are existing results, find the biggest task_id
        task_ids = [int(key.decode().split(':')[1]) for key in existing_results]
        biggest_task_id = max(task_ids)

        # Set the task_counter to the biggest task_id + 1
        task_id = biggest_task_id + 1
        r.set('task_counter', task_id)

    # Add the task to the tasks queue with the unique task ID
    r.rpush('tasks', f"{task_id}:{json.dumps(data)}")

    return {'task_id': task_id}, 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')