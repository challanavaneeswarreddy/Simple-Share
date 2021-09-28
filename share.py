import pymsgbox
import socket
import cv2
import numpy as np
import os
import pyautogui
import pyperclip
from collections import deque



#share module
		


def share():
	#checks the active hotspots and returns them
	x=os.popen('nmcli -g SSID dev wifi list').read()
	#the returned output should be like Rgukt\nOngole\n
	#below line splits the output at \n and stores them in an array 
	x=x.split('\n')
	print(x)
	cap = cv2.VideoCapture(0)
	#while True:
	ret, frame = cap.read()
	img = cv2.rectangle(frame, (10,6) , (630,55) , (224,78,98) , -1)
	cv2.putText(img, "Choose the Receiver"  ,(175,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2 , cv2.LINE_AA)
		
		
	i=0
	#prints all the retunred hotspots
	for y in x:
		pox=((i+1)*65)+5*i
		poy=130+(70*i)
		print(pox," ",poy," ",y)
		if(y==''):
			break
		string=(str(i+1)," ",y)
		img = cv2.rectangle(frame, (42,pox) , (590,poy) , (247,160,140) , -1)
		cv2.putText(img, str(i+1)+" "+y ,(75,105+(70*i)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1 )
		i+=1
	cv2.putText(img, " Chose the Option ? Then, Click Q to enter "  ,(60,105+(70*i)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0 , 255), 2 )
	#cv2.putText(img, " Want to Exit ? Then, Click E to exit "  ,(95,105+(70*i)+50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0 , 255), 2 )

	
	cv2.imshow('frame', frame)
	if cv2.waitKey():
		response = pymsgbox.prompt('Enter  your Option ')
		try:
			wifi=x[int(response)-1]
		except:
			pymsgbox.alert('Chose the correct Option', 'Title')
		else:
			print(wifi)
			#wifi=wifi.replace(" ",'%s')
			cmd=f"nmcli con up id '{wifi}'"
			cmd2=f"nmcli dev wifi connect '{wifi}' password SimpleShare"
			status=os.system(cmd)
			print(status)
			if(status!=0):
				print(f"wifi value {wifi}")
				os.system(cmd2)
			ip=os.popen('hostname -I').read()
			ip=ip.split(' ')
			ip=ip[0]
			print(ip)
			cap.release()
			cv2.destroyAllWindows() 	
			client(ip)
				
	
	


		
def client(ip):
	cap = cv2.VideoCapture(0)

	yellow_lower = np.array([22, 93, 0])
	yellow_upper = np.array([45, 255, 255])
	prev_x = 0
	prev_y = 0
	
	
	

	while True:
		ret, frame = cap.read()
		ret, frame2 = cap.read()
		colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0)]
	    
		diff = cv2.absdiff(frame, frame2)
		if(diff.any()):
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
			contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

			for c in contours:
				area = cv2.contourArea(c)
				if area > 100:
					x, y, w, h = cv2.boundingRect(c)
					cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
				    
				    
				    
					if y < prev_y:
						pyautogui.hotkey('ctrl', 'c')
						date = pyperclip.paste()
						filename=date
						print(filename)
						socketClient(ip,filename)
						continue
					prev_y = x
		cv2.imshow('frame', frame)
		if cv2.waitKey(10) == ord('q'):
			s.close()
			break

	cap.release()
	cv2.destroyAllWindows()
	
	
def socketClient(ip,filename):
	SEPARATOR = "<SEPARATOR>"
	BUFFER_SIZE = 4096
	# the ip address or hostname of the server, the receiver
	host = ip
	# the port, let's use 5001
	port = 5001
	s = socket.socket()
	print(f"[+] Connecting to {host}:{port}")
	s.connect((host, port))
	print("[+] Connected.")

	print(filename)
	filesize = os.path.getsize(filename)
	print(filesize)
	s.send(f"{filename}{SEPARATOR}{filesize}".encode())
	with open(filename, "rb") as f:
		while True:
  			# read the bytes from the file
			bytes_read = f.read(BUFFER_SIZE)
			if not bytes_read:
  				# file transmitting is done
				break
			# we use sendall to assure transimission in 
			# busy networks
			s.sendall(bytes_read)
	s.close()

				
				

