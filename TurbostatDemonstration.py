#!/usr/bin/env python3

import subprocess as sp
from threading import Thread
from time import sleep
from datetime import datetime, timedelta
import pandas as pd
import sys
import os
from matplotlib import pyplot as plt

run = True
programExec = False
data = {"index":[],"time":[],"value":[],"executing":[]}
def readturbostat():
    global programExec
    global data
    cmd = "sudo turbostat --cpu 22 --interval 0.05 --hide usec,Time_Of_Day_Seconds,Package,Die,Core,CPU,APIC,X2APIC,Avg_MHz,Busy%,Bzy_MHz,TSC_MHz,IPC,IRQ,POLL,C1,C2,POLL%,C1%,C2%,PkgWatt"
    process = sp.Popen(cmd,stdout=sp.PIPE,stderr=sp.PIPE,shell=True)
    index = 0

    start_time = datetime.now()
    while(run == True):
        line = process.stdout.readline().decode().strip()
        if(line == "CorWatt"):
            data["executing"].append(programExec)
            time = datetime.now()
            #time_elapsed = datetime.now() - start_time
            data["time"].append(time)
            line = process.stdout.readline()
            line = float(process.stdout.readline().decode())
            data["value"].append(line)
            data["index"].append(index)
            index += 1
    print("Stopped")

if(len(sys.argv)<2):
    print("Command missing")
    exit(-1)

colormap = ["green","red"]

t = Thread(target = readturbostat)
t.start()
sleep(1)
cmd = sys.argv[1:]
programExec = True
p = os.popen(" ".join(cmd))
print(p.read())
programExec = False
sleep(1)
run = False
sleep(1)
print(data)

plt.figure(figsize=(24,8))

# labels
plt.xlabel('time(s)', fontsize=15)
plt.ylabel('core Watt', fontsize=15)

x = []
y = []
old = False
for i in range(len(data["index"])):
    if data["executing"][i] == old:
        x.append(data["time"][i])
        y.append(data["value"][i])
    else:
        x.append(data["time"][i])
        y.append(data["value"][i])
        print(x,y)
        if(old):
            im = plt.plot(x,y,"o-",color="red",markersize=0.1)
        else:
            im = plt.plot(x,y,"o-",color="green",markersize=0.1)
        old = data["executing"][i]
        x = [data["time"][i]]
        y = [data["value"][i]]
print(x,y)

if(old):
    im = plt.plot(x,y,"o-",color="red",markersize=0.1)
else:
    im = plt.plot(x,y,"o-",color="green",markersize=0.1)
old = data["executing"][i]
x = [data["time"][i]]
y = [data["value"][i]]

plt.savefig("output.svg")
data = pd.DataFrame(data)
print(data)
data.to_csv("output.csv")



# if(len(sys.argv)<2):
#     print("Command missing")
#     exit(-1)


# t = Thread(target = readturbostat)
# t.start()
# sleep(1)
# cmd = sys.argv[1:]
# programExec = True
# p = os.popen(" ".join(cmd))
# print(p.read())
# programExec = False
# sleep(1)
# run = False
# sleep(1)
# data = pd.DataFrame(data)
# data_execute = data[data["executing"]==True]
# print("EXECUTE")
# print(data_execute)
# execute_time = data_execute["index"]
# # execute_time = data_execute["time"]
# execute_power = data_execute["value"]
# data_nonexecute = data[data["executing"]==False]
# print("NON-EXECUTE")
# print(data_nonexecute)
# non_execute_time = data_nonexecute["index"]
# # non_execute_time = data_nonexecute["time"]
# non_execute_power = data_nonexecute["value"]

# # execute_power.plot(use_index=True,color="red")
# # non_execute_power.plot(use_index=True,color="green")


# plt.plot(execute_time,execute_power,"o-",color="red")
# plt.plot(non_execute_time,non_execute_power,"o-",color="green")
# # plt.plot(data["index"],data["value"],color=data["executing"])
# plt.savefig("output.svg")



# data.to_csv("output.csv")
