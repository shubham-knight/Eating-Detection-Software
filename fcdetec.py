import cv2
import dlib
from math import hypot
import os
from win32com.client import GetObject
import pyautogui
from time import sleep
import winsound
from tkinter import *  
from tkinter import messagebox 
import ctypes
import platform
from ctypes import CDLL

WMI = GetObject('winmgmts:')
processes = WMI.InstancesOf('Win32_Process')


cap = cv2.VideoCapture(0)    #Turn on the camera

detector = dlib.get_frontal_face_detector()    
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")




font = cv2.FONT_HERSHEY_PLAIN
timer = 0
flag=0
last_state= 0
while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = detector(gray)

    #print(timer)
    for face in faces:

        
        landmarks = predictor(gray,face)
        left_point = (landmarks.part(60).x , landmarks.part(60).y)
        right_point = (landmarks.part(64).x , landmarks.part(64).y)
            
        upper_point = (landmarks.part(51).x , landmarks.part(51).y)
        bottom_point = (landmarks.part(57).x , landmarks.part(57).y)
            
        upper_point_nose = (landmarks.part(33).x , landmarks.part(33).y)
        bottom_point_chin= (landmarks.part(8).x , landmarks.part(8).y)
            
        hor_line = cv2.line(frame, left_point,right_point, (0,255,0),2)
        ver_line = cv2.line(frame, upper_point,bottom_point, (255,0,0),2)
        
            
            
        ver_line_len= hypot((upper_point[0] - bottom_point[0]) , (upper_point[1] - bottom_point[1]))
        hor_line_len= hypot((left_point[0] - right_point[0]) , (left_point[1] - right_point[1]))
        ratio =hor_line_len/ver_line_len
        #print(ratio)
        
        #print(timer)
        #print(last_state)
        if ratio > 2.3:
            if last_state == 0:
                timer+=1
            else:
                timer=0
                last_state=0
            
            if timer>=100:
               
                cv2.putText(frame,"Warning Start Eating", (50,50), font, 3, (0,0,255))
                if timer%200 ==0:
                    top = Tk()  
                    top.geometry("100x100")      
                    top.eval('tk::PlaceWindow %s center' % top.winfo_toplevel())
                    top.lift()
                    top.attributes("-topmost", True)
                    top.withdraw()
                    messagebox.showwarning("warning","Warning : Start Eating or the screen will lock itself!!!") 

                    top.deiconify()
                    top.destroy()
                    top.quit()
                #timer=0
                #last_state=0
                #window = Tk()
                #window.geometry("100x100")      
                #window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
                #window.withdraw()
                
                #if messagebox.askquestion("warning","Do You Want to continue??") == False: 
                #    timer=0
                #    last_state=0
                # else:
                #     flag=1
                #    cap.release()
                #    cv2.destroyAllWindows()
                #     window.deiconify()
                #    window.destroy()
                #   window.quit()
                #    break
                    
                    
            if timer>=800:
                if platform.system()=='Windows':
                    ctypes.windll.user32.LockWorkStation()
                    timer=0
                    last_state=0
                    break
                elif  platform.system()=='Linux':
                    os.popen('gnome-screensaver-command --lock')
                    timer=0
                    last_state=0
                    break
                else:
                    loginPF = CDLL('/System/Library/PrivateFrameworks/login.framework/Versions/Current/login')
                    result = loginPF.SACLockScreenImmediate()
                    timer=0
                    last_state=0
                    break
            
            #cv2.putText(frame,"Not eating", (50,150), font, 3, (255,0,0))
        else :
            if last_state == 1:
                timer+=1
            else:
                timer=0
                last_state=1
            cv2.putText(frame,"Eating", (50,150), font, 3, (255,0,0))
    
    
    
    cv2.imshow("Face Landmarks", frame)
    key = cv2.waitKey(1)
    if cv2.getWindowProperty("Face Landmarks", cv2.WND_PROP_AUTOSIZE) < 1:
        break
    
    if key == 27 or flag==1:
        break
cap.release() 
cv2.destroyAllWindows()