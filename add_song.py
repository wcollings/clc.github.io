import os
from yattag import Doc
from functools import reduce
import re


cwd=os.getcwd()
files=os.listdir(os.path.join(cwd,"to_process"))
meta={}
lyrics=[]
doc,tag,text=Doc().tagtext()

def make_html(f):
	meta["FOLDER"]=meta["ALBUM"].split(" ")[0].lower()
	#First, read the header
	#Then read the rest
	#Check the number of "===" lines.
		#2 means its in English (or Scots)
		#3 means it's in Gaidhlig (or Gailge)
	with tag("html"):
		with tag("head"):
			with tag("title"):
				text("{} - {}".format(meta["ARTIST"],meta["SONG"]))
			doc.stag("link", ("href","../../style.css"), ("rel","stylesheet"))
		with tag("body"):
			with tag("p",("align","left")):
				with tag("a",("href","../../index.html")):
					text("Celtic Lyrics Corner")
				text(">")
				with tag("a",("href","../../artists.html")):
					text("Artists & Groups")
				text(">")
				with tag("a",("href","../index")):
					text(meta["ARTIST"])
				text(">")
				with tag("a", ("href","{}.html".format(meta["FOLDER"]))):
					text(meta["ALBUM"])
				with tag("table", ("id","header")):
					doc.stag("img",src="{}.jpg".format(meta["FOLDER"]))
	print(doc.getvalue())

def make_row(s1,s2):
	with tag("tr"):
		with tag("td"):
			text(s1)
		with tag("td"):
			text(s2)


def parse_doc(f):
	inf=open(f)
	lines=[x.rstrip() for x in inf.readlines()]
	div_cnt=0
	sections=["header","lang1","lang2"]
	section_divs=[]
	section="header"
	for i in range(len(lines)):
		if "==" in lines[i]:
			div_cnt+=1
			section_divs.append(i)
	section_divs.append(len(lines)-1)
	header=parse_header(lines[:section_divs[0]])
	lyrics.append(lines[section_divs[0]+1:section_divs[1]])
	lyrics[0].insert(0,"<b><u>Lyrics:</u></b>")
	if div_cnt ==2:
		lyrics.append(lines[section_divs[1]+1:])
		lyrics[1].insert(0,"<b><u>English Translation:</u></b>")
		
def parse_header(lines):
	strip=re.compile('(\w+)="(.*)"')
	for line in lines:
		results=strip.search(line)
		k=results.group(1)
		v=results.group(2)
		meta[k]=v


for file in files:
	parse_doc(reduce(os.path.join,[cwd,"to_process",file]))
	make_html(os.path.join(cwd,"to_process",file))
