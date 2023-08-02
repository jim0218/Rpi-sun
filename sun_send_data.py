import serial
import time , os
import datetime
from  sun_avg_csv import avgdata ,dataindex ,Now_time
import RPi.GPIO as GPIO

def step1(): #撥號1
    errorcount = 0
    while True:        
        print("input:at+cbst=XX,X,X")
        Arudics_ser.write(b'at+cbst=XX,X,X\r\n')
        time.sleep(1)
        while True:        
            Arudics_return = Arudics_ser.readline().decode()
            print("return:",Arudics_return)                
            if "OK"  in Arudics_return :                
                return "Step1 OK"
            elif "at+cbst=71,0,1" in Arudics_return:                
                continue
            elif errorcount == 3:
                return "call error"
            else:
                errorcount+=1
                break

#at
#OK
#at+cbst=71,0,1
#OK
#atdt0088160000564
#CONNECT 19200
#NO CARRIER


def step2(): #撥號2
    errorcount = 0
    while True:
        print("input:atdtXXXXXXXXXXXXX")
        Arudics_ser.write(b"atdtXXXXXXXXXXXXX\r\n")
        time.sleep(1)
        while True:            
            Arudics_return = Arudics_ser.readline().decode()
            print(Arudics_return)
            if "CONNECT"  in Arudics_return:                
                return "Step2 OK"            
            elif "CARRIER" in Arudics_return:
                errorcount +=1                                            
            elif errorcount == 3:
                return "call error"            
            else:
                continue                               
                
                
            
def step3(data,start_time):  #傳資料
    #now_time = datetime.datetime.now()

    data = str(data) +"\r\n"
    data = data.encode()
    Arudics_ser.write(data)
    time.sleep(0.5)

    now_time = datetime.datetime.now()
    send_time = "$"+ str(now_time)[:-7] + "*" +"\r\n"
    send_time = send_time.encode()
    Arudics_ser.write(send_time)
    
    return "send finish"

def configtxt():  #config.txt 更新下一個檔案
    with open ("/home/databuoy/python/sun/config.txt","r+") as f:
        w = f.read().split()[0]
        f.seek(0) #文件指針歸0
        write_next = datetime.datetime.strptime(w, '%Y%m%d%H%M')
        delta = datetime.timedelta(hours=1)
        write_next = write_next + delta
        write_next = str(write_next)
        f.write(write_next.replace("-", "").replace(":", "").replace(" ", "")[:-2])
        f.close()

def gpiocontrol(pin,control):
    if control == "HIGH":
        GPIO.output(pin,GPIO.HIGH)
    elif control == "LOW":
        GPIO.output(pin,GPIO.LOW)

# print("Rudices poweron")
# gpiocontrol(23, "HIGH")
# time.sleep(15)  # 等衛星連線  根據衛星連線的時間調整

# Arudics_PORT = "COM19"
GM500_PORT =  "/dev/ttyUSB3"
Arudics_BAUNDRAT = 19200
Arudics_ser = serial.Serial(GM500_PORT,Arudics_BAUNDRAT,8,"N",1,timeout=10)

Arudics_ser.flushInput()
Arudics_ser.flushOutput()

step1 = step1()
if "OK" in step1:
    Arudics_ser.flushInput()
    Arudics_ser.flushOutput()
    step2 = step2()
else:
   print("step1 error")
   Arudics_ser.close()
   os._exit(0)

if "CONNECT" in step2:
    # nowtime = Now_time()
    # nowminites = nowtime[-1]           #取得現在時間(分)
    # dataindex = dataindex(nowminites)  #取得要從第幾筆資料開始傳    
    # return_datas = avgdata(dataindex)  #取得平均資料
    return_datas = avgdata(0)

    start_send= "start send {}.csv".format(str(return_datas[0]) )+ "\r\n"
    print(f"{start_send}")
    start_send = start_send.encode()
    Arudics_ser.write(start_send)

    time.sleep(0.5)

    filename = "$" + return_datas[0] + "*" +"\r\n"
    filename = filename.encode()
    Arudics_ser.write(filename)

    step3 = step3(return_datas[1])
else:
    print("step2 error")
    Arudics_ser.close()
    os._exit(0)

print(step3)
if step3 == "send finish":

    print("input:finish")
    Arudics_ser.write(b"finish\r\n")
    time.sleep(1)
    configtxt()
    print("END CLOSE")
    Arudics_ser.close()
    os._exit(0)
    # Arudics_return = Arudics_ser.readline().decode()
    # print(Arudics_return)
    # if "receiveok" in Arudics_return: 
        # configtxt()                    #更新config.txt       
        # print("END Close Program ")        
        # Arudics_ser.close()
        # os._exit(0)
        # print("Rudices poweroff")
        # gpiocontrol(23, "LOW")
        # if int(nowminites) >= 50:
        #     configtxt()
