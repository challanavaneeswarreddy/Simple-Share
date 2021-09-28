import pymsgbox
import socket
import cv2
import numpy as np
import os
import pyautogui
import pyperclip
from collections import deque
from share import *
from receive import *


#index page(home page)
def index():
	cap = cv2.VideoCapture(0)
	while True:
		ret, frame = cap.read()
		img = cv2.rectangle(frame, (10,6) , (630,55) , (224,78,98) , -1)
		img = cv2.rectangle(frame, (42,65) , (590,130) , (247,160,140) , -1)
		img = cv2.rectangle(frame, (42,135) , (590,200) , (247,160,140) , -1)
		#img = cv2.rectangle(frame, (42,205) , (590,270) , (247,160,140) , -1)
		cv2.putText(img, "Simple Share"  ,(175,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2 , cv2.LINE_AA)
		cv2.putText(img, "1. SHARE"  ,(75,105), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1 )
		cv2.putText(img, "2. RECEIVE"  ,(75,175), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1 )
		#cv2.putText(img, "3. AIR CANVAS"  ,(75,245), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1 )
		cv2.putText(img, " Chose the Option ? Then, Click Q to enter "  ,(60,300), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0 , 255), 2 )
		cv2.putText(img, " Want to Exit ? Then, Click E to exit "  ,(95,350), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0 , 255), 2 )
		

		if cv2.waitKey(10) == ord('q'):
			response = pymsgbox.prompt('Enter  your Option ')
			cap.release()
			cv2.destroyAllWindows()

			if (response == "1"):
				share()
				index()
			elif (response == "2"):
				receive()
				index()
			else:
				pymsgbox.alert('Chose the correct Option', 'Title')
				index()
		elif cv2.waitKey(10) == ord('e'):
			break


		cv2.imshow('frame', frame)
		
		
		
		

			

index()
