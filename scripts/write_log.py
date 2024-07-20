import datetime as dt
def log(message):
    time = dt.datetime.now()
    with open('./data/log/log', 'a') as a:
        a.write(f'{message} {time}\n')
        
