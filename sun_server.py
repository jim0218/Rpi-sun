#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import datetime ,time
HOST = '0.0.0.0'
PORT = 4000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)
print('server start at: %s:%s' % (HOST, PORT))
print('wait for connection...')

data = []
recv_data = ""

while True:
    client, addr = s.accept()
    print('connected by ' + str(addr))

    while True:
        indata = client.recv(1024)
        indata = indata.decode()
        print('recv: ' + indata)
        
        recv_data = recv_data+indata
        
        start_index = recv_data.find("$")    #資料開頭的index
        end_index = recv_data.find("*")      #資料結尾的index

        if start_index != -1 and end_index != -1:
            data.append(recv_data[start_index:end_index+1])  #抓資料放list
            recv_data = recv_data[end_index+1:]              #移除已存入list的資料
        print("data: ",data)
        print("datalen:",len(data))
        # if "finish" in indata and len(data)>=2:
        #     client.send(b"receiveok\r\n")
        
        if len(data)==3  or  len(indata) == 0 :    # connection closed
            now_time = datetime.datetime.now()
            receive_time = str(now_time)[:-7]
            client.send(b"receiveok\r\n")
            client.close()                                  #結束連線 儲存資料
            print("closed connection.")
            print(f"open file {data[0][1:-1]}.csv")
            with open ("{}.csv".format(data[0][1:-1]),"a") as f:
                print(f"write in:{data[1]}\n")
                f.write(f"{data[1]}\n")
                f.write(f"send_time,{data[2]}\n")
                f.write(f"receive_time,{receive_time}\n")
                print("write down")
                data.clear()
                recv_data = ""
                f.close()
            break
        else:
            continue    