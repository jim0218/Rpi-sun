import pandas as pd
from datetime import datetime, date

#平均資料 (開始的筆數)
def avgdata(startindex):
    with open ("/home/databuoy/python/sun/config.txt","r") as c:        
        send_file = c.read().split()[0]

    data = pd.read_csv("/home/databuoy/python/sun/{}.csv".format(send_file))
    data = data.values.tolist()

    x = []
    avg_list = []
    for j in range(len(data[0])):
        for i in range(startindex,len(data)):    # range( 起始行數 , len(data) )            
            try:
                x.append(float(data[i][j]))
            except:
                continue
        # print(x)
        # print("len:",len(x))
        avg = sum(x)
        avg_list.append(round(avg/len(data),3))
        x.clear()
    avg_list[0] = "$Q"
    avg_list[-4] = data[startindex][-4].replace("T",",")
    avg_list[-1] = "check code" +"*"

    avg_data = ""
    for i in avg_list:
        if i == avg_list[-1]:
            avg_data = avg_data + str(i)
        else:
            avg_data = avg_data + str(i) + ","

    return [send_file,avg_data]


#開始的筆數 ( 現在時間分 )
def dataindex( nowminute ):
    with open ("/home/databuoy/python/sun/config.txt","r") as c:
        send_file = c.read()

    data = pd.read_csv("/home/databuoy/python/sun/{}.csv".format(send_file))
    data = data.values.tolist()

    for i in range(len(data)-1):
        index = i
        time1 = data[0][-4].replace("T"," ")[:-2]
        time1 = datetime.strptime(time1, "%Y-%m-%d %H:%M:%S")

        time2 = data[i][-4].replace("T"," ")[:-2]
        time2 = datetime.strptime(time2, "%Y-%m-%d %H:%M:%S")

        minute = (time2 - time1).seconds // 60
        if minute >= (nowminute//10)*10:
            return index

def Now_time():
    now_time = datetime.datetime.now()
    year = str(now_time.year)
    if now_time.month <10:
        month = "0"+str(now_time.month)
    day = str(now_time.day)
    hour = int(now_time.hour)
    if hour <10:
        hour = "0"+str(hour)
    minute = str(now_time.minute)
    return [year,month,day,hour,minute]