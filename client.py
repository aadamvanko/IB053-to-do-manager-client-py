import jsons
import requests
import typing
from dataclasses import dataclass

api_url = "http://localhost:8080"

@dataclass
class LoginResponseDTO:
    loggedIn: bool
    
@dataclass
class User:
    id: int
    name: str
    surname: str
    username: str

@dataclass
class Task:
    id: int
    estimatedFinishTime: int
    orderIndex: int
    owner: User
    prerequisites: typing.List['Task']

@dataclass
class NewTaskDTO:
    estimatedFinishTime: int
    orderIndex: int
    prerequisites: typing.List['Task']

@dataclass
class Credentials:
    username: str
    password: str

class Client:
    def __init__(self):
        self.credentials = Credentials("joe", "pass")
        self.loggedIn = False
        self.options = { 
            "login": self._login, 
            "getTasks": self._printTasks, 
            "addTask": self._addTask, "changeTask":self._changeTask, "deleteTask": self._deleteTask, 
            "getTotalTime": self._getTotalTime,
            "exit": None
        }

    def _makeRequest(self, method, url, data="", headers={}):
        methods = { 'get': requests.get, 'post': requests.post, 'put': requests.put, 'delete': requests.delete }
        method = methods[method]
        response = method(url, data=data, headers={ **{ "username":self.credentials.username, "password":self.credentials.password }, **headers })
        return response

    def _login(self):
        loginResponseDTO = LoginResponseDTO(False)
        while not loginResponseDTO.loggedIn:
            self.credentials.username = input("Enter username:")
            self.credentials.password = input("Enter password:")
            response = self._makeRequest("post", f"{api_url}/login")
            #print(response.content)
            loginResponseDTO = jsons.loadb(response.content, cls=LoginResponseDTO)
        print("Logged in as", self.credentials.username)

    def _getTasksList(self):
        response = self._makeRequest('get', f"{api_url}/tasks")
        tasks = jsons.loadb(response.content, typing.List[Task])
        return tasks

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
        estimatedFinishTime = input('Enter estimated finish time in minutes: ')
        orderIndex = input('Enter ordering index: ')
        prerequisites = self._getPrerequisitesList()
        newTaskDTO = NewTaskDTO(estimatedFinishTime, orderIndex, prerequisites)
        response = self._makeRequest('post', f"{api_url}/tasks", jsons.dumps(newTaskDTO), {"content-type": "application/json"})
        #print(response.content)

    def _changeTask(self):
        id = int(input("Enter id of the task you want to edit: "))
        existingTasks = self._getTasksList()
        task = list(filter(lambda task: task.id == id, existingTasks))[0]
        task.estimatedFinishTime = input('Enter estimated finish time in minutes: ')
        task.orderIndex = input('Enter ordering index: ')
        task.prerequisites = self._getPrerequisitesList()
        response = self._makeRequest("put", f"{api_url}/tasks/{id}", jsons.dumps(task), {"content-type": "application/json"})
        #print(response.content)

    def _deleteTask(self):
        task_id = input("Enter id of the task to delete: ")
        response = self._makeRequest("delete", f"{api_url}/tasks/{task_id}")
        print(f"Task with id={task_id} was {'successfully' if response.status_code == 200 else 'not' } deleted")

    def _getTotalTime(self):
        response = self._makeRequest("get", f"{api_url}/tasks/total_time")
        totalTime = jsons.loadb(response.content, int)
        print(f"Total time is {totalTime}")

    def _printMenu(self):
        print("Options:")
        for option in self.options:
            print(option)

    def _getOption(self):
        option = ""
        while option not in self.options:
            option = input("Enter option:")
        return option

    def run(self):
        """
        self._login()
        self._printTasks()
        self._getTotalTime()
        self._deleteTask()
        self._addTask()
        self._changeTask()
        self._printTasks()
        """
        
        self._login()
        while True:
            self._printMenu()
            option = self._getOption()
            if option == "exit":
                break
            self.options[option]()
        

Client().run()