import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import requests
import tkinter
from tkinter import *
import tkinter.messagebox
from pytube import YouTube
from os import system
import re
import urllib
import threading
import subprocess
import time

length = 0
stopped = False
downloaded_var = False
title = ""
tries = 0

def command(comm):
    stopbtn.configure(command=stop)
    playbtn.configure(command=ap)
    print("playing")
    system(comm)
    playbtn.configure(command=play)
    stopbtn.configure(command=None)

def ap():
    tkinter.messagebox.showinfo("already playing","the song is already playing..")
    return

def playing():
  minutes = length//60
  seconds = length%60
  minute = 0
  for i in range(minutes):
    if minute < 10:
      minute = "0"+str(minute)
    second = 0
    for i in range(60):
      if second < 10:
        second = "0"+str(second)
      if stopped:
        time.sleep(1)
        status_var.set("music stopped")
        time.sleep(1)
        status_var.set("press play to play the song!")
        return
      status_var.set("playing "+title+" ("+str(minute)+":"+str(second)+")")
      if type(second) == str:
        second=int(second[1])
      time.sleep(1)
      second+=1
    if type(minute) == str:
        minute=int(minute[1])
    minute+=1
  for secondvar in range(0,seconds):
      if secondvar < 10:
        secondvar = "0"+str(secondvar)
      status_var.set("playing "+title+" ("+str(minute)+":"+str(secondvar)+")")
      time.sleep(1)
  time.sleep(1)
  status_var.set("press play to play the song!")
  playbtn.configure(command=play)

def play():
  global stopped
  global downloaded_var
  stopped = False
  playbtn.configure(command=ap)
  t = threading.Thread(target=get,args=[E1.get()]) 
  t.start()

  return
def stop():
   global stopped
   print("stopping..")
   playbtn.configure(command=play)
   playbtn.configure(bg="white")
   process = subprocess.Popen(['killall','afplay'], 
                           stdout=subprocess.PIPE,
                           universal_newlines=True)
   print("returning")
   stopped=True
   return

def downloading():
    global downloaded_var
    print("donwloading..")
    while not downloaded_var:
     if downloaded_var:
       return
     time.sleep(1)
     status_var.set("downloading.")   
     if downloaded_var:
       return
     time.sleep(1)
     status_var.set("downloading..")
     if downloaded_var:
       return
     time.sleep(1)
     status_var.set("downloading...")

def get(search_query):
 global downloaded_var
 global tries
 downloaded = False
 playbtn.configure(bg="grey")
 while not downloaded:
  try:
    global length
    global title
    res = requests.get("https://www.youtube.com/results?search_query="+search_query)
    vid = re.findall(r"watch\?v=(.{11})",res.text)[0]
    yt = YouTube("youtube.com/watch?v="+vid)
    if yt.length > 60*60:
      tkinter.messagebox.showerror("video too long","video should not be longer than 60 minutes")
      return
    t=threading.Thread(target=downloading)
    t.start()
    t = yt.streams.filter(only_audio=True).all()
    t[0].download(filename="video")
    length = yt.length
    title = yt.title
    downloaded_var = True
    t2 = threading.Thread(target=command,args=["afplay video.mp4"])
    t2.start()
    t3 = threading.Thread(target=playing)
    t3.start()
    return True
  except requests.exceptions.ConnectionError:
     tkinter.messagebox.showerror("Connection error!","please connect to internet to listen to music")
     playbtn.configure(command=play)
     break
  except urllib.error.HTTPError:
    continue
    

window = tkinter.Tk()
window.title("saavn(remake)")
window.geometry('800x500')
window.configure(bg="tomato")

status_var = StringVar()

status_var.set("press play to play the song!")

status = Label(window,textvariable=status_var,background="white")
E1 = Entry(window)
l1 = Label()
label1 = Label(window,text="Song Name-",relief=RAISED)
playbtn = Button(window,text="Play!",command=play,border=20,width=10,background="black")
stopbtn = Button(window,text="stop",width=10)

l1.pack(pady=50)
l1.configure(bg="tomato")
label1.pack()
status.configure(bg="white")
E1.pack()
E1.configure(relief=SUNKEN,width=30)
status.pack(pady=80)
playbtn.pack(side=LEFT,pady=15,padx=200)
stopbtn.pack(side=LEFT)

window.mainloop()
