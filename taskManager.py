import sys
import json
from datetime import datetime

def run_task_manager(command):
    instruction = command[0]
    command = command[1:]
    result = False

    if len(command) >= 1 :

        if instruction == "add" :
            result = add(command)
        elif instruction == "update" :
            result = update(command)
        elif instruction == "delete" :
            result = delete(command)
        else :
            print("Command Unknow")

    else :
        print("Missing Information")


    if result :
        return "Success"
    else :
        return "Error"


def add(command):
    make_task(command[0], get_time())
    return True

def update(command):
    if len(command) < 2 :
        print("Missing Information")
        return False
    else :
        return action_on_tasks("update", command)

def delete(command):
    if len(command) < 1:
        print("Missing Information")
        return False
    else:
        return action_on_tasks("delete", command)

def get_time():
    time = datetime.now()
    return time.strftime("%d-%m-%y %H:%M:%S")

def make_task(description, createdAT):
    identifier = 0
    tasks = {}

    try:
        with open('Task_Manger.json', 'r') as fp:
            tasks = json.load(fp)
            identifier = len(tasks)

    except IOError:
        print("Creating Json File")

    taskDict = {
        identifier : {
            "description": description,
            "status": "todo",
            "createdAT": createdAT,
            "updatedAT": createdAT
        }
    }

    tasks.update(taskDict)
    json_obj = json.dumps(tasks, indent=5)

    with open('Task_Manger.json', 'w') as fp:
        fp.write(json_obj)

def action_on_tasks(action, information):
    identifier = information[0]
    try:
        with open('Task_Manger.json', 'r') as fp:
            tasks = json.load(fp)
            if identifier in tasks.keys():
                if action == "update" :
                    tasks[identifier]["description"] = information[1]
                    tasks[identifier]["updatedAT"] = get_time()
                elif action == "delete":
                    tasks.pop(identifier)
            else :
                print("Task not found")
                return False

        json_obj = json.dumps(tasks, indent=5)

        with open('Task_Manger.json', 'w') as fp:
            fp.write(json_obj)
        return True

    except IOError:
        print("No Tasks registered")
        return False


if __name__ == '__main__':
    print(run_task_manager(sys.argv[1:]))
