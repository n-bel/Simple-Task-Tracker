import sys
import json
from datetime import datetime


"""
Function that runs when asking the task 
manager to make any action.
"""
def run_task_manager(command):
    instruction = command[0]
    command = command[1:]
    result = False

    #redirecting any instruction to the right
    #function
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
            print("Command Unknown")# When we do not recognise the command we print this

    #Tellsthe user if the command was successfully
    #executed or if we ran into an issue
    if result :
        return "Success"
    else :
        return "Error"

"""
Function that adds an task.
"""
def add(command):
    make_task(command[0], get_time())
    return True

"""
Function that updates a task.
"""
def update(command):
    if len(command) < 2 : # Check if the number of arguments is sufficient
        print("Missing Information")
        return False
    else :
        return action_on_tasks("update", command)

"""
Function that deletes a task.
"""
def delete(command):
    if len(command) < 1: # Check if the number of arguments is sufficient
        print("Missing Information")
        return False
    else:
        return action_on_tasks("delete", command)


"""
Function that updates the status of a task.
"""
def status_update(command, newStatus):
    if len(command) < 1: # Check if the number of arguments is sufficient
        print("Missing Information")
        return False
    else:
        command.append(newStatus) # Adding the new status to the command
        return action_on_tasks("status update", command)

"""
Function that lists the tasks.
"""
def list_tasks(command):
    try: # check if there is a Json file
        with open('Task_Manger.json', 'r') as fp:
            tasks = json.load(fp)
            if len(command) == 0: # Check if the number of arguments is sufficient
                pretty_print_task(tasks, None)
            else:
                if command[0] in ["done", "todo", "in-progress"]: # check if the status change is correct
                    pretty_print_task(tasks, command[0])
                else :
                    print("Unknown argument") # let the user know with this msg that the new status is not supported
                    return False

        return True

    except IOError: # if there is no json file catch the error
        print("No Tasks registered") # print this error msg to let the user know
        return False

"""
Function that gives the time
and the date.
"""
def get_time():
    time = datetime.now()
    return time.strftime("%d-%m-%y %H:%M:%S")

"""
Function that creates a task.
"""
def make_task(description, createdAT):
    identifier = 0 # default id is 0
    tasks = {}

    try: # Check if a json file already exists
        with open('Task_Manger.json', 'r') as fp:
            tasks = json.load(fp) # recuperate the tasks
            identifier = int(list(tasks.keys())[-1])+1 # get the last value for the id and increment it to get a new unique id

    except IOError: # if there is no json file let the user know that we are creating one
        print("Creating Json File")

    # create a dict with the right keys to make the task
    taskDict = {
        identifier : {
            "description": description,
            "status": "todo",
            "createdAT": createdAT,
            "updatedAT": createdAT
        }
    }

    tasks.update(taskDict) # Update the json with the new task
    json_obj = json.dumps(tasks, indent=5)

    with open('Task_Manger.json', 'w') as fp:
        fp.write(json_obj) # write the updated tasks set on the jason

"""
Function that applies a transformation
on an existing task.
"""
def action_on_tasks(action, information):
    identifier = information[0] # get the identifier of the task to be modified
    try: # Check if a json file already exists
        with open('Task_Manger.json', 'r') as fp:
            tasks = json.load(fp) # recuperate the tasks
            if identifier in tasks.keys(): # check if the task is in the json
                match action:
                    case "update" :
                        tasks[identifier]["description"] = information[1]
                        tasks[identifier]["updatedAT"] = get_time()
                    case "delete":
                        tasks.pop(identifier)
                    case "status update":
                        tasks[identifier]["status"] = information[1]
                        tasks[identifier]["updatedAT"] = get_time()
                    case _:
                        print("Action not recognised")
            else : # handle in the case of the task not being in the json
                print("Task not found")
                return False

        json_obj = json.dumps(tasks, indent=5)

        with open('Task_Manger.json', 'w') as fp:
            fp.write(json_obj)
        return True

    except IOError: # case where there is no json file
        print("No Tasks registered")
        return False

"""
Functions that formats and prints
all the tasks that fit the given
parameter.
"""
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
