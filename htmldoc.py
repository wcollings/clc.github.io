from bs4 import BeautifulSoup as bs
import os
import globals as g
import json
from functools import reduce

class htmldoc:
	def __init__(self, file, format="ISO-8859-1"):
		self.originalFile=file
		self.skip=False
		try:
			self.soup=bs(open(file,'r', encoding=format),'html.parser')
			cleaned=self.soup.find("cleaned")
			#if cleaned is not None:
				#self.skip=True
			self.title=self.soup.title
			if "404" in self.title.string:
				self.skip=True
		except:
			self.skip=True
			g.failed_files.append(file)
			return

	'''
		Functions relating to cleaning the shit that was this HTML when I got it
	'''
	def clean(self):
		"""
			Runs all "cleaning" functions:
			Makes the document CSS-compliant
			Cleans the header table
			Cleans the lyrics table
			Cleans the nested "table-row-col-table-row-col-table-row-col-center" bullshit
		"""
		if self.skip:
			return
		#Fix the body tag
		b=self.soup.body
		if "link" in b.attrs:
			del b["link"]
		if "alink" in b.attrs:
			del b["alink"]
		if "vlink" in b.attrs:
			del b["vlink"]
		if "bgcolor" in b.attrs:
			del b["bgcolor"]
		self.clean_bloat()
		self.clean_header()
		self.clean_lyrics()
		self.purge()

	def clean_header(self):
		"""
			Cleans the header table, makes it CSS-compliant
			Also gets rid of all the extra row-column pairs used only for spacing
		"""
		head_t=self.soup.find("table",attrs={"border":"3","bordercolordark":"#000080"})
		if not head_t:
			return
		for div in head_t.find_all("div"):
			div.unwrap()
		attrs=['border','bordercolor','bordercolordark','bordercolorlight','cellpadding','cellspacing','width']
		for attr in attrs:
			del head_t[attr]
		head_t["id"]="head_t"
		if not head_t.find("table"):
			return
		head_t.find("table").unwrap()
		attrs=["valign","align","width"]
		for td in head_t.find_all("td",attrs={"width":"20%"}):
			del td["align"]
			del td["valign"]
			del td["width"]
			td["id"]="lc"
		for td in head_t.find_all("td",attrs={"width":"80%"}):
			del td["align"]
			del td["valign"]
			del td["width"]
		for td in head_t.find_all("td"):
			if td.find("tr") is not None:
				p=td.parent
				td.unwrap()
				p.unwrap()

	def clean_lyrics(self):
		"""
			Cleans the lyrics table, makes it CSS-compliant
			Also gets rid of all the extra row-column pairs used only for spacing
		"""
		lyrics_t=self.soup.find("table",attrs={"border":"0","width":"90%"})
		if not lyrics_t:
			return
		attrs=["border","cellpadding", "cellspacing", "width"]
		for attr in attrs:
			del lyrics_t[attr]
		lyrics_t["id"]="lyrics"
		for td in lyrics_t("td"):
			del td["align"]
			del td["width"]
	#So many tags that didn't need to be there...
	def clean_bloat(self):
		tl=[self.soup("font"), self.soup("em"),self.soup("center")]
		if tl[0]:
			for font in tl[0]:
				font.unwrap()
		if tl[1]:
			for em in tl[1]:
				em.unwrap()
		if tl[2]:
			for cent in tl[2]:
				cent.unwrap()
	
	#this process left a fair number of useless tags sitting around, on top of them being there to begin with.
	# This just goes through and deletes any tags that should have contents but don't.
	def purge(self):
		done=False
		elem_ignore=["link","img","br"]
		while not done:
			done=True
			for elem in self.soup.find_all():
				if elem.name in elem_ignore:
					continue
				#if len(elem.contents)==1 and elem.contents[0]=="\n":
				if all([ x== "\n" for x in elem.contents]):
					done=False
					elem.extract()

	def update_links(self):
		if self.skip:
			return
		split_path=g.splitall(self.originalFile)
		path_home="../"*(len(split_path)-2)
		links=self.soup.find_all("a")
		links[0]["href"]=path_home+"index.html"
		if "Artists" in links[1].get_text():
			links[1]["href"]=path_home+"artists.html"

		if self.ftype == "song":
			album=links[3]["href"]
			album=album[:album.find(".html")]
			for link in links[5:]:
				#If this is an external link, we don't worry about it
				if "http" in link.attrs["href"]:
					continue
				new_path=g.find_path(link["href"],album)
				if new_path==-1:
					g.links_f.write('"{}" in file "{}"\n'.format(link["href"], self.originalFile))
				else:
					temp="../../"+new_path
					
				#g.links_f.write('"{}"->"{}"'.format(link["href"],g.find_path(link["href"], album)))
			#return
		elif self.ftype == "album":
			# If there aren't 3 links, that means it's a compilation or a Puirt. But they do exist, so we need to
			# handle them
			if len(links) > 2:
				links[2]["href"]="../index.html"
		elif self.ftype == "artist":
			for link in links[2:]:
				if "../" not in link["href"]:
					link["href"]=self.update_album(link["href"])
		elif self.ftype=="songlist":
			self.update_root()

	def update_root(self):
		for row in self.soup.body.find_all("tr"):
			cols=row.find_all("td")
			if not cols[0].find("a"):
				continue
			
			#the first link is the song
			#	update the song link, but strip off the "../.../" as that will fuck things up
			new_path=g.find_path(cols[0].a["href"], )
			new_path=g.splitall(new_path)
			cols[0].a["href"]=reduce(os.path.join,new_path[2:])
			test=False
			#the second link is the artist -- it doesn't need to be updated
			#the third link is the album -- if it's a compilation it doesn't need updating
			if cols[2].a is not None:
				if not "compilation" in cols[2].a["href"]:
					new_path=g.splitall(g.find_path(cols[2].a["href"]))
					new_path[1]="."
					cols[2].a["href"]=reduce(os.path.join, new_path[2:])
			if len(cols) <4:
				continue
			for link in cols[3].find_all("a"):
				new_path=g.splitall(g.find_path(link["href"]))
				link["href"]=reduce(os.path.join,new_path[2:])


	def update_album(self,an):
		dir,fn=os.path.split(an)
		return "{}/{}".format(fn[:fn.find(".html")],fn)
	def insert_css(self, link):
		if self.skip:
			return
		if self.soup.head.find("link"):
			self.soup.head.link["href"]=link
			return
		new_tag=self.soup.new_tag("link",rel="stylesheet",href=link)
		self.soup.head.append(new_tag)
	#Now we're getting into functions to build the page if it doesn't yet exist

	def write(self,file=None):
		if self.skip:
			return
		cleaned=self.soup.new_tag("cleaned")
		self.soup.body.append(cleaned)
		try:
			if file != None:
				fp=open(file,'w')
			else:
				os.remove(self.originalFile)
				fp=open(self.originalFile,'w')
			self.soup.smooth()
			fp.write(self.soup.prettify(formatter='html'))
			fp.close()
		except FileNotFoundError:
			print("I couldn't find a file called {}".format(self.originalFile))
		except UnicodeEncodeError as ue:
			print(ue.object[ue.start:ue.end])
			print("Error in file: {}".format(self.originalFile))
			print("The encoding happened because of an encoding error: {}".format(ue.encoding))


if __name__=="__main__":
	g.failed_files=[]
	files=[
		"songlist-a.html",
		"songlist-a_1.html",
		"songlist-b.html",
		"songlist-c.html",
		"songlist-d.html",
		"songlist-e.html",
		"songlist-f.html",
		"songlist-g.html",
		"songlist-h.html",
		"songlist-i.html",
		"songlist-j.html",
		"songlist-l.html",
		"songlist-m.html",
		"songlist-n.html",
		"songlist-o.html",
		"songlist-p.html",
		"songlist-qr.html",
		"songlist-s.html",
		"songlist-t.html",
		"songlist-uv.html",
		"songlist-w.html",
		"songlist-y.html"]
	g.all_files=json.load(open("dir_struct.json",'r'))
	for file in files:
		h=htmldoc(file)
		h.ftype="songlist"
		h.update_links()
		h.write()
	print(g.failed_files)
