#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import MongoDB as db
import Current_time
import sys

TOKEN = 'https://api.telegram.org/bot709273597:AAE0wgZwOtPku0IZeyP1bh7YAHbhhW_YtJo/'

#select offset from db
def get_offset_from_db():
    try:
        return db.get_offset()
    except:
        db.add_new_offset(0)
        return get_updates_messages()[0]['update_id']

#get telegram json messages information
def get_updates_messages():
    messages_json = json.dumps(requests.get(TOKEN + 'getUpdates', data={'offset': get_offset_from_db()}).json())
    messages_json = json.loads(messages_json)["result"]
    return messages_json

#get offset from telegram json
def get_offset():
    return get_updates_messages()[0]['update_id']

#get count off all messages
def get_message_count():
    count = len(get_updates_messages())
    return count

#get info about user message
def get_message_info(message_id = 0):
    print get_updates_messages()[message_id]
    user_id = int(get_updates_messages()[message_id]['message']['from']['id'])
    user_message = str(get_updates_messages()[message_id]['message']['text'].encode('utf-8'))
    return [user_id,user_message]

#trying to save the offset
def save_offset():
    try:
        db.add_new_offset(get_offset()+1)
    except:
        print 'you dont have new messages for make new offsets'
    pass
#to add some remind user must take several steps
#0 - add remind text
#1 - add remind time
__USERS_ANSWER_STEP = {}

#add to db remind text info
def set_remind_text(user_id,user_text):
    db.add_remind_text(user_id,
                       user_text
                       )

#add to db remind time info
def set_remind_time(user_id,user_text):
    datetime = Current_time.descrypt_datetime(user_text)
    db.add_remind_time(user_id,
                       Current_time.desrypt_turple_time((datetime[2],datetime[3])),
                       str(datetime[0]),
                       str(datetime[1])
                       )
#add to the dict user answer step
def set_user_answer_step(user_id,step):
    global __USERS_ANSWER_STEP
    __USERS_ANSWER_STEP[user_id] = step

#get from the dict user answer step
def check_user_answer_step(user_id):
    global __USERS_ANSWER_STEP
    user_answer_step = 0
    if not user_id in __USERS_ANSWER_STEP:
        __USERS_ANSWER_STEP[user_id] = 0
    else:
        user_answer_step = __USERS_ANSWER_STEP[user_id]
    return user_answer_step

#write a message to user by user_id
def make_answer(user_id,user_text,user_answer_step = 0):

    if user_answer_step == 0:
        requests.post(TOKEN + 'sendMessage', data={'chat_id': user_id, 'text': '"'+user_text+'"'+'This is your remind'})
        set_remind_text(user_id,user_text)
        requests.post(TOKEN + 'sendMessage', data={'chat_id': user_id, 'text': 'Write plz the date, like "mouth/day/hour:minute"'})
        requests.post(TOKEN + 'sendMessage', data={'chat_id': user_id, 'text': 'Example: 3:24/8:24"'})

        set_user_answer_step(user_id,1)
    #
    if user_answer_step == 1:
        requests.post(TOKEN + 'sendMessage', data={'chat_id': user_id, 'text': '"'+user_text+'"'+'This is your date'})
        requests.post(TOKEN + 'sendMessage', data={'chat_id': user_id, 'text': 'Trying to set your remind...'})

        if Current_time.check_datatime_valid(user_text):
            set_remind_time(user_id,user_text)
            requests.post(TOKEN + 'sendMessage', data={'chat_id': user_id, 'text': 'Your remind added, good luck!'})
            set_user_answer_step(user_id, 0)
        else:
            requests.post(TOKEN + 'sendMessage', data={'chat_id': user_id, 'text': 'This date not valid, plz try again.'})
            db.delete_last_remind()
            set_user_answer_step(user_id, 0)


def update():
    #take a count of not read messages
    count = get_message_count()
    for i in range(count):
        #check and set user answer id
        user_answer_step = check_user_answer_step(get_message_info(i)[0])
        #write message by answer step
        make_answer(get_message_info(i)[0],get_message_info(i)[1],user_answer_step)

        #add new offset
        if i==count-1: save_offset()
    #restart, create a cicle
    update()

db.init_db(True)
#start bot
update()


# print json.loads(jsotTEXT)["result"][0]['message']['from']['id']