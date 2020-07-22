import datetime

endTime = datetime.datetime.now() + datetime.timedelta(minutes=1)
print('starting time',datetime.datetime.now())
while True:
  if datetime.datetime.now() >= endTime:
    print(datetime.datetime.now())
    break