#!/usr/bin/python3
"""
This module defines class for score
"""

from uuid import uuid4
import json
from datetime import datetime
from sqlalchemy import (Column, String, Text, CheckConstraint,
                        DateTime, ForeignKey, Integer)

from ..persons.person import Base


class Score(Base):
    """Score class"""
    __tablename__ = "score"
    id = Column(String(60), unique=True, primary_key=True, nullable=False)
    session = Column(String(10))
    semester = Column(Integer, CheckConstraint("semester <= 5"))
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())
    lecturer_id = Column(String(30), ForeignKey("lecturers.id"))
    student_id = Column(String(30), ForeignKey("students.id"))
    course_code = Column(String(10))
    level = Column(String(15), CheckConstraint("level IN ('Certificate', 'Diploma', 'Advanced')"))
    __unit = Column(Integer)
    __attendance = Column(Integer)
    __assignment = Column(Text) #json.dumps([{"mark obtained": 0, "mark obtainable": 10}])
    __test = Column(Text) #json.dumps([{"mark obtained": 0, "mark obtainable": 20}])
    __exam = Column(Text) #json.dumps({"mark obtained": 0, "mark obtainable": 60})
    __score = Column(String(60)) #json.dumps({"mark obtained": 0, "mark obtainable": 100})


    def __init__(self, **kwargs):
        """intitializes attendance"""
        if "id" not in kwargs:
            self.id = str(uuid4())
        else:
            self.id = kwargs.pop("id")
        if "created_at" not in kwargs:
            self.created_at = datetime.now()
        else:
            date = kwargs.pop("created_at")
            update = kwargs.pop("update_at")
            try:
                self.created_at = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
                self.updated_at = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
            except TypeError:
                self.created_at = date
                self.updated_at = update
        if "lecturer_id" not in kwargs or "student_id" not in kwargs\
            or "course_code" not in kwargs or "session" not in kwargs:
            raise AttributeError("Please ensure none of \
                                 session/course_code/lecturer_id/student_id \
                                 is not missing")
        for key, value in kwargs.items():
            setattr(self, key, value)
        from models import vault
        vault.new(self)

    def save_me(self):
        """adds update to database"""
        from models import vault
        self.updated_at = datetime.now()
        vault.save()

    def to_dict(self):
        """returns a dictionary representation of the class"""
        self_dict = {}
        self_dict.update(self.__dict__)
        self_dict.update({'__class__': self.__class__.__name__})
        self_dict['created_at'] = self.created_at.isoformat()
        self_dict['updated_at'] = self.created_at.isoformat()
        return self_dict

    def json_me(self):
        """returns a json representation of self"""
        return json.dumps(self.to_dict())

    def save(self):
        """fetches unit from course code and sets then saves"""

    def add_assignment(self, ass_no = "nill", mkobtnble = "nill",
                       mkobtnd = "nill"):
        """
        create assignment with markobtainable, default is 10
        add marks to assignment with assignment number, default is latest
        update mark obtainable, default updates latest
        update score with number, default updates latest
        """
        try:
            obj = json.loads(self.__assignment)
        except TypeError:
            obj = []
        except json.JSONDecodeError:
            obj = []
        if mkobtnd == "nill":
            if ass_no == "nill":
                if mkobtnble == "nill":
                    obj.append({"mark_obtained": 0, "mark_obtainable": 10})
                else:
                    obj.append({"mark_obtained": 0, "mark_obtainable": mkobtnble})
            else:
                try:
                    if mkobtnble == "nill":
                        if obj[ass_no - 1]["mark_obtained"] > 10:
                            raise  ValueError("Please update Mark Obtained to be less than 10")
                        obj[ass_no - 1]["mark_obtainable"] = 10
                    else:
                        if obj[ass_no - 1]["mark_obtained"] > mkobtnble:
                            raise  ValueError(f"Please update Mark Obtained to be \
less than {mkobtnble}")
                        obj[ass_no - 1]["mark_obtainable"] = mkobtnble
                except IndexError:
                    pass
        else:
            if ass_no != "nill":
                try:
                    if mkobtnble != "nill":
                        obj[ass_no - 1]["mark_obtainable"] = mkobtnble
                    if mkobtnd > obj[ass_no - 1]["mark_obtainable"]:
                        raise ValueError("Mark Obtained cannot be more than Mark Obtainable")
                    obj[ass_no - 1]["mark_obtained"] = mkobtnd
                except IndexError:
                    pass
            else:
                if mkobtnble != "nill":
                    obj[(len(obj) - 1)]["mark_obtainable"] = mkobtnble
                if mkobtnd > obj[(len(obj) - 1)]["mark_obtainable"]:
                    raise ValueError("Mark Obtained cannot be more than Mark Obtainable")
                obj[(len(obj) - 1)]["mark_obtained"] = mkobtnd
        self.__assignment = json.dumps(obj)
        self.updated_at = datetime.now()
        return obj

    def rm_assignment(self, ass_no="nill"):
        """remove assignment, default removes last updated"""
        try:
            obj = json.loads(self.__assignment)
        except TypeError:
            obj = []
        except json.JSONDecodeError:
            obj = []
        if len(obj) == 0:
            raise ValueError("Assignment list empty, nothing to remove")
        if ass_no == "nill":
            obj.pop()
        else:
            try:
                obj.pop(ass_no - 1)
            except IndexError:
                pass
        self.__assignment = json.dumps(obj)
        self.updated_at = datetime.now()
        return obj

    def view_assignment(self, py_obj=False):
        """view assignment default returns json string
        True as second arg returns python list object"""
        if py_obj is True:
            return json.loads(self.__assignment)
        return self.__assignment

    def add_test(self, ass_no = "nill", mkobtnble = "nill",
                       mkobtnd = "nill"):
        """
        adds test,  default is 20
        update mark obtainable, by default updates latest to 20
        update mark obtained, default updates latest
        """
        try:
            obj = json.loads(self.__test)
        except TypeError:
            obj = []
        except json.JSONDecodeError:
            obj = []
        if mkobtnd == "nill":
            if ass_no == "nill":
                if mkobtnble == "nill":
                    obj.append({"mark_obtained": 0, "mark_obtainable": 20})
                else:
                    obj.append({"mark_obtained": 0, "mark_obtainable": mkobtnble})
            else:
                try:
                    if mkobtnble == "nill":
                        if obj[ass_no - 1]["mark_obtained"] > 20:
                            raise  ValueError("Please update Mark Obtained to be less than 20")
                        obj[ass_no - 1]["mark_obtainable"] = 20
                    else:
                        if obj[ass_no - 1]["mark_obtained"] > mkobtnble:
                            raise  ValueError(f"Please update Mark Obtained to be \
less than {mkobtnble}")
                        obj[ass_no - 1]["mark_obtainable"] = mkobtnble
                except IndexError:
                    pass
        else:
            if ass_no != "nill":
                try:
                    if mkobtnble != "nill":
                        obj[ass_no - 1]["mark_obtainable"] = mkobtnble
                    if mkobtnd > obj[ass_no - 1]["mark_obtainable"]:
                        raise ValueError("Mark Obtained cannot be more than Mark Obtainable")
                    obj[ass_no - 1]["mark_obtained"] = mkobtnd
                except IndexError:
                    pass
            else:
                if mkobtnble != "nill":
                    obj[(len(obj) - 1)]["mark_obtainable"] = mkobtnble
                if mkobtnd > obj[(len(obj) - 1)]["mark_obtainable"]:
                    raise ValueError("Mark Obtained cannot be more than Mark Obtainable")
                obj[(len(obj) - 1)]["mark_obtained"] = mkobtnd
        self.__test = json.dumps(obj)
        self.updated_at = datetime.now()
        return obj

    def rm_test(self, ass_no="nill"):
        """remove test, default removes last updated"""
        try:
            obj = json.loads(self.__test)
        except TypeError:
            obj = []
        except json.JSONDecodeError:
            obj = []
        if len(obj) == 0:
            raise ValueError("Assignment list empty, nothing to remove")
        if ass_no == "nill":
            obj.pop()
        else:
            try:
                obj.pop(ass_no - 1)
            except IndexError:
                pass
        self.__test = json.dumps(obj)
        self.updated_at = datetime.now()
        return obj

    def view_test(self, py_obj=False):
        """returns test results
        default returns a json string
        true as arg retunrs python list"""
        if py_obj is True:
            return json.loads(self.__test)
        return self.__test

    def add_exam(self, mkobtained, mkobtainable=60):
        """
        adds student mark
        default is 60
        """
        try:
            obj = json.loads(self.__exam)
        except ValueError:
            obj = [] #{"mark_obtainable": 0, "mark_obtained": 60}
        except json.JSONDecodeError:
            obj = [] #{"mark_obtainable": 0, "mark_obtained": 60}
        obj.append({"mark_obtainable": mkobtainable, "mark_obtained": mkobtained})
        # obj["mark_obtainable"] = mkobtainable
        # obj["mark_obtained"] = mkobtained
        self.__exam = json.dumps(obj)
        self.updated_at = datetime.now()
        return obj

    def view_exam(self, py_obj=False):
        """
        returns exam default returns
        json string otherwise python dict"""
        if py_obj is True:
            return json.loads(self.__exam)
        return self.__exam

    def calc_score(self):
        """
        returns a dictionary of detailed total sccore
        breakdwon turned true break down
        """
        attendance = 10
        # print("assignment***********************")
        assignment = get_average(self.view_assignment(True), 10)
        # print("test****************************")
        test = get_average(self.view_test(True), 20)
        # print("exam***********************")
        exam = get_average(self.view_exam(True), 60)
        breakdown_dict = {"attendance": attendance, "test": test,
                          "assignment": assignment, "exam":exam}
        result = {}
        total = attendance + assignment + test + exam
        result.update(breakdown_dict)
        result.update(check_grade(total))
        result.update(total=total)
        # get course code method needs to be added so that it is updated
        # to the result. and weighted point is calculated
        self.__score = json.dumps(result)
        self.updated_at = datetime.now()
        return result


def get_average(score_list, obtainable):
    """
    returns the average score based on the obtainable
    """
    total_mark = {"total_obtained": 0, "total_obtainable": 0}
    # print(score_list, type(score_list))
    i = 0
    for score in score_list:
        total_mark["total_obtainable"] += score["mark_obtainable"]
        total_mark["total_obtained"] += score["mark_obtained"]
        i += 1
        # print(total_mark, i)
    # print(total_mark)
    return round(total_mark["total_obtained"] / total_mark["total_obtainable"] * obtainable, 2)

def check_grade(score):
    """returns a tuple of grade and point"""
    if score > 100 or score < 0:
        raise ValueError("Score must be within 0 and 100")
    score_list = [(39, 0), (49, 40), (59, 50), (69, 60), (100, 70)]
    for i in range(len(score_list)):
        if score > score_list[i][1] and score < score_list[i][0]:
            i += 1
            break
    grade = {5:"A", 4:"B", 3:"C", 2:"D", 1:"1"}
    return {"grade": grade[i], "point": i}
