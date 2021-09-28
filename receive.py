import pymsgbox
import socket
import cv2
import numpy as np
import os
import pyautogui
import pyperclip
import threading
from queue import Queue
from collections import deque
#import imutils
#names of the file received stored in this array
receivedFiles="NofilesReceived"
j=0
#flag to stop threading
flag=False
#recieve module
def receive():
	user=os.popen('whoami').read()
	print(user)
	#queue to store files recieved
	q=Queue() 
	cap = cv2.VideoCapture(0)
	ret, frame = cap.read()
	#cvCopy(frame2,frame)
	img = cv2.rectangle(frame, (10,6) , (630,55) , (224,78,98) , -1)
	#checking wheter hotspot is alredy created or not
	cmd=f"nmcli connection up '{user}(simple-share)'"
	print(cmd)
	status=os.system(cmd)
	if(status!=0):
		#to create hotspot with the username that returned from whoami cmd
		cmd2=f"nmcli device wifi hotspot con-name '{user}(simple-share)' ssid '{user}(simple-share)' password SimpleShare"
		status=os.system(cmd2)
			
			
		if(status!=0):
			cv2.putText(img, "Error in creating hotspot"  ,(100,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1 , cv2.LINE_AA)
		cv2.imshow('frame', frame)
		if cv2.waitKey():
			cv2.destroyAllWindows()

	else:
		i=0
		global flag
		img = cv2.rectangle(frame, (10,6) , (630,55) , (224,78,98) , -1)
		
		#img = cv2.rectangle(frame, (42,135) , (590,200) , (247,160,140) , -1)
		hotspot =user[:-1]+'(simple-share)'
		cv2.putText(img, f"{hotspot} hotspot created"  ,(40,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1 , cv2.LINE_AA)
		cv2.putText(img, f"Receiving Files......."  ,(100,130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2 , cv2.LINE_AA)
		cv2.putText(img, f"After completion press any key to Exit"  ,(40,330), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2 , cv2.LINE_AA)
		
		#print(i)
		cv2.imshow('frame2', frame)
		flag=False
		t=threading.Thread(target=callServer, args =(q, ))	
		t.start();
				
		if cv2.waitKey():
			cv2.destroyAllWindows()
			flag=True;
		
	
		
	cap.release()
	displayFiles(q)


#function to call server for infinite times
def callServer(q):
	receivedFiles="NofilesRecived"
	while True:
		text=server()
		if not text in q.queue:
			q.put(text)
		
			
	 
#server function that receives files		
def server():
		
	try:
		# device's IP address
		SERVER_HOST = "0.0.0.0"
		SERVER_PORT = 5001
		# receive 4096 bytes each time
		BUFFER_SIZE = 4096
		SEPARATOR = "<SEPARATOR>"
		# create the server socket
		# TCP socket
		s = socket.socket()
		# bind the socket to our local address
		s.bind((SERVER_HOST, SERVER_PORT))

		# enabling our server to accept connections
		# 5 here is the number of unaccepted connections that
		# the system will allow before refusing new connections
		s.listen(1)
		print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
		# accept connection if there is any
		client_socket, address = s.accept() 

		# if below code is executed, that means the sender is connected
		print(f"[+] {address} is connected.")
		# receive the file infos
		# receive using client socket, not server socket
		received = client_socket.recv(BUFFER_SIZE).decode()
		filename, filesize = received.split(SEPARATOR)
		# remove absolute path if there is
		filename = os.path.basename(filename)
		print (filename)
		# convert to integer
		filesize = int(filesize)
		print(filesize)
		# start receiving the file from the socket
		# and writing to the file stream
		#progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
		with open('files/'+filename, "wb") as f:

			while True:

				# read 1024 bytes from the socket (receive)
				bytes_read = client_socket.recv(BUFFER_SIZE)
				if not bytes_read:    
				    # nothing is received
				    # file transmitting is done
				    break
				# write to the file the bytes we just received
				f.write(bytes_read)
				# update the progress bar
				#progress.update(len(bytes_read))

		# close the client socket
		client_socket.close()
		# close the server socket
		s.close()
		print("hello")
		#recivedFiles
		#print(receivedFiles)
		#hj=input()
		#receivedFiles = receivedFiles + ("$"+filename)
		#print("Received files = "+receivedFiles)
		#jh=input()
		return filename
		
	
	except:
		print("ERROR: NOT SENT")
		


def displayFiles(q):
	cap = cv2.VideoCapture(0)
	#while True:
	ret, frame = cap.read()
	#frame = imutils.resize(frame, height=3320)
	img = cv2.rectangle(frame, (10,6) , (630,55) , (224,78,98) , -1)
	cv2.putText(img, "Received Files"  ,(175,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2 , cv2.LINE_AA)
		
	#x=q.get().split('$')
	#img = cv2.rectangle(frame, (20,6) , (830,55) , (224,78,98) , -1)
	#cv2.putText(img, str(x)  ,(275,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2 , cv2.LINE_AA)
	i=0
	p=0
	k=0
	while(not q.empty()) :
		x=q.get().split('$')
		#prints all the retunred files
		for y in x:
			pox=((i+1)*65)+5*i
			poy=130+(70*i)
			print(pox," ",poy," ",y)
			string=(str(i+1)," ",y)
			#img = cv2.rectangle(frame, (42,pox) , (590,poy) , (247,160,140) , -1)
			if(p==0):
				cv2.putText(frame, str(k+1)+" "+y ,(75,105+(70*i)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1 )
			if(p==1):
				cv2.putText(frame, str(k+1)+" "+y ,(275,105+(70*i)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1 )
			if(p==2):
				cv2.putText(frame, str(k+1)+" "+y ,(475,105+(70*i)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1 )
			p+=1
			k+=1
			if(p==3):
				p=0
				i+=1
	#cv2.putText(img, " Chose the Option ? Then, Click Q to enter "  ,(60,105+(70*i)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0 , 255), 2 )
	cv2.putText(frame, " Want to Exit ? Then, press any key "  ,(95,105+(70*i)+50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0 , 255), 2 )

	
	cv2.imshow('frame', frame)
	if cv2.waitKey():
		cap.release()
		cv2.destroyAllWindows()
	


