import datetime as date

def descrypt_datetime(text_datetime = '12:3/12:4'):
    datetime = (
        (text_datetime.split("/")[0].split(":")[0],text_datetime.split("/")[0].split(":")[1]),
        (text_datetime.split("/")[1].split(":")[0],text_datetime.split("/")[1].split(":")[1])
    )
    mouth = int(datetime[0][0])
    day = int(datetime[0][1])
    hour = int(datetime[1][0])
    minute = int(datetime[1][1])

    return (mouth,day,hour,minute)
def desrypt_turple_time(turple_time = (12,55)):
    time = ''+str(turple_time[0])+':'+str(turple_time[1])
    return time

def time_check_valid(text_time = '12:01'):
    status = True
    time = ''
    #---------------------------------
    # ':' check
    try:
        if ':' in text_time:
            time = text_time.split(':')
    except:
        status = False
    #---------------------------------
    # check for integer
    try:
        time[0] = int(time[0])
        time[1] = int(time[1])
    except:
        status = False
    #---------------------------------
    # check time valid
    try:
        if time[0]>=0 and time[0]<=24 and time[1]>=0 and time[1]<=59:
            pass
        else:
            status = False
    except:
        status = False
    #-----**---------**--------**----------**

    return status
def date_check_valid(text_date = '9:14'):
    status = True
    date = ''
    # ---------------------------------
    # ':' check
    try:
        if ':' in text_date:
            date = text_date.split(':')
    except:
        status = False
    # ---------------------------------
    # check for integer
    try:
        date[0] = int(date[0])
        date[1] = int(date[1])
    except:
        status = False
    # ---------------------------------
    # check time valid
    try:
        if date[0] > 0 and date[0] <= 12 and date[1] > 0 and date[1] <= 30:
            pass
        else:
            status = False
    except:
        status = False
    # -----**---------**--------**----------**

    return status
def check_datatime_valid(text_datetime = '12:3/12:4'):
    status = True
    try:
        datetime = descrypt_datetime(text_datetime)
        if time_check_valid(''+str(datetime[2])+':'+str(datetime[3])):
            pass
        else:
            status = False
        print ''+str(datetime[0])+':'+str(datetime[1])
        print status
        if date_check_valid(''+str(datetime[0])+':'+str(datetime[1])):
            pass
        else:
            status = False
        print ''+str(datetime[2])+':'+str(datetime[3])
        print status
    except:
        status = False

    return  status

def get_time():
    cur_date = date.datetime.now()
    time = (cur_date.hour,cur_date.minute)
    return time


