import os
import re
import beautifulsoup as bs

def finalize_links(path, album):
	# read through each file in the folder
	# parse each file for its links
	# update the links as necessary
	a_name_index = album.find(".")
	a_name = album[:a_name_index]
	c_dir = os.path.join(path, a_name)
	files = os.listdir(c_dir)
	for file in files:
		parse_file(os.path.join(path, a_name, file))


def parse_file(path):
	link_pat = re.compile("(<a href=\".+?)\"")
	lines = open(path).readlines()
	for i in range(len(lines)):
		for match in link_pat.finditer(lines[i]):
			fname = lines[i][match.span()[0] + 9:match.span()[1]]
			if not os.path.exists(fname):
				done = True

def search_dirs(path, fname):
	#4 cases:
	# it's the index page, in which case the albums are found in their own directory now
	# it's by the same artist, in which case it's probably in a sister directory
	# it's by a different artist, but still in the artists list, in which case:
	#   head down 1 more directory
	#   append the album folder again

	#testing case 1
	if not "\\" in fname:

	if fname.startswith("../"):
		fname=fname[3:]
	p, dir = os.path.split(path)
	folders = [dir]
	while dir != "Celtic Lyrics Corner":
		p, dir = os.path.split(p)
		folders.append(dir)

def split_path(path):
	if "\\" in path:
		delim="\\"
	else:
		delim="/"
	folders=[]
	while path:
		i=path.find(delim)
		if i is not None:
			folders.append(path[:i])
			if path[i+1]==delim:
				i+=1
			path=path[i:]
		else:
			folders.append(path)
			return folders

def parse_dir(d):
	r={}
	subfolders=False
	for file in os.listdir(d):
		if os.path.isdir(os.path.join(d,file)):
			r[file]=parse_dir(os.path.join(d,file))
			subfolders=True
	if not subfolders:
		s=[]
		for file in os.listdir(d):
			if os.path.isfile(os.path.join(d,file)):
				s.append(file)
		return s
	return r

def find_all(key, d):
	keys=split_path(key)

def find_key(key,d):
	l=[]
	for v in d:
		if d[v] is dict:
			p=find_key(key,d[v])
			if p is not None:
				l.append(p)

		elif key in d[v]:
			return v
		else:
			return None
	if len(l)==0:
		return None
	else:
		return l