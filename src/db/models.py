from datetime import date
from re import S
from typing import Text
from sqlalchemy import Boolean, Column, LargeBinary, String, DateTime, Integer, JSON, ForeignKey, Table, BigInteger, column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

Base = declarative_base()


class Users(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)

    name = Column(String)
    surname = Column(String)
    email = Column(String, unique = True, index = True )
    password = Column(String)
    organization =Column(String)
    qualification = Column(String)
    theme = Column(String)
    about = Column(String)
    avatar = Column(String, default='avatars/logo.png')
    
    
    sections = relationship('Section', back_populates='user')
    
def __init__(
            self, name="", surname="", email="", password="", organization="", qualification="", theme="", about="", avatar=""
    ):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        self.organization = organization
        self.qualification = qualification
        self.theme = theme
        self.about = about
        self.avatar = avatar
        self.sections = []
        
def __repr__(self):
    return f'name: {self.name}, surname: {self.surname}, email: {self.email}, ' \
        f'password: {self.password}, organization: {self.organization}, qualification: {self.qualification}, ' \
        f'theme: {self.theme}, about: {self.about}, avatar: {self.avatar} ' 


class Section(Base):
    __tablename__ ='sections'
    id = Column(Integer, primary_key=True)
    name_of_section = Column(String)
    user_id = Column(Integer, ForeignKey('Users.id'))

    # section = relationship('Tables', back_populates='table')
    user = relationship('Users', back_populates='sections')
    tasks = relationship('Tasks', back_populates='section')

    def __init__(self, name_of_section="", user=None):  # Изменено: добавлен аргумент user
        self.name_of_section = name_of_section
        self.user = user  # Изменено: устанавливаем атрибут user

    def __repr__(self):
        return f'name_of_section: {self.name_of_section}, user_id: {self.user_id}'


class Tasks(Base):
    __tablename__ ='tasks'
    id = Column(Integer, primary_key=True)
    task_description = Column(String)
    checked = Column(Boolean)
    section_id = Column(Integer, ForeignKey('sections.id'))

    section = relationship('Section', back_populates='tasks')

    def __init__(self, task_description=None, checked=False, section=None):
        self.task_description = task_description
        self.checked = checked
        self.section = section

    def __repr__(self):
        return f'task_description: {self.task_description}, checked: {self.checked}, section_id: {self.section_id}'
    
class Teams(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name_of_team = Column(String)
    id_users_of_teams = Column(Integer, ForeignKey('Users.id'))


    
    """ sections = relationship('Section', back_populates='user') """
    
    def __init__(self, name_of_team="", id_users_of_teams=""):
        self.name_of_team = name_of_team
        self.id_users_of_teams = id_users_of_teams

    def __repr__(self):
        return f'name_of_team: {self.name_of_team}, id_users_of_teams: {self.id_users_of_teams}'
        
class Projects(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name_of_project = Column(String)
    date_of_start = Column(DateTime, default=func.now())
    status = Column(String)
    user_id = Column(Integer, ForeignKey('Users.id'))



    """ table = relationship('Section', back_populates='section') """

    def __init__(self, name_of_project="", date_of_start="", status="", user_id=""):
        self.name_of_project = name_of_project
        self.date_of_start = date_of_start
        self.status = status
        self.user_id = user_id

        
    def __repr__(self):
        return f'name_of_project: {self.name_of_project}, date_of_start: {self.date_of_start}, status: {self.status}, user_id: {self.user_id}'
    
    
class TeamLeads(Base):
    __tablename__ = 'team_leads'
    id = Column(Integer, primary_key=True)
    team_lead_id = Column(Integer, ForeignKey('Users.id'))
    teams_id = Column(Integer, ForeignKey('teams.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    task_from_team_lead = Column(Integer, ForeignKey('tasks.id'))
    
    """ sections = relationship('Section', back_populates='user') """
    
    def __init__(self, team_lead_id="", teams_id="", project_id="", task_from_team_lead=""):
        self.team_lead_id = team_lead_id
        self.teams_id = teams_id
        self.project_id = project_id
        self.task_from_team_lead = task_from_team_lead
    
    def __repr__(self):
        return f'team_lead_id: {self.team_lead_id}, teams_id: {self.teams_id}, project_id: {self.project_id}, task_from_team_lead: {self.task_from_team_lead}'
    

    

class Comments(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    text_of_comment = Column(String)
    date_of_comment = Column(DateTime, default=func.now())
    user_id_comment = Column(Integer, ForeignKey('Users.id'))
    task_id_comment = Column(Integer, ForeignKey('tasks.id'))
    
    def __init__(self, text_of_comment="", date_of_comment="", user_id_comment="", task_id_comment=""):
        self.text_of_comment = text_of_comment
        self.date_of_comment = date_of_comment
        self.user_id_comment = user_id_comment
        self.task_id_comment = task_id_comment
        
    def __repr__(self):
        return f'text_of_comment: {self.text_of_comment}, date_of_comment: {self.date_of_comment}, user_id_comment: {self.user_id_comment}, task_id_comment: {self.task_id_comment}'
    
    
class Attachments(Base):
    __tablename__ = 'attachments'
    id = Column(Integer, primary_key=True)
    type = Column(String)
    value = Column(String)
    id_of_attachment_user = Column(Integer, ForeignKey('Users.id'))
    task_attachment_id = Column(Integer, ForeignKey('tasks.id'))
    
    def __init__(self, type="", value="", id_of_attachment_user="", task_attachment_id=""):
        self.type = type
        self.value = value
        self.id_of_attachment_user = id_of_attachment_user
        self.task_attachment_id = task_attachment_id
    
    
    def __repr__(self):
        return f'type: {self.type}, value: {self.value}, id_of_attachment_user: {self.id_of_attachment_user}, task_attachment_id: {self.task_attachment_id}'
    
class Chats(Base):
    __tablename__ = 'chats'
    id = Column(Integer, primary_key=True)
    name_of_chat = Column(String)
    id_of_chat_user = Column(Integer, ForeignKey('Users.id'))
    id_of_chat_team = Column(Integer, ForeignKey('teams.id'))
    
    def __init__(self, name_of_chat="", id_of_chat_user="", id_of_chat_team=""):
        self.name_of_chat = name_of_chat
        self.id_of_chat_user = id_of_chat_user
        self.id_of_chat_team = id_of_chat_team
        
    def __repr__(self):
        return f'name_of_chat: {self.name_of_chat}, id_of_chat_user: {self.id_of_chat_user}, id_of_chat_team: {self.id_of_chat_team}'
    

class Messages(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    text_of_message = Column(String)
    date_of_message = Column(DateTime, default=func.now())
    id_of_message_user = Column(Integer, ForeignKey('Users.id'))
    id_of_message_chat = Column(Integer, ForeignKey('chats.id'))
    
    def __init__(self, text_of_message="", date_of_message="", id_of_message_user="", id_of_message_chat=""):
        self.text_of_message = text_of_message
        self.date_of_message = date_of_message
        self.id_of_message_user = id_of_message_user
        self.id_of_message_chat = id_of_message_chat
        
    def __repr__(self):
        return f'text_of_message: {self.text_of_message}, date_of_message: {self.date_of_message}, id_of_message_user: {self.id_of_message_user}, id_of_message_chat: {self.id_of_message_chat}'