import os
from functools import reduce
from types import prepare_class
import dirs as d
from bs4 import BeautifulSoup as bs
from dataclasses import dataclass
import unicode

@dataclass
class entry:
	song:str=""
	slink:str=""
	artist:str=""
	arlink:str=""
	album:str=""
	allink:str=""
	notes:dict={}
	def __repr__(self):
		out="<tr>"
		out+='<td><a href="{}">{}</a></td>'.format(self.slink,format_name(self.song))
		out+='<td><a href="{}">{}</a></td>'.format(self.arlink,self.artist)
		out+='<td><a href="{}">{}</a></td>'.format(self.allink,self.album)
		if self.notes:
			out+='<td>{}</td>'.format(self.notes)
		out+='</tr>\n'
		return out

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

files=d.get_files(True)
entries={}
alphabetical=[None]*26

#Read each song file, parse it for the relevent data
for file in files:
	#there may have been clashes, this iterates through all of them
	paths=files[file]
	for path in paths:
		p=reduce(os.path.join,path.extend(file))
		s=bs(open(p))
		tb=s.body.find("table",{"id":"head_t"})
		links=s.body.find_all("a")
		temp=entry()
		temp.song=tb.find_all("td")[1].get_text()
		temp.slink=p
		temp.artist=links[2].get_text()
		temp.arlink=links[2]["href"]
		temp.album =links[3].get_text()
		temp.allink=links[3]["href"]
		if file in entries:
			entries[file].append(temp)
		else:
			entries[file]=[temp]	

#sort the list into alphabetical sublists
for entry in entries.values():
	for item in entry:
		n=unicode.unidecode(format_name(item.song)).lower()
		index=ord(n[0])-97
		alphabetical[index].append(item)
