from __init__ import db
from datetime import datetime
from sqlalchemy import inspect
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

# class Activity(db.Model):
#     __tablename__ = 'activity'
#     id=db.Column(db.String(50),nullable=False,primary_key=True,unique=True)
#     custId=db.Column(db.String(50),nullable=False)
#     details=db.Column(db.String(150),nullable=True)
#     type=db.Column(db.String(20),nullable=True)
#     date=db.Column(db.DateTime, default=datetime.now(),nullable=True)
#     def toDict(self):
#         return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }




class Users(db.Model):
    __tablename__ = 'users'
    userId=db.Column(db.String(50),primary_key=True,nullable=False,unique=True)
    name=db.Column(db.String(30),nullable=False)
    mobile=db.Column(db.String(15),nullable=False)
    email=db.Column(db.String(75),nullable=True,unique=True)
    password=db.Column(db.String(100),nullable=False)
    address1=db.Column(db.String(200),nullable=True)
    address2=db.Column(db.String(200),nullable=True)
    city=db.Column(db.String(50),nullable=True)
    state=db.Column(db.String(75),nullable=True)
    zip=db.Column(db.Integer,nullable=True)
    status=db.Column(db.Boolean, default=True,nullable=False)
    date=db.Column(db.DateTime, default=datetime.now(),nullable=True)
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

class Schedules(db.Model):
    __tablename__ = 'schedules'
    scheduleId=db.Column(db.String(50),nullable=False,primary_key=True,unique=True)
    userId=db.Column(db.String(50),ForeignKey('users.userId'),nullable=False)
    deviceId=db.Column(db.String(50),nullable=True)
    name=db.Column(db.String(50),nullable=True)
    startTime=db.Column(db.DateTime,nullable=False)
    duration=db.Column(db.Integer,nullable=False)
    status=db.Column(db.Boolean, default=True,nullable=False)
    date=db.Column(db.DateTime, default=datetime.now(),nullable=True)
    user = relationship('Users', backref='schedules')
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
    

class Devices(db.Model):
    __tablename__ = 'devices'
    deviceId=db.Column(db.String(50),primary_key=True,nullable=False,unique=True)
    userId=db.Column(db.String(50),ForeignKey('users.userId'),nullable=False)
    name=db.Column(db.String(50),nullable=False)
    description=db.Column(db.String(200),nullable=True)
    password=db.Column(db.String(50),nullable=False)
    extra=db.Column(db.String(100),nullable=True)
    status=db.Column(db.Boolean,default=True,nullable=False)
    date=db.Column(db.DateTime, default=datetime.now(),nullable=True)
    user = relationship('Users', backref='devices')
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
    


# class Monitor(db.Model):
#     __tablename__ = 'monitor'
#     id=db.Column(db.String(50),primary_key=True,nullable=False,unique=True)
#     custId=db.Column(db.String(50),nullable=False,unique=True)
#     deviceId=db.Column(db.String(50),nullable=False,unique=True)
#     phase1=db.Column(db.Boolean, default=False,nullable=False)
#     phase2=db.Column(db.Boolean, default=False,nullable=False)
#     phase3=db.Column(db.Boolean, default=False,nullable=False)
#     isMotorOn=db.Column(db.Boolean, default=False,nullable=False)
#     waterLevel=db.Column(db.Integer,nullable=False) 
#     isActive_iot=db.Column(db.Boolean, default=False,nullable=False)
#     isActive_remote=db.Column(db.Boolean, default=False,nullable=False)
#     msg=db.Column(db.String(200),nullable=False)
#     uptime=db.Column(db.DateTime,default=datetime.now(),nullable=True)
#     date=db.Column(db.DateTime,default=datetime.now(),nullable=True)
#     def toDict(self):
#         return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
    


# class Admin(db.Model):
#     __tablename__ = 'admin'
#     id=db.Column(db.String(50),primary_key=True,nullable=False,unique=True)
#     name=db.Column(db.String(50),nullable=False)
#     username=db.Column(db.String(50),nullable=False)
#     mobile=db.Column(db.String(15),nullable=False,unique=True)
#     email=db.Column(db.String(75),nullable=False)
#     password=db.Column(db.String(50),nullable=False)
#     secretkey=db.Column(db.String(100),nullable=False)
#     date=db.Column(db.DateTime, default=datetime.now(),nullable=True)
#     def toDict(self):
#         return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
    
    