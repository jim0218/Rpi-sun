import RPi.GPIO as GPIO
import os
import time , serial

def gpio_init(pinlist):  #GPIO腳位設定    
    GPIO.setmode(GPIO.BCM)    
    GPIO.setup(pinlist,GPIO.OUT,initial=GPIO.HIGH)  #(pin,腳位輸出OUT,預設值=HIGH)
    return "gpio init ok"



def pi_clock():    #pi 校正時間
    GM500_PORT =  "/dev/ttyUSB1"
    GM500_BAUNDRAT = 19200
    GM500_ser = serial.Serial(GM500_PORT,GM500_BAUNDRAT,8,"N",1,timeout=5)
    GM500list = []

    while True:
        GM500_return = GM500_ser.readline()
        GM500_return = GM500_return.decode("utf-8",errors="ignore")        
        if "Q" in GM500_return :
            GM500list.append(GM500_return.split(","))
            time =   GM500list[0][-4].replace("T"," ")[:-2]            
            time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")+datetime.timedelta(hours=8)
            os.system(f"sudo date -s {time}")
            GM500_ser.close() 
            return "Calibration time OK"

# gm500 = 22
# rudics = 23
# imm = 24
# atm926 = 25
pinlist=[22,23,24,25]

print("time sleep 120s....")
time.sleep(120)

print("Calibration time.......")
rpiclock = pi_clock()
print(rpiclock)

print("gpio init......")
gpioinit = gpio_init(pinlist)
print(gpioinit)
