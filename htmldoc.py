from bs4 import BeautifulSoup as bs
import os
import globals as g

class htmldoc:
	def __init__(self, file):
		self.originalFile=file
		self.bad=False
		try:
			self.soup=bs(open(file,'r', encoding="ISO-8859-1"),'html.parser')
			self.title=self.soup.title
			if "404" in self.title.string:
				self.bad=True
		except:
			self.bad=True
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
		if self.bad:
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
		if self.bad:
			return
		self.update=[]
		links=self.soup.find_all("a")
		if self.ftype == "song":
			links[0]["href"]="../../index.html"
			links[1]["href"]="../../artists.html"
			album=links[3]["href"]
			album=album[:album.find(".html")]
			for link in links[5:]:
				#If this is an external link, we don't worry about it
				if "http" in link.attrs["href"]:
					continue
				new_path=g.find_path(link["href"],album)
				if new_path==-1:
					g.links_f.write("{} in file {}\n".format(link["href"], self.originalFile))
				else:
					link["href"]=g.find_path(link["href"], album)
				#g.links_f.write('"{}"->"{}"'.format(link["href"],g.find_path(link["href"], album)))
			#return
		elif self.ftype == "album":
			links[0]["href"]="../../index.html"
			links[1]["href"]="../../artists.html"
			# If there aren't 3 links, that means it's a compilation or a Puirt. But they do exist, so we need to
			# handle them
			if len(links) > 2:
				links[2]["href"]="../index.html"
		elif self.ftype == "artist":
			for link in links[2:]:
				if "../" not in link["href"]:
					link["href"]=self.update_album(link["href"])

	def update_album(self,an):
		dir,fn=os.path.split(an)
		return "{}/{}".format(fn[:fn.find(".html")],fn)
	def insert_css(self, link):
		if self.bad:
			return
		if self.soup.head.find("link"):
			self.soup.head.link["href"]=link
			return
		new_tag=self.soup.new_tag("link",rel="stylesheet",href=link)
		self.soup.head.append(new_tag)
	#Now we're getting into functions to build the page if it doesn't yet exist
	def build(self):
		self.set_meta()
		#For now I'm going to assume the lyrics themselves have already been passed in or read
		self.build_header()
		self.soup=bs("<html></html>",'html.parser')

	#Check if there's artist, album, credits, language, etc
	def set_meta(self):
		pass

	def build_header(self):
		pass

	def write(self,file=None):
		if self.bad:
			return
		try:
			if file==None:
				fp=open(self.originalFile,'w')
			else:
				os.remove(self.originalFile)
				fp=open(self.originalFile,'w', encoding="UTF-8")
			self.soup.smooth()
			fp.write(self.soup.prettify())
			fp.close()
		except FileNotFoundError:
			print("I couldn't find a file called {}".format(self.originalFile))
		except UnicodeEncodeError as ue:
			print(ue.object[ue.start:ue.end])
			print("The encoding happened because of an encoding error: {}".format(ue.encoding))


failed_files=[]