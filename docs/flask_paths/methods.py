#!/usr/bin/python3
"""this module contains useful
functions neccesary for the app to work
"""

import json

def add_student_info(session: str, level:str, student_dict:dict=None):
    """
    creates a json file data for session if not exist
    adds student json data to the preexisting data
    returns nothing
    """
    if student_dict is None:
        student_dict = {}
    filename = f"storage/student-other-info/{level}-{session}.json"
    with open(filename, "w+", encoding="utf8") as file:
        try:
            datas = json.load(file)
        except json.JSONDecodeError:
            datas = {}
    with open(filename, "w+", encoding="utf8") as file:
        if student_dict.get("id") in datas:
            datas[student_dict.get("id")].update(student_dict)
        else:
            datas.update({f"{student_dict.get('id', '1')}": student_dict})
        json.dump(datas, file)


def load_student_info(sess: str, level:str, id:str) -> dict:
    """returns student other info data"""
    filename = f"storage/student-other-info/{level}-{sess}.json"
    with open(filename, 'w+', encoding='utf-8') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = {}
    return data.get(id, {})
