import uiautomator
import os
import subprocess
import time
import tkinter 

#__________________________________________________________________________________
def ADB_Reset():
    
    try:
        os.system('adb kill-server')
        os.system('adb start-server')    
    except:
        print('ADB CRASH')
        os._exit(0)

#__________________________________________________________________________________
#?port
def Initialize():

	SerialNumber = subprocess.getoutput('adb devices').split('\n')
	SerialNumber.remove('List of devices attached')
	d = [] #Device list 

	for i in range(len(SerialNumber) -1 ):
		SerialNumber[i] = SerialNumber[i].strip('device').strip()
		print (SerialNumber[i])
		os.system('adb -s ' + SerialNumber[i] + ' reconnect')
		port = int(i + 1000)
		d.append(uiautomator.Device(SerialNumber[i], port))
		print('Device {} is {} '.format (i , SerialNumber[i]) )
	
		print ('\nThere are {} devices in total'.format(len(d)))

	try:
		if len(d) > 1 :
			print ('\nThere are {} devices in total'.format(len(d)))
			i = int(input('Please selecet the device\n')) #兩台以上就要選
		elif len(d) ==1:
			print ('There is one device connected')
			i = 0
		else:
			print ('There are no devices connected')
			os._exit(0)
	except:
		print ('Cant selecet devices')
		os._exit(0)
    
	return i,d,SerialNumber

#__________________________________________________________________________________
#????
def Wake_Up(d,i):
	print('Unlock Screen')
	try:
		d[i].screen.on()
	except:
		pass
	try:
		d[i](resourceId="com.android.systemui:id/lock_icon").click()
	except:
		pass
#__________________________________________________________________________________
#?Call

def Call_Conduct(d,i,callnumber):
	if d[i].screen == "off":
		try:
			Wake_Up(d,i)
		except:
			pass
	
	print(callnumber.get())
	tmp = callnumber.get()
	numb=[]
	for count in range(len(tmp)):
		numb.append(tmp[count])

	#??????
	try:
		d[i](className ="android.widget.TextView", text = 'Phone').click()
	except:
		pass
		
	try:
		d[i](resourceId="com.google.android.dialer:id/fab").click()
	except:
		pass
	#????
	try:
		for number in range(len(numb)):
			d[i](resourceId="com.google.android.dialer:id/dialpad_key_number", text = numb[number]).click()
	except:
		pass
	#??
	try:
		d[i](resourceId="com.google.android.dialer:id/dialpad_floating_action_button").click() 
	except:
		pass
	#???????
	time.sleep(10)
	try:
		d[i](resourceId="com.google.android.dialer:id/incall_end_call").click()
	except:
		pass
		
	print('Call End')

#__________________________________________________________________________________

#__________________________________________________________________________________
#Display
def DisplayTab(i,d,SerialNumber):
	Display = tkinter.Tk()
	Display.geometry("150x150")
	Display.title(SerialNumber)
	
	label1=tkinter.Label(Display, text ="⎝ ◕ д ◕ ⎠", fg="red", bg="blue", font=("Ariel",12), padx = 20, pady=10)
	label1.pack()
	
	textvarSCO = tkinter.StringVar()
	textvarSCO.set("神說要有光,螢幕就亮了")
	buttonSCO=tkinter.Button(Display, textvariable=textvarSCO, command = lambda: Wake_Up(d,i), bg='LightBlue')
	buttonSCO.pack()
	
	label2=tkinter.Label(Display, text ="打電花", fg="red", bg="blue", font=("Ariel",12), padx = 20, pady=10)
	label2.pack()
	callnumber = tkinter.StringVar()
	Number = tkinter.Entry(Display, textvariable = callnumber)
	Number.pack()
	textvarCall = tkinter.StringVar()
	textvarCall.set("摳摳摳")
	buttonCall=tkinter.Button(Display, textvariable=textvarCall, command = lambda: Call_Conduct(d,i,callnumber), bg='LightBlue')
	buttonCall.pack()
	
	Display.mainloop()


if __name__ == '__main__':
	i,d,SN = Initialize() # Enable Colorama on Windows platform.	
	DisplayTab(i,d,SN)


