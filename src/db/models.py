from datetime import date
from email import message
from re import S
from sqlite3 import Date
from typing import Text
from sqlalchemy import (
    Boolean,
    Column,
    String,
    DateTime,
    Integer,
    ForeignKey,
    Table,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

Base = declarative_base()

#!----------------------------------------------------------------------------------------------------------------------------

class Roles(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    
    role = Column(String)

    users = relationship("Users", back_populates="role")
    
    def __init__(self, role=""):
        self.role = role

    def __repr__(self):
        return f"role: {self.role}"

#!----------------------------------------------------------------------------------------------------------------------------

class Organization(Base):
    __tablename__ = "organization"
    id = Column(Integer, primary_key=True)
    
    name = Column(String)

    users = relationship("Users", back_populates="organization")
    
    def __init__(self, name=""):
        self.name = name

    def __repr__(self):
        return f"name: {self.name}"
    
#!----------------------------------------------------------------------------------------------------------------------------

class Priority(Base):
    __tablename__ = "priority"
    id = Column(Integer, primary_key=True)
    
    priority_value = Column(String) 
    
    tasks = relationship("Tasks", back_populates="priority", primaryjoin="Priority.id == Tasks.priority_id")
    
    def __init__(self, priority_value=""):
        self.priority_value = priority_value

    def __repr__(self):
        return f"priority_value: {self.priority_value}"

#!----------------------------------------------------------------------------------------------------------------------------

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)

    name = Column(String)
    surname = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    theme = Column(String)
    about = Column(String)
    avatar = Column(String, default="avatars/logo.png")
    dateReg = Column(DateTime, default=func.now())
    role_Id = Column(Integer, ForeignKey("roles.id"))
    organization_Id = Column(Integer, ForeignKey("organization.id"))

    tasks = relationship("Tasks", back_populates="task_creator")
    organization = relationship("Organization", back_populates="users")
    role = relationship("Roles", back_populates="users")
    projects = relationship("Projects", back_populates="user_project")
    sections = relationship("Section", back_populates="user")
    comments = relationship("Comments", back_populates="userCommment")
    attachments = relationship("Attachments", back_populates="attachmentUser")
    created_chats = relationship("Chats", back_populates="chat_creators")
    chat_users = relationship("Chats", secondary="chat_users", back_populates="chat_users")
    message = relationship("Messages", back_populates="userMessage")

def __init__(
    self,
    name="",
    surname="",
    email="",
    password="",
    theme="",
    about="",
    avatar="",
    dateReg="",
):
    self.name = name
    self.surname = surname
    self.email = email
    self.password = password
    self.theme = theme
    self.about = about
    self.avatar = avatar
    self.dateReg = dateReg
    self.sections = []


def __repr__(self):
    return (
        f"name: {self.name}, surname: {self.surname}, email: {self.email},password: {self.password}"
        f"theme: {self.theme}, about: {self.about}, avatar: {self.avatar}, dateReg: {self.dateReg}"
    )


#!----------------------------------------------------------------------------------------------------------------------------


class Projects(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    
    name_of_project = Column(String)
    date_of_start = Column(DateTime, default=func.now())
    status = Column(String)
    project_creator = Column(Integer, ForeignKey("users.id"))

    user_project = relationship("Users", back_populates="projects")
    project = relationship("Section", back_populates="section")

    def __init__(self, name_of_project="", date_of_start="", status="", project_creator=""):
        self.name_of_project = name_of_project
        self.date_of_start = date_of_start
        self.status = status
        self.project_creator = project_creator

    def __repr__(self):
        return f"name_of_project: {self.name_of_project}, date_of_start: {self.date_of_start}, status: {self.status}, project_creator: {self.project_creator}"

#!----------------------------------------------------------------------------------------------------------------------------

project_users = Table(
    "project_users",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("project_id", Integer, ForeignKey("projects.id")),
)

#!----------------------------------------------------------------------------------------------------------------------------

class Section(Base):
    __tablename__ = "sections"
    id = Column(Integer, primary_key=True)
    
    name_of_section = Column(String)
    creator = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))

    section = relationship("Projects", back_populates="project")
    user = relationship("Users", back_populates="sections")
    tasks = relationship("Tasks", back_populates="section")

    def __init__(self, name_of_section="", user=None):
        self.name_of_section = name_of_section
        self.user = user

    def __repr__(self):
        return f"name_of_section: {self.name_of_section}, user_id: {self.user_id}"


#!----------------------------------------------------------------------------------------------------------------------------


class Tasks(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    
    task_description = Column(String)
    checked = Column(Boolean)
    DateStart = Column(DateTime, default=func.now())
    DateEnd = Column(DateTime)
    section_id = Column(Integer, ForeignKey("sections.id"))
    creator = Column(Integer, ForeignKey("users.id"))
    priority_id = Column(Integer, ForeignKey("priority.id"))

    priority = relationship("Priority", back_populates="tasks")
    task_creator = relationship("Users", back_populates="tasks")
    section = relationship("Section", back_populates="tasks")
    comments = relationship("Comments", back_populates="comment")
    attachments = relationship("Attachments", back_populates="attachment")

    def __init__(
        self,
        task_description=None,
        checked=False,
        DateStart=func.now(),
        DateEnd=None,
        section = None

    ):
        self.task_description = task_description
        self.checked = checked
        self.DateStart = DateStart
        self.DateEnd = DateEnd
        self.section = section

    def __repr__(self):
        return f"task_description: {self.task_description}, checked: {self.checked}, section_id: {self.section_id}, DateStart: {self.DateStart}, DateEnd: {self.DateEnd}, section_id: {self.section_id}, creator: {self.creator}, priority_id: {self.priority_id}"

#!----------------------------------------------------------------------------------------------------------------------------

task_users = Table(
    "task_users",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("task_id", Integer, ForeignKey("tasks.id")),
)

#!----------------------------------------------------------------------------------------------------------------------------

class Comments(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    
    text_of_comment = Column(String)
    date_of_comment = Column(DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"))

    comment = relationship("Tasks", back_populates="comments")
    userCommment = relationship("Users", back_populates="comments")

    def __init__(
        self,
        text_of_comment="",
        date_of_comment="",
    ):
        self.text_of_comment = text_of_comment
        self.date_of_comment = date_of_comment

    def __repr__(self):
        return f"text_of_comment: {self.text_of_comment}, date_of_comment: {self.date_of_comment}"

#!----------------------------------------------------------------------------------------------------------------------------

class Attachments(Base):
    __tablename__ = "attachments"
    id = Column(Integer, primary_key=True)
    file_path = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"))

    attachment = relationship("Tasks", back_populates="attachments")
    attachmentUser = relationship("Users", back_populates="attachments")

    def __init__(
        self, file_path=""
    ):
        self.file_path = file_path

    def __repr__(self):
        return f"file_path: {self.file_path}"

#!----------------------------------------------------------------------------------------------------------------------------

class Chats(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True)
    
    name_of_chat = Column(String)
    chat_creator = Column(Integer, ForeignKey("users.id"))

    chat_creators = relationship("Users", back_populates="created_chats")
    chat_users = relationship("Users", secondary="chat_users", back_populates="chat_users")
    messages = relationship("Messages", back_populates="chatMessage")

    def __init__(self, name_of_chat="", chat_creator=""):
        self.name_of_chat = name_of_chat
        self.chat_creator = chat_creator

    def __repr__(self):
        return f"name_of_chat: {self.name_of_chat}, chat_creator: {self.chat_creator}"

#!----------------------------------------------------------------------------------------------------------------------------

class Messages(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    
    text_of_message = Column(String)
    date_of_message = Column(DateTime, default=func.now())
    message_user = Column(Integer, ForeignKey("users.id"))
    chat_id = Column(Integer, ForeignKey("chats.id"))

    userMessage = relationship("Users", back_populates="message")
    chatMessage = relationship("Chats", back_populates="messages")

    def __init__(
        self,
        text_of_message="",
        date_of_message="",
        message_user="",
        chat_id="",
    ):
        self.text_of_message = text_of_message
        self.date_of_message = date_of_message
        self.message_user = message_user
        self.chat_id = chat_id

    def __repr__(self):
        return f"text_of_message: {self.text_of_message}, date_of_message: {self.date_of_message}, message_user: {self.message_user}, chat_id: {self.chat_id}"

#!----------------------------------------------------------------------------------------------------------------------------

chat_users = Table(
    "chat_users",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("chat_id", Integer, ForeignKey("chats.id")),
)

#!----------------------------------------------------------------------------------------------------------------------------






