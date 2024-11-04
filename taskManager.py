import sys
import json
from datetime import datetime

def run_task_manager(command):
    instruction = command[0]
    command = command[1:]
    result = False

    match instruction:
        case "add" :
            result = add(command)
        case "update" :
            result = update(command)
        case "delete" :
            result = delete(command)
        case "mark-in-progress":
            result = status_update(command, "in-progress")
        case "mark-done":
            result = status_update(command, "done")
        case "list":
            result = list_tasks(command)
        case _ :
            print("Command Unknow")


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

def status_update(command, newStatus):
    if len(command) < 1:
        print("Missing Information")
        return False
    else:
        command.append(newStatus)
        return action_on_tasks("status update", command)

def list_tasks(command):
    try:
        with open('Task_Manger.json', 'r') as fp:
            tasks = json.load(fp)
            if len(command) == 0:
                pretty_print_task(tasks, None)
            else:
                if command[0] in ["done", "todo", "in-progress"]:
                    pretty_print_task(tasks, command[0])
                else :
                    print("Unknown argument")
                    return False

        return True

    except IOError:
        print("No Tasks registered")
        return False

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
                match action:
                    case "update" :
                        tasks[identifier]["description"] = information[1]
                        tasks[identifier]["updatedAT"] = get_time()
                    case "delete":
                        tasks.pop(identifier)
                    case "status update":
                        tasks[identifier]["status"] = information[1]
                    case _:
                        print("Action not recognised")
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

def pretty_print_task(tasks, status):
    for key in tasks.keys():
        if status == tasks[key]["status"] or status is None :
            print("\nID : ", key,
                  "\nDescription : ", tasks[key]["description"],
                  "\nStatus : ", tasks[key]["status"],
                  "\nCreated at : ", tasks[key]["createdAT"],
                  "\nUpdated at : ", tasks[key]["updatedAT"],
                  "\n")


if __name__ == '__main__':
    print(run_task_manager(sys.argv[1:]))
