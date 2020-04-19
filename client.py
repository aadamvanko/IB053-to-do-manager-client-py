import jsons
import requests
import typing

from models import *
from task_service import TaskService


@dataclass
class Credentials:
    username: str
    password: str


class Client:
    def __init__(self):
        self.taskService = TaskService()
        self.credentials = Credentials("joe", "pass")
        self.loggedIn = False
        self.options = { 
            "login": self._login, 
            "getTasks": self._printTasks, 
            "addTask": self._addTask,
            "changeTask":self._changeTask,
            "deleteTask": self._deleteTask, 
            "getTotalTime": self._getTotalTime,
            "exit": None
        }

    def _login(self):
        loggedIn = False
        while not loggedIn:
            self.credentials.username = input("Enter username:")
            self.credentials.password = input("Enter password:")
            loggedIn = self.taskService.login(self.credentials)
        print("Logged in as", self.credentials.username)

    def _getTasksList(self):
       return self.taskService.getTasks(self.credentials)

    def _printTasks(self):
        for task in self._getTasksList():
            print(task)

    def _getPrerequisitesList(self):
        print("Enter tasks ids one by one, -1 for end: ")
        id = 0
        ids = []
        while True:
            id = int(input("Enter id: "))
            if id == -1:
                break
            ids.append(id)
        existingTasks = self._getTasksList()
        tasks = map(lambda id: list(filter(lambda task: task.id == id, existingTasks))[0], ids)
        return list(tasks)

    def _addTask(self):
        estimatedFinishTime = int(input('Enter estimated finish time in minutes: '))
        orderIndex = int(input('Enter ordering index: '))
        prerequisites = self._getPrerequisitesList()
        newTaskDTO = NewTaskDTO(estimatedFinishTime, orderIndex, prerequisites)
        addedTask = self.taskService.addTask(self.credentials, newTaskDTO)
        print(f"Task added, id={addedTask.id}")

    def _changeTask(self):
        id = int(input("Enter id of the task you want to edit: "))
        existingTasks = self._getTasksList()
        task = list(filter(lambda task: task.id == id, existingTasks))[0]
        task.estimatedFinishTime = int(input('Enter estimated finish time in minutes: '))
        task.orderIndex = int(input('Enter ordering index: '))
        task.prerequisites = self._getPrerequisitesList()
        changed = self.taskService.changeTask(self.credentials, task)
        print(f"Task with id={id} was {'' if changed else 'NOT'} changed.")

    def _deleteTask(self):
        id = input("Enter id of the task to delete: ")
        deleted = self.taskService.deleteTask(self.credentials, id)
        print(f"Task with id={id} was{'' if deleted else ' NOT' } deleted")

    def _getTotalTime(self):
        print(f"Total time is {self.taskService.getTotalTime(self.credentials)}")

    def _printMenu(self):
        print(f"Options: {', '.join(self.options.keys())}")

    def _getOption(self):
        option = ""
        while option not in self.options:
            option = input("Enter option:")
        return option

    def _executeOption(self, option):
        try:
            self.options[option]()
        except requests.ConnectionError:
            print("Please check your internet connection and try again")

    def run(self):
        print("Use username joe and password pass")
        self._login()
        while True:
            self._printMenu()
            option = self._getOption()
            if option == "exit":
                break
            self._executeOption(option)
        
if __name__ == "__main__":
    Client().run()