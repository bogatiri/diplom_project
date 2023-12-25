from typing import Text
from sqlalchemy import Column, LargeBinary, String, DateTime, Integer, JSON, ForeignKey, Table, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Users(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)

    name = Column(String)
    surname = Column(String)
    email = Column(String)
    password = Column(String)
    organization =Column(String)
    qualification = Column(String)
    theme = Column(String)
    about = Column(String)
    avatar = Column(String, default='avatars/logo.png')
    
    
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
        
def __repr__(self):
    return f'name: {self.name}, surname: {self.surname}, email: {self.email}, ' \
        f'password: {self.password}, organization: {self.organization}, qualification: {self.qualification}, ' \
        f'theme: {self.theme}, about: {self.about}, avatar: {self.avatar} ' 
