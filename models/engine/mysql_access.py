#!/usr/bin/python3
"""database storage"""


from importlib import import_module

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.exc import NoResultFound

from models.persons.person import Base
# from models.persons.admin import Admin
# from models.persons.lecturers import Lecturer
# from models.persons.students import Student
# from models.assets.attendance import Attendance
# from models.assets.scores import Score
# from models.assets.courses import Course
# from models.persons.auth import Auth


class MySQLStorage:
    """This describe the storage for the record"""
    __engine = None
    __session = None

    classes = {
                "Persons": import_module("models.persons.person").Persons,
                "Admin": import_module("models.persons.admin").Admin,
                "Lecturer": import_module("models.persons.lecturers").Lecturer,
                "Student": import_module("models.persons.students").Student,
                "Attendance": import_module("models.assets.attendance").Attendance,
                "Score": import_module("models.assets.scores").Score,
                "Course": import_module("models.assets.courses").Course,
                "Auth": import_module("models.persons.auth").Auth
        }

    def __init__(self):
        """conneect and createst the sql storage"""
        usr = "admin"
        pwd = "mesacot"
        db = "Student_Record"
        host = "localhost"
        url = f"{usr}:{pwd}@{host}/{db}"
        self.__engine = create_engine("mysql+mysqlconnector://{}".format(url),
                                      pool_size=10, pool_pre_ping=True)


    def new(self, obj):
        """add the object to the current database session (self.__session)"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the database session (self.__session)"""
        self.__session.commit()
        # self.__session.close()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)
            self.__session.commit()
            self.__session.flush()

    def reload(self):
        """creates and reloads content"""
        connection = self.__engine.connect()
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=connection, expire_on_commit=False)
        self.__session = scoped_session(session)

    def all(self, obj=None):
        """returns all objects or all specifics"""
        classes = self.classes
        obj_dicts = {}
        for string, clss in classes.items():
            if obj is None or obj == string or isinstance(obj, clss):
                clss = self.__session.query(clss).all()
            else:
                continue
            for objects in clss:
                try:
                    key = objects.__class__.__name__ + "." + objects.id
                except AttributeError:
                    key = objects.__class__.__name__ + "." + objects.email
                obj_dicts.update({key: objects})
        return obj_dicts

    def close(self):
        """closes session"""
        self.__session.remove()

    def find(self, obj, **kwargs):
        """returns a list of abj according to kwargs"""
        classes = self.classes
        if obj in classes:
            obj = classes.get(obj)
        if obj in classes.values():
            try:
                res = self.__session.query(obj).filter_by(**kwargs).order_by(desc(obj.created_at))
            except NoResultFound:
                return []
            return res.all()
        return []
