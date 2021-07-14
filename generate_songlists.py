import os
import re
import unicodedata
from functools import reduce
from types import prepare_class
import dirs as d
from bs4 import BeautifulSoup as bs
from dataclasses import dataclass

class entry:
	def __init__(self):
		pass
	def __repr__(self):
		slink="{}/{}/{}.html".format(self.arlink,self.allink,self.slink)
		alink="{}/{}/{}.html".format(self.arlink,self.allink,self.allink)
		out="<tr>"
		out+='<td><a href="{}">{}</a></td>'.format(slink,format_name(self.song))
		out+='<td><a href="{}">{}</a></td>'.format(self.arlink,self.artist)
		out+='<td><a href="{}">{}</a></td>'.format(alink,self.album)
		if self.notes:
			out+='<td>{}</td>'.format(self.notes)
		out+='</tr>\n'
		return out

	def __hash__(self):
		return self.slink

	def parse(self,line):
		s=bs(line,'html.parser')
		links=s.find_all("a")
		self.slink=links[0]["href"]
		self.song=links[0].get_text()
		self.arlink=links[1]["href"]
		self.artist=links[1].get_text()
		self.allink=links[2]["href"]
		self.album=links[2].get_text()
		
	def __eq__(self, e):
		same=False
		if e.slink==self.slink:
			same=True
		if e.arlink==self.arlink:
			same=True
		return same

def format_name(n):
	if n.startswith("The"):
		return n[:4]+", The"
	else:
		return n

def nstrip(s):
	bad=re.compile("[\n\t >]*(.+)[\n\t ]*")
	return bad.match(s).groups()[0]

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

files=d.get_files(True)
entries={}
alphabetical=[None]*26

#Read each song file, parse it for the relevent data
for file in files:
	#there may have been clashes, this iterates through all of them
	paths=files[file]
	for path in paths:
		path.append(file)
		p=reduce(os.path.join,path)
		s=bs(open(p))
		links=s.p.find_all("a")
		strs=[]
		for string in s.p.strings:
			strs.append(string)
		temp=entry()
		temp.arlink=links[2]["href"]
		temp.artist=nstrip(strs[5])
		temp.allink=links[3]["href"]
		temp.album =nstrip(strs[7])
		temp.slink =file
		temp.song  =nstrip(strs[-1])
		if file in entries:
			entries[file].append(temp)
		else:
			entries[file]=[temp]	

#sort the list into alphabetical sublists
for entry in entries.values():
	for item in entry:
		n=remove_accents(format_name(item.song)).lower()
		index=ord(n[0])-97
		alphabetical[index].append(item)

ofp=open("songs_a_test.html", "w")
for item in alphabetical[0]:
	ofp.write(item)
ofp.close()	