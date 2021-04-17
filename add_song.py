import os
from yattag import Doc
from functools import reduce
from bs4 import BeautifulSoup as bs
import re
import json
import dirs


files=os.listdir("to_process")
meta={}
lyrics=[]
dir_s=dirs.get_folders()
doc,tag,text=Doc().tagtext()

def make_html(f):
	artist=re.compile("@@ARTIST")
	album=re.compile("@@ALBUM")
	song=re.compile("@@TITLE")
	alb_l=re.compile("@@ALB_LINK")
	language=re.compile("@@LANGUAGE")
	lines=open("templates/song.html",'r').readlines()
	for i in range(len(lines)):
		lines[i]=artist.sub(meta["ARTIST"],lines[i])
		lines[i]=album.sub(meta["ALBUM"],lines[i])
		lines[i]=song.sub(meta["SONG"],lines[i])
		lines[i]=alb_l.sub(meta["ALB_LINK"],lines[i])
		lines[i]=add_credits(lines[i])
		lines[i]=add_language(lines[i])
	format_lyrics()
	lyrics="".join(doc.getvalue())
	lyrics_line=0
	pos=68
	lines.insert(pos,lyrics)
	print("Writing to file: {}".format(meta["writepath"]))
	if os.path.exists(meta["writepath"]):
		temp=input("WARNING: this file already exists. Overwright? (y/n)\n>")
		if not (temp=="y" or temp=="Y"):
			return -1
	f=open(meta["writepath"],'w')

	soup=bs("".join(lines), 'html.parser')
	soup.smooth()
	f.write(soup.prettify())
	f.close()
	if not os.path.exists(reduce(os.path.join,[meta["ART_LINK"],meta["ALB_LINK"],meta["ALB_LINK"]+".html"])):
		print("Please note that there isn't an index file for {} yet, so it would help to make that".format(meta["ALBUM"]))
	if meta["ART_LINK"] != "." and not os.path.exists(os.path.join(meta["ART_LINK"],"index.html")):
		print("Plese note that there isn't an index file for {} yet, so it would help to make that".format(meta["ARTIST"]))
	return 1

	#First, read the header
	#Then read the rest
	#Check the number of "===" lines.
		#2 means its in English (or Scots)
		#3 means it's in Gaidhlig (or Gailge)
def add_credits(line):
	credits=re.compile("@@CREDITS")
	if credits.search(line):
		if "CREDITS" in meta:
			return credits.sub(meta["CREDITS"],line)
		else:
			return ""
	else:
		return line
def add_language(line):
	language=re.compile("@@LANGUAGE")
	if language.search(line):
		if "LANGUAGE" in meta:
			return language.sub(meta["LANGUAGE"],line)
		else:
			return ""
	else:
		return line
	

def convert_characters(line):
	char_map={
		"\\`a":"à", "\\'a":"á", "\\^a":"â",
		"\\`A":"À", "\\'A":"Á", "\\^A":"Â",

		"\\`e":"è", "\\'e":"é", "\\^e":"ê",
		"\\`E":"È", "\\'E":"É", "\\^E":"Ê",

		"\\`i":"ì", "\\'i":"í", "\\^i":"î",
		"\\`I":"Ì", "\\'I":"Í", "\\^I":"Î",

		"\\`o":"ò", "\\'o":"ó", "\\^o":"ô",
		"\\`O":"Ò", "\\'O":"Ó", "\\^O":"Ô",

		"\\`u":"ù", "\\'u":"ú", "\\^u":"û",
		"\\`U":"Ù", "\\'U":"Ú", "\\^U":"Û"
	}
	for key in char_map:
		while (pos:=line.find(key)) != -1:
			line=line[:pos]+char_map[key]+line[pos+3:]
	return line
	
def format_lyrics():
	#First we're gonna convert the accent mark characters if they need it
	#if there are more than 1 column, the second will be in English regardless
	for i in range(len(lyrics[0])):
		lyrics[0][i]=convert_characters(lyrics[0][i])
	newp=False
	# The first line is the "Lyrics:"/"Translation:" line. It's already been set, so write it literally
	with tag("tr"):
		for i in range(len(lyrics)):
			with tag("td"):
				doc.asis(lyrics[i][0])

	#If there's only 1 column, just print that one and skip over all the ugliness following
	if len(lyrics)==1:
		for line in lyrics[0][1:]:
			if line=="":
				newp=True
				continue
			make_row([line], newp)
			newp=False
		return

	# if they're the same length, there's not a weird edge case to deal with
	if len(lyrics[0])==len(lyrics[1]):
		for l1,l2 in zip(lyrics[0][1:],lyrics[1][1:]):
			if l1=="":
				newp=True
				continue
			make_row([l1,l2], newp)
			newp=False
		return

	tag_r=re.compile("(!.*?) ")
	tags={}
	res=None

	#First, parse through the shorter (translation) column, finding the tags and saving them
	for i in range(len(lyrics[1])-1):
		if res:=tag_r.match(lyrics[1][i+1]):
			#save the tag and location
			tags[res.group()]=i+1
			#and then delete it from the document
			lyrics[1][i+1]=tag_r.sub("",lyrics[1][i+1])

	print_both=False
	# iterate through the first set of lyrics
	for i in range(len(lyrics[0])-1):
		#if you find a tag
		if res:=tag_r.match(lyrics[0][i+1]):
			#find its pair (hoping it exists)
			if res.group() in tags:
				print_both=True
				l1=tags[res.group()]
			else:
				print("Error! Unmatched lyrics tag {}!".format(res.group()))
			
			#remove the tag
			lyrics[0][i+1]=tag_r.sub("",lyrics[0][i+1])
		
		#newlines show up as "", but putting a blank table row does nothing. This is a (kinda clunky) workaround
		if lyrics[0][i+1]=="":
			print_both=False
			newp=True
			continue

		#and then just print the line (or lines)
		if print_both:
			make_row([lyrics[0][i+1],lyrics[1][l1]], newp)
			l1+=1
		else:
			make_row([lyrics[0][i+1]], newp)
		newp=False
	
	

def make_row(lines, newp=False):
	with tag("tr"):
		for line in lines:
			if newp:
				with tag("td", id="newpara"):
					if line[0]=="@":
						doc.asis(line[1:])
					else:
						text(line)
			else:
				with tag("td"):
					if line[0]=="@":
						doc.asis(line[1:])
					else:
						text(line)

def set_file_properties():
	meta["path"]=[]
	if meta["ART_LINK"]=="." or meta["ALB_LINK"]==".":
		meta["path"]=["."]
	elif meta["ART_LINK"] in dir_s:
		meta["path"].append(meta["ART_LINK"])
		temp=dir_s[meta["ART_LINK"]]
		album=meta["ALB_LINK"]
		if album in temp:
			meta["path"].append(album)
		else:
			temp=input("I couldn't find an album folder named {}. If this album does exist,\
			 enter the folder name. Otherwise, just hit enter".format(meta["ALB_LINK"]))
			if temp=="":
				meta["path"]=["."]
	else:
		temp=input("I couldn't find a folder for artist {}. If this artist already has a folder, enter the artist and album folder\
			names with a space between them below. Otherwise just hit enter.".format(meta["ART_LINK"].lower()))
		if temp=="":
			meta["path"]=["."]
		else:
			meta["path"].append(temp.split(" "))
				
	#meta["ALB_LINK"]="@@ALBUM INDEX NAME@@"
	meta["path"].append(str(meta["SONG_LINK"]))
	meta["writepath"]=reduce(os.path.join,meta["path"])

def set_paths():
	if "ALB_LINK" not in meta:
		if "{" in meta["ALBUM"]:
			al=meta["ALBUM"]
			meta["ALB_LINK"]=al[al.find("{")+1:al.find("}")].lower()
			meta["ALBUM"]=al.replace("{","").replace("}","")
		else:
			meta["ALB_LINK"]=meta["ALBUM"].split(" ")[0].lower()
	if "ART_LINK" not in meta:
		if "{" in meta["ARTIST"]:
			ar=meta["ARTIST"]
			meta["ART_LINK"]=ar[ar.find("{")+1:ar.find("}")].lower()
			meta["ARTIST"]=ar.replace("{","").replace("}","")
		else:
			meta["ART_LINK"]=meta["ARTIST"].split(" ")[0].lower()
	if "SONG_LINK" not in meta:
		_,s=os.path.split(meta["FNAME"])
		meta["SONG_LINK"]=s[:-3]+"html"

def parse_doc(f):
	inf=open(f, encoding="UTF-8")
	lines=[x.rstrip() for x in inf.readlines()]
	div_cnt=0
	sections=["header","lang1","lang2"]
	section_divs=[]
	section="header"
	meta["FNAME"]=f
	for i in range(len(lines)):
		if "==" in lines[i]:
			div_cnt+=1
			section_divs.append(i)
	section_divs.append(len(lines))
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
		v=convert_characters(results.group(2))
		meta[k]=v
	set_paths()
	set_file_properties()


cwd=os.getcwd()
for file in files:
	parse_doc(reduce(os.path.join,[cwd,"to_process",file]))
	result=make_html(os.path.join(cwd,"to_process",file))
	lyrics=[]
	meta={}
	doc,tag,text=Doc().tagtext()
	#os.remove(reduce(os.path.join,[cwd,"to_process",file]))
	meta={}
