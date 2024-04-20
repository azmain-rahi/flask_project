import json
import redis
import os
from multiprocessing import Process
from time import sleep

r = redis.Redis(host='localhost', port=6379, db=0)

def process_task():
    while True:
        task_json = r.lpop('tasks')
        if task_json:
            task_id, task_data = task_json.decode().split(':', 1)
            task = json.loads(task_data)
            result = do_some_processing(task)
            r.set(f'result:{task_id}', json.dumps(result))
            print(f'Task {task_id} processed.')
        else:
            sleep(1)

def do_some_processing(task):
    # Add your custom processing logic here
    result = task['input'] * 2
    return {'result': result}

if __name__ == '__main__':
    num_workers = os.cpu_count()
    processes = [Process(target=process_task) for _ in range(num_workers)]

    for process in processes:
        process.start()

    for process in processes:
        process.join()