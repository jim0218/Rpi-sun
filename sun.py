import serial
import sys
import time
import datetime
import os
import RPi.GPIO as GPIO


def gpiocontrol(pin,control):   #樹莓派 IO控制
    if control == "HIGH":
        GPIO.output(pin,GPIO.HIGH)
    elif control == "LOW":
        GPIO.output(pin,GPIO.LOW)

def Now_time():               #取得現在時間
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

def Runtime_minute(runminute):      #程式需要執行的時間(分鐘)  
    now_time = datetime.datetime.now()
    run_time = datetime.timedelta(minutes=runminute)
    run_time = now_time + run_time
    minute = run_time.minute
    return minute

# print("GM500 power-on")    
# gpiocontrol(22,"HIGH")  #樹莓派 IO控制  GM500 ON
# time.sleep(5)

# GM500_PORT = "COM24"
GM500_PORT =  "/dev/ttyUSB1"
GM500_BAUNDRAT = 19200
GM500_ser = serial.Serial(GM500_PORT,GM500_BAUNDRAT,8,"N",1,timeout=5)

nowtime = Now_time()
runtime = Runtime_minute(2)   # 執行時間 (分鐘)

with open ("/home/databuoy/python/sun/config.txt","a+") as c:
    c.seek(0) 
    filecheck = len(c.read())
    c.seek(0)
    if filecheck == 0:
        print("create config.txt")
        c.write("{}{}{}{}00".format(nowtime[0],nowtime[1],nowtime[2],nowtime[3]))        
    else:
        # print("oldfile")
        c.close()

try:
    while True:
        nowtime = Now_time()
        GM500_return = GM500_ser.readline()
        GM500_return = GM500_return.decode("utf-8",errors="ignore")

        if int(nowtime[-1]) ==  int(runtime):
            print("time out")
            print("Close Program")
            GM500_ser.close()
            # print("GM500 poweroff")
            # gpiocontrol(22, "LOW")
            os._exit(0)
            break

        if "Q" in GM500_return :
            #時間 +8hr
            GM500_return = GM500_return.split(",")
            time0 = GM500_return[-4].replace("T"," ")[:-2]
            time8 = datetime.datetime.strptime(time0, "%Y-%m-%d %H:%M:%S")+datetime.timedelta(hours=8)
            GM500_return[-4] = str(time8).replace(" ","T")
            GM500_return = ",".join(GM500_return)
            
            print(f"open file {nowtime[0]}{nowtime[1]}{nowtime[2]}{nowtime[3]}00.csv")
            with open ("/home/databuoy/python/sun/{}{}{}{}00.csv".format(nowtime[0],nowtime[1],nowtime[2],nowtime[3]),"a") as f:
                f.write(f"{GM500_return}\n")
            print(f"write in:{GM500_return}\n")
            time.sleep(1)

except:
    GM500_ser.close()
    os._exit(0)
    # gpiocontrol(22, "LOW")
