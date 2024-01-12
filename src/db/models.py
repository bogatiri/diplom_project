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
    
    
    
    
""" class Tables(Base):
    __tablename__ = 'tables'
    id = Column(Integer, primary_key=True)
    name_of_table = Column(String)
    id_table = Column(Integer, ForeignKey('Users.id'))


    table = relationship('Section', back_populates='section')

    def __init__(self, name_of_table="", id_table=""):
        self.name_of_table = name_of_table
        self.id_table = id_table

    def __repr__(self):
        return f'name_of_table: {self.name_of_table}, id_table: {self.id_table}' """
