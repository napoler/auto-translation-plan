
from fun import random_date

import datetime


end_time=datetime.datetime.now()
start_time=datetime.datetime.now() + datetime.timedelta(days=-150) # 当前时间减去3分钟

print(random_date(start=start_time,end=end_time))