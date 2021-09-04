import os
from bs4 import BeautifulSoup as bs
import json
import re

ignore_folders=[".git",".idea",".vscode","__pycache__", "js"]

def walk(top, maxdepth):
	dirs, nondirs = [], []
	for entry in os.scandir(top):
		(dirs if entry.is_dir() else nondirs).append(entry.path)
	yield top, dirs, nondirs
	if maxdepth > 1:
		for path in dirs:
			for x in walk(path, maxdepth-1):
				yield x

def extract_albums(l):
	num=re.compile("\d{4} ?-")
	indices=[]
	for i in range(len(l)):
		if num.search(l[i]):
			indices.append(i)
	albs=[]
	for i in range(len(indices)):
		date=l[indices[i]]
		name=""
		link=""
		#If there's a link, it's going to take up at least 2 more lines
		if indices[i+1] > 2 + indices[i]:
			bad=l[indices[i+1]]



def read_artist(p):
	s=bs(open(p), 'html.parser')
	ht=s.find(id='head_t')
	data={}
	data['image']=ht.find('img')['src']
	data['artist']=ht.find('img')['alt']
	m=ht.find(string=re.compile("Members"))
	# extract the member list, if it exists
	if m is not None:
		data['members']=[]
		m=m.find_next("td")
		r = re.compile("\w[\w ]+")
		for mem in m.children:
			if mem==mem.string:
				if mem.string=='\n':
					continue
				data['members'].extend(r.findall(mem))
			else:
				data['members'].extend(r.findall(mem.text))
	albs = ht.find(string=re.compile("Albums"))
	albs = albs.find_next("td").contents
	date=re.compile("\d{4} ?-")
	data['albums']=[]
	#albs=[[j for j in i.stripped_strings] for i in albs]
	i=0
	while i < len(albs):
		date=re.findall(r'\d+',albs[i])[0]
		name=re.findall(r'\w[\w ]+',albs[i+1].text)[0]
		data['albums'].append([date,name,albs[i+1]['href']])
		i=albs.index("<br/>",i)+1
	return data

record=[]
file=""
ignore=False
for root,dirs,files in walk(".", 1):
	for dir in dirs:
		ignore = False
		for bad in ignore_folders:
			if bad in dir:
				ignore=True
				break
		if ignore==True:
			continue
		print(dir)
		record.append(read_artist(dir+"\index.html"))
print(record)