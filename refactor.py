import os
import re
import shutil
#import linking as l


def search_dir(d):
	c_dir=os.path.join(curr_dir,d)
	files=os.listdir(c_dir)
	sorted=False
	for i in files:
		if os.path.isdir(os.path.join(c_dir,i)):
			sorted=True
	if sorted:
		return 1
	if not os.path.exists(os.path.join(c_dir,"index.html")):
		return -1
	f=open(os.path.join(c_dir,"index.html"),'r')
	lines=f.readlines()
	f.close()
	album_list=[]
	for line in lines:
		album=albumpat.findall(line)
		if album != []:
			temp=sort_album(c_dir,album[0])
			album_list.append(album[0])
	for album in album_list:
		sort_album(c_dir,album)

def sort_album(path,a):
	if not os.path.exists(os.path.join(path,a)):
		return -1
	f=open(os.path.join(path,a))
	lines=f.readlines()
	f.close()
	songs=[]
	a_name_index=a.find(".")
	a_name=a[:a_name_index]
	for line in lines:
		if songpat.search(line):
			songs.append(songpat.findall(line)[0])
	lines[10:12]=edit_links(lines[10:12])
	try:
		os.mkdir(os.path.join(path,a_name))
	except:
		pass
	shutil.move(os.path.join(path,a),os.path.join(path,a_name,a))
	coverart="{}.jpg".format(a_name)
	shutil.move(os.path.join(path,coverart),os.path.join(path,a_name,coverart))
	for song in songs:
		if os.path.exists(os.path.join(path,song)):
			process_song(path,song,a_name)


def process_song(path,song, album):
	# On line 12 (for us 11), add an extra "../" to all the links
	# on line 13 (for us 12), add an extra "../" to just the first link
	# Move to its new folder
	try:
		f=open(os.path.join(path,song), encoding='iso-8859-1')
	except:
		print("Could not find song {}, from the album {}".format(song,album))
		return
	text=f.readlines()
	f.close()
	text[10:12]=edit_links(text[10:12])
	f=open(os.path.join(path,album,song),'wb')
	for line in text:
		string=line.encode('iso-8859-1')
		f.write(string)
	f.close()
	done=True
	os.remove(os.path.join(path,song))

def edit_links(lines):
	start=lines[0].find('<')+9
	end=lines[0].find('\"',start)
	beginning=lines[0][:start]
	ending=lines[0][end:]
	mid=lines[0][start:end]
	mid="../"+mid
	lines[0]=beginning+mid+ending
	# Append to the second link
	start = lines[0].find('<', start) + 1
	start = lines[0].find('<', start) + 9
	end = lines[0].find('\"', start)
	beginning = lines[0][:start]
	ending = lines[0][end:]
	mid = lines[0][start:end]
	mid = "../" + mid
	lines[0] = beginning + mid + ending
	# append to the third link
	start = lines[1].find('<') + 9
	end = lines[1].find('\"', start)
	beginning = lines[1][:start]
	ending = lines[1][end:]
	mid = lines[1][start:end]
	mid = "../" + mid
	lines[1] = beginning + mid + ending
	return lines


structure={}
dirs=[]
albumpat=re.compile("\s+[\d?]{4} -.*\"(.*\.html)\"")
songpat=re.compile("\s+\d+\. ?<a.+\"(.*\.html)\"")
curr_dir=os.getcwd()
for files in os.listdir(curr_dir):
	if os.path.isdir(os.path.join(curr_dir, files)):
		dirs.append(files)

print("I found {} directories.".format(len(dirs)))
full_record={}
for dir in dirs:
	if dir != "__pycache__":
		search_dir(dir)