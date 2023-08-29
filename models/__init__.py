#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""


from models.engine.mysql_access import MySQLStorage

vault = MySQLStorage()
vault.reload()
