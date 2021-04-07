import os
import re
import htmldoc
import globals as g
from htmldoc import htmldoc as hd
import dirs

class conflict:
	def __init__(self, fname,first,second):
		self.fname=fname
		self.first=first
		self.second=second
	def print(self):
		print("Found a conflict with file:{}\n\t{}\n\t{}".format(self.fname,self.first,self.second))



g.failed_files=[]
ignore_files=["contact.html","contact_old.html","disclaimer.html","faq.html",
	"search.html", "template.html","source.html","updates.html", ".missing.html.swp", "missing.html",
	"sources.html"]
dirs.ignore_files=ignore_files
g.all_files=dirs.get_files()
print("I found {} songs".format(len(g.all_files)))
g.links_f=open("links_to_update.txt","w")
for root,dirs,files in os.walk("."):
	for name in files:
		if name in ignore_files:
			continue
		if not ".html" in name:
			continue

		cf=hd(os.path.join(root,name))
		temp=g.splitall(os.path.join(root,name))
		if root==".":
			cf.insert_css("style.css")
			cf.clean()
			cf.write()
		#"index.html" is always an artist
		if "index" in name:
			cf.ftype="artist"
			cf.clean()
			cf.insert_css("../style.css")
		#the album file is under the same name as its folder, so it's ".../album/album.html"
		elif temp[2] in name:
			cf.ftype="album"
			cf.clean()
			cf.insert_css("../../style.css")
		else:
			cf.ftype="song"
			cf.clean()
			cf.insert_css("../../style.css")
		#cf.update_links()
		cf.write()
print("Failed files:")
print(htmldoc.failed_files)
g.links_f.close()
