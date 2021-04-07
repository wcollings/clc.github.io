import os
import json
import globals as g

ds={}
def get_folders():
	for root,dirs,files in os.walk("."):
		for dir in dirs:
			if ".git" in root:
				continue
			if ".idea" in root:
				continue
			r=root[2:]
			if r in ds:
				ds[r].append(dir)
			else:
				ds[r]=[dir]
	return ds

ignore_folders=[".git",".idea",".vscode","__pycache__"]
ignore_files=["contact.html","contact_old.html","disclaimer.html","faq.html",
	"search.html", "template.html","source.html","updates.html", ".missing.html.swp", "missing.html",
	"sources.html"]

def get_files():
	all_files={}
	conflicts=[]
	for root, dirs,files in os.walk("."):
		for name in files:
			if name in ignore_files:
				continue
			if not ".html" in name:
				continue
			if "index" in name:
				continue
			if name in all_files:
				all_files[name].append(g.splitall(root))
			else:
				all_files[name]=[g.splitall(root)]
	return all_files