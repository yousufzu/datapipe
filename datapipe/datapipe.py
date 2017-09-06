import multiprocessing as mp

def new_process(classname, email):
	print('In a new process! Yay!')
	

def start_job(classname, email):
	# Fork off a new process. Make sure this returns quickly.
	mp.Process(target=new_process, args=(classname, email)).start()
	
