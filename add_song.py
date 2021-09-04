import os
from yattag import Doc
from functools import reduce
from bs4 import BeautifulSoup as bs
import re
import dirs
import sys


files=os.listdir("to_process")
meta={}
lyrics=[]
dir_s=dirs.get_folders()
doc,tag,text=Doc().tagtext()
if len(sys.argv) > 1:
	files=sys.argv[1:]

def make_html(f):
	"""
		Generate the actual HTML page for this song
	"""
	lines=open("templates/song.html",'r').readlines()
	# Parse the template, replacing the parts that need to be replaced
	artist=re.compile("@@ARTIST")
	album=re.compile("@@ALBUM")
	song=re.compile("@@TITLE")
	alb_l=re.compile("@@ALB_LINK")
	for i in range(len(lines)):
		lines[i]=artist.sub(meta["ARTIST"],lines[i])
		lines[i]=album.sub(meta["ALBUM"],lines[i])
		lines[i]=song.sub(meta["SONG"],lines[i])
		lines[i]=alb_l.sub(meta["ALB_LINK"],lines[i])
		lines[i]=add_credits(lines[i])
		lines[i]=add_language(lines[i])
		lines[i]=add_lyrics(lines[i])

	#if a song with this filename exists, prompt
	print("Writing to file: {}".format(meta["writepath"]))
	if os.path.exists(meta["writepath"]):
		temp=input("WARNING: this file already exists. Overwright? (y/n)\n>")
		if not (temp=="y" or temp=="Y"):
			return -1
	f=open(meta["writepath"],'w',encoding="UTF-8")

	#now save that
	soup=bs("".join(lines), 'html.parser')
	soup.smooth()
	f.write(soup.prettify(formatter="html"))
	f.close()

	#helpful prompt if no album index file exists
	if not os.path.exists(reduce(os.path.join,[meta["ART_LINK"],meta["ALB_LINK"],meta["ALB_LINK"]+".html"])):
		print("Please note that there isn't an index file for {} yet, so it would help to make that".format(meta["ALBUM"]))

	#helpful prompt if no artist index file exists
	if meta["ART_LINK"] != "." and not os.path.exists(os.path.join(meta["ART_LINK"],"index.html")):
		print("Plese note that there isn't an index file for {} yet, so it would help to make that".format(meta["ARTIST"]))
	return 1

def add_credits(line):
	"""
		If the "credits" signature is on this line, replace it. Otherwise return it unchanged
	"""
	credits=re.compile("@@CREDITS")
	if credits.search(line):
		if "CREDITS" in meta:
			return credits.sub(meta["CREDITS"],line)
		else:
			return ""
	else:
		return line

def add_language(line):
	"""
		If the "language" signature is on this line, replace it. Otherwise return it unchanged
	"""
	language=re.compile("@@LANGUAGE")
	if language.search(line):
		if "LANGUAGE" in meta:
			return language.sub(meta["LANGUAGE"],line)
		else:
			return ""
	else:
		return line
	
def convert_characters(line):
	"""
		Replace shorthand accent marks with real accent marks, and replace funky 
		UTF-8 quotation marks with standard quotation marks
	"""
	char_map={
		"\\`a":"&agrave;", "\\'a":"&aacute;", "\\^a":"&acirc;",
		"\\`A":"&Agrave;", "\\'A":"&Aacute;", "\\^A":"&Acirc;",

		"\\`e":"&egrave;", "\\'e":"&eacute;", "\\^e":"&ecirc;",
		"\\`E":"&Egrave;", "\\'E":"&Eacute;", "\\^e":"&Ecirc;",

		"\\`i":"&igrave;", "\\'i":"&iacute;", "\\^i":"&icirc;",
		"\\`I":"&Igrave;", "\\'I":"&Iacute;", "\\^I":"&Icirc;",

		"\\`o":"&ograve;", "\\'o":"&oacute;", "\\^o":"&ocirc;",
		"\\`O":"&Ograve;", "\\'O":"&Oacute;", "\\^O":"&Ocirc;",

		"\\`u":"&ugrave;", "\\'u":"&uacute;", "\\^u":"&ucirc;",
		"\\`U":"&Ugrave;", "\\'U":"&Uacute;", "\\^U":"&Ucirc;",

		"“":"\"", "”":"\"","’":"\'"
	}
	for key in char_map:
		while (pos:=line.find(key)) != -1:
			line=line[:pos]+char_map[key]+line[pos+len(key):]
	return line
	
def add_lyrics(line):
	"""
		Parse and process the lyrics. There can be one or two columns, and some handy "tagging" features as well
	"""
	lyrics_l=re.compile("@@LYRICS")
	if not lyrics_l.search(line):
		return line
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
			make_row([line])
		return

	# if they're the same length, there's not a weird edge case to deal with
	if len(lyrics[0])==len(lyrics[1]):
		for l1,l2 in zip(lyrics[0][1:],lyrics[1][1:]):
			make_row([l1,l2])
		return "".join(doc.getvalue())

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
		
		#and then just print the line (or lines)
		if print_both:
			make_row([lyrics[0][i+1],lyrics[1][l1]])
			l1+=1
		else:
			make_row([lyrics[0][i+1]])
	return "".join(doc.getvalue())
	
def make_row(lines):
	"""
	Format the raw lyrics, in *line* 
	"""
	with tag("tr"):
		for line in lines:
			with tag("td"):
				if line=="":
					doc.asis("&nbsp;")
				else:
					doc.asis(line)

unknown_art_str="I couldn't find a folder for artist {}. If this artist already has a folder, enter the artist and album folder names with a space between them below. Otherwise just hit enter.\n>"
unknown_alb_str="I couldn't find an album folder named {}. If this album does exist, enter the folder name. Otherwise, just hit enter\n>"
def set_file_properties():
	"""
		process and verify the pre-processed path

		Whereas set_path only parses strings, this then checks to make sure those folders exist, and determines the final path
	"""
	meta["path"]=[]
	#if the artist or album folder provided are "root", skip the rest of this and just use that
	if meta["ART_LINK"]=="." or meta["ALB_LINK"]==".":
		meta["path"]=["."]

	#"path" is the path, from root to the song itself.
	# if the artist folder we were given does exist, throw that on the stack first
	elif meta["ART_LINK"] in dir_s:
		meta["path"].append(meta["ART_LINK"])

		#then get a slice of the directory structure, pulling just the artist's subfolders
		temp=dir_s[meta["ART_LINK"]]

		#extract the album name and check if it exists
		album=meta["ALB_LINK"]
		if album in temp:
			meta["path"].append(album)
		# if it doesn't exist, prompt for that
		else:
			temp=input(unknown_alb_str.format(meta["ALB_LINK"]))
			if temp=="":
				meta["path"]=["."]
	else:
		# if the artist folder doesn't exist, prompt for both the artist and album
		temp=input(unknown_art_str.format(meta["ART_LINK"].lower()))
		if temp=="":
			meta["path"]=["."]
		else:
			meta["path"].append(temp.split(" "))
				
	meta["path"].append(str(meta["SONG_LINK"]))
	#smoosh the whole path into a single string
	meta["writepath"]=reduce(os.path.join,meta["path"])

def set_paths():
	"""
		pre-process the file path

		I've given an option to specify the relevent folder/file name in the same record as the metadata record. This just
		checks if they've taken advantage of that, and sets the needed fields if so.
	"""
	if "ALB_LINK" not in meta:
		if "{" in meta["ALBUM"]:
			al=meta["ALBUM"]
			#this is an ugly way of writing "all the characters that are inside the curly braces, but lowercase"
			meta["ALB_LINK"]=al[al.find("{")+1:al.find("}")].lower()
			meta["ALBUM"]=al.replace("{","").replace("}","")
		# if they haven't specified an album by either a dedicated ALB_LINK field or by this, my only guess is 
		# to take the first word of the album name, and use that.
		else:
			meta["ALB_LINK"]=meta["ALBUM"].split(" ")[0].lower()
	# artists work the same, but with different fields
	if "ART_LINK" not in meta:
		if "{" in meta["ARTIST"]:
			ar=meta["ARTIST"]
			meta["ART_LINK"]=ar[ar.find("{")+1:ar.find("}")].lower()
			meta["ARTIST"]=ar.replace("{","").replace("}","")
		else:
			meta["ART_LINK"]=meta["ARTIST"].split(" ")[0].lower()
	# if they didn't specify a filename for the song, assume they want it to be the same as
	# the filename that the unformatted song lyrics are in
	if "SONG_LINK" not in meta:
		if "{" in meta["SONG"]:
			song=meta["SONG"]
			meta["SONG_LINK"]=song[song.find("{")+1:song.find("}")].lower()+".html"
			meta["SONG"]=song.replace("{","").replace("}","")
			while (pos:=meta["SONG_LINK"].find("\\")) != -1:
				meta["SONG_LINK"]=meta["SONG_LINK"][:pos]+meta["SONG_LINK"][pos+1]
				#line=line[:pos]+char_map[key]+line[pos+len(key):]
		else:
			_,s=os.path.split(meta["FNAME"])
			meta["SONG_LINK"]=s[:-3]+"html"

def parse_doc(f):
	inf=open(f, encoding="UTF-8")
	lines=[x.rstrip() for x in inf.readlines()]
	#there can be 2-3 sections in the provided file:
	# the metadata information,
	# the lyrics in one language, and (potentially)
	# the lyrics in a second language (english)
	#the sections are divided up by some number of '====' on their own line
	sections=["header","lang1","lang2"]
	section_divs=[]
	div_cnt=0
	section="header"
	meta["FNAME"]=f
	#this just goes through a finds the line numbers for the divs. For reasons, the last line needs to be pushed
	# onto the stack as well
	for i in range(len(lines)):
		if "==" in lines[i]:
			div_cnt+=1
			section_divs.append(i)
	section_divs.append(len(lines))
	#take the section between the first div markers as the header
	parse_header(lines[:section_divs[0]])
	#the next section is the first set of lyrics
	lyrics.append(lines[section_divs[0]+1:section_divs[1]])
	#put a title line into the lyrics table
	lyrics[0].insert(0,"<b><u>Lyrics:</u></b>")

	#process the (optional) second set of lyrics, same as the first
	if div_cnt ==2:
		lyrics.append(lines[section_divs[1]+1:])
		lyrics[1].insert(0,"<b><u>English Translation:</u></b>")
			
def parse_header(lines):
	"""
		Take the key-value pairs from the header of the document and parse them into our dict
	"""
	strip=re.compile('(\w+)="(.*)"')
	for line in lines:
		# the metadata section is already in key-value pairs, just extract them from that format
		# and put them into a dict
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
