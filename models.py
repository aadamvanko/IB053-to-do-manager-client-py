from dataclasses import dataclass
import typing

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