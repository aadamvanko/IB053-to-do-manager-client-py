import jsons
import requests
from models import *

class TaskService:
    api_url = "http://localhost:8080"

    def _makeRequest(self, method, url, data="", headers={}):
        methods = { 'get': requests.get, 'post': requests.post, 'put': requests.put, 'delete': requests.delete }
        method = methods[method]
        response = method(url, data=data, headers=headers)
        return response

    def _makeAuthenticatedRequest(self, credentials, method, url, data="", headers={}):
        return self._makeRequest(method, url, data, headers={ **{ "username": credentials.username, "password": credentials.password }, **headers })

    def login(self, credentials):
        response = self._makeAuthenticatedRequest(credentials, "post", f"{self.api_url}/login")
        if not response:
            return False
        loginResponseDTO = jsons.loadb(response.content, cls=LoginResponseDTO)
        return loginResponseDTO.loggedIn

    def getTasks(self, credentials):
        response = self._makeAuthenticatedRequest(credentials, 'get', f"{self.api_url}/tasks")
        tasks = jsons.loadb(response.content, typing.List[Task])
        return tasks

    def addTask(self, credentials, newTaskDTO):
        response = self._makeAuthenticatedRequest(credentials, 'post', f"{self.api_url}/tasks", jsons.dumps(newTaskDTO), {"content-type": "application/json"})
        return jsons.loadb(response.content, cls=Task)

    def changeTask(self, credentials, changedTask):
        response = self._makeAuthenticatedRequest(credentials, "put", f"{self.api_url}/tasks/{changedTask.id}", jsons.dumps(changedTask), {"content-type": "application/json"})
        return bool(response)

    def deleteTask(self, credentials, id):
        response = self._makeAuthenticatedRequest(credentials, "delete", f"{self.api_url}/tasks/{id}")
        return bool(response)

    def getTotalTime(self, credentials):
        response = self._makeAuthenticatedRequest(credentials, "get", f"{self.api_url}/tasks/total_time")
        totalTime = jsons.loadb(response.content, int)
        return totalTime
