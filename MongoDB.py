#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3 as db
import Current_time

__connection = None

def get_connection():
    global __connection
    if __connection is None:
        __connection = db.connect("remind.db")
        __connection.text_factory = str
    return __connection

def init_db (force = False):
    connection = get_connection()
    curs = connection.cursor()

    if force:
        curs.execute("DROP TABLE IF EXISTS reminders")

    curs.execute("""
        CREATE TABLE IF NOT EXISTS users_offsets (
        id INTEGER PRIMARY KEY,
        offset INTEGER NOT NULL,
        time TEXT NOT NULL
        )
        """)
    curs.execute("""
    CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    time TEXT NOT NULL,
    mouth TEXT NOT NULL,
    day TEXT NOT NULL
    )
    """)
    connection.commit()

def add_new_offset(user_offset):
    connection = get_connection()
    curs = connection.cursor()
    curs.execute("DELETE FROM users_offsets ORDER BY id DESC LIMIT 1")
    connection.commit()
    curs.execute("INSERT INTO users_offsets (offset, time) VALUES (?, ?)", (user_offset,Current_time.desrypt_turple_time(Current_time.get_time())))
    connection.commit()

def add_remind_text (user_id = 0,message = ''):
    connection = get_connection()
    curs = connection.cursor()
    curs.execute("INSERT INTO reminders (user_id, message,time,mouth,day) VALUES (?, ?,?,?,?)",(user_id,message,'0','0','0'))
    connection.commit()
def add_remind_time (user_id = 0,time = '', mouth = '', day = ''):
    connection = get_connection()
    curs = connection.cursor()
    curs.execute("UPDATE reminders SET time = ?,mouth = ?, day = ? WHERE user_id = ?",(time,mouth,day,user_id))
    connection.commit()

def delete_last_remind():
    connection = get_connection()
    curs = connection.cursor()
    curs.execute("DELETE FROM reminders ORDER BY id DESC LIMIT 1")

def get_offset():
    connection = get_connection()
    curs = connection.cursor()
    curs.execute("SELECT offset FROM users_offsets LIMIT 1")
    offset = curs.fetchall()
    return offset[0][0]
