from win10toast_persist import ToastNotifier
import time
import getpass

# define notifier
toaster = ToastNotifier() 
#tracking the positions on server queue
current_pos = 0
last_pos = 0
#bools to control execution
has_run = False
first_notificarion = False
#get log adress
user_name = getpass.getuser()
file_adress = "C:\\Users\\" + user_name + "\\AppData\Roaming\\.minecraft\\logs\\latest.log"



#shortening toaster call 
def notification():
	toaster.show_toast(message_title, 
						"Position in queue: {}".format(current_pos), 
						duration=None,
						icon_path="icon.ico")

while True:
	with open(file_adress, mode = 'r', encoding = 'utf-8') as fp:
		#grabbing the title of the message from the log
		line = fp.readline()
		while line:
			line = fp.readline()
			if 'Connecting' in line:
				break
		line = line.split(":")
		message_title = line[-1]
		
		#convert the text in the log to a usabe number, and if it fails check if the player has connected to the server
		my_lines = fp.readlines()

		try:
			current_pos = int(my_lines[-1].split(':')[-1])
		except ValueError:
			last_few = list()
			for i in range(1,10):
				last_few.append(my_lines[-i])
			if 'Connecting to the server...' in last_few: 
				#print(last_few)
				toaster.show_toast(message_title, "You are connect to the server", duration=None)
				break
		else:
			pass

	#notifies user as soon as the program starts and then goes on the conditional checks
	if first_notificarion == False:
		notification()
		first_notificarion = True

	if current_pos > 100:
		if has_run == False:
			last_pos = current_pos
			has_run = True
		if last_pos - current_pos >= 100:
			notification()
			has_run = False
		time.sleep(60)

	elif 100 >= current_pos > 10:
		if has_run == False:
			last_pos = current_pos
			has_run = True
		if last_pos - current_pos >= 10:
			notification()
			has_run = False
		time.sleep(30)

	elif current_pos <= 10 and current_pos < last_pos:
		notification()
		time.sleep(10)
		last_pos = current_pos
	time.sleep(2)
	