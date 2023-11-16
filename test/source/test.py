import datetime

now = datetime.datetime.now()
time_string = now.strftime("%Y年%m月%d日%p")

if time_string.endswith('AM'):
    time_string = time_string[:-2] + '上午'
elif time_string.endswith('PM'):
    time_string = time_string[:-2] + '下午'

print(time_string)
