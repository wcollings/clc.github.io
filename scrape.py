import os
from bs4 import BeautifulSoup as bs
import json
import re
from copy import copy

ignore_folders=[".git",".idea",".vscode","__pycache__", "js", "compilations","puirt", "soundtracks","templates","to_process"]

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

def find_language(t):
	bolds=t.find_all("b")
	for b in bolds:
		if "Language" in b.string:
			lang=b.parent.parent.next_sibling.next_sibling
			return get_html_enc_string(lang)
	return "English"

def parse_lyrics(t, num_langs):
	lyrics=[]
	col=0
	line=[]
	for td in t('td'):
		if col==0:
			if len(td.text.strip()) > 0:
				line=[get_html_enc_string(td)]
			else:
				continue
			if num_langs != 1:
				col=1
				continue
		else:
			col=0
			line.append(get_html_enc_string(td))
		lyrics.append(line)
	return lyrics

def get_innermost_elem(elem):
	next_elem=None
	for child in elem.children:
		if hasattr(child,'children'):
			next_elem=copy(child)
	if next_elem is None:
		return elem
	else:
		return get_innermost_elem(next_elem)

def get_html_enc_string(l):
	inner_child=get_innermost_elem(l)
	s=inner_child.encode(formatter='html').decode()
	start=s.find('>')+1
	stop=s.find('<',start)
	return s[start:stop].strip()
	#return l.decode('utf8').encode(formatter='html')

def read_song(f):
	s=bs(open(f, encoding='UTF-8'),'html.parser')
	contents={}
	links=s("a")
	contents["album"]=[links[3]['href'],get_html_enc_string(links[3])]
	contents["artist"]=[links[2]['href'],get_html_enc_string(links[2])]
	contents["song"]=list(links[0].parent.strings)[-1].strip()[2:]
	h=s.find("table",id='head_t')
	if 'alt' in h.img:
		contents['image']=[h.img['src'],h.img['alt']]
	else:
		contents['image']=[h.img['src']]
	contents["language"]=find_language(h)
	num_langs=1
	if contents['language'] != 'English':
		num_langs=2
	t=s.find('table',id='lyrics')
	contents['lyrics']=parse_lyrics(t,num_langs)
	return contents

def listfind(l,elem, start):
	for i in range(len(l[start:])):
		record=l[i+start]
		if record is None:
			record="None"
		if elem.search(record):
			return i+start
	return -1

def read_artist(p):
	if not os.path.exists(p):
		return {}
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
		data["members"]=m.text.strip()
		'''
		r = re.compile("\w[\w ']+")
		for mem in m.children:
			if mem==mem.string:
				if mem.string=='\n':
					continue
				data['members'].extend(r.findall(mem))
			else:
				data['members'].extend(r.findall(mem.text))
		'''
	albs = ht.find(string=re.compile("Albums"))
	albs = albs.find_next("td").contents
	date=re.compile("(\d{4}) ?-")
	data['albums']=[]
	#albs=[[j for j in i.stripped_strings] for i in albs]
	i=0
	a_str = [ a.string for a in albs]
	while i < len(albs):
		if len(a_str)==i+1 or a_str[i+1] == None:
			p=re.compile("(\d{4}) - ([\w ]+)")
			res=p.findall(a_str[i])
			d=int(res[0][0])
			name=res[0][1]
			link=None
		else:
			d=int(re.findall(date,albs[i])[0][0])
			name=re.findall(r'\w[\w ]+',albs[i+1].text)[0]
			link=albs[i+1]['href']
		data['albums'].append([d,name,link])
		i=listfind(a_str,date, i+1)
		if i==-1:
			break
		#i=a_str.find(None,i)+1
	return data

def read_album(p):
	pass

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
		rec=read_artist(dir+"/index.html")
		rec["folder"]=dir
		record.append(rec)
json.dump(record,open("record.json","w"), indent=3)
'''
of=open("chunnamise.json",'w')
f=read_song("chunnamise.html")
json.dump(f,of, indent=2)
'''