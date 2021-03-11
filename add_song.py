import os
cwd=os.getcwd()
files=os.listdir(os.path.join(cwd,"to_process"))
for file in files:
	make_html(os.path.join(cwd,"to_process",file))

def make_html(f):
	#First, read the header
	#Then read the rest
	#Check the number of "===" lines.
		#2 means its in English (or Scots)
		#3 means it's in Gaidhlig (or Gailge)
