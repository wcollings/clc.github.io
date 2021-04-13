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

def get_files(songs_only=False):
	all_files={}
	for root, dirs,files in os.walk("."):
		for name in files:
			if name in ignore_files:
				continue
			if not ".html" in name:
				continue
			if "index" in name:
				continue
			if root==".":
				continue
			path=g.splitall(root)
			if songs_only:
				if path[-1]==name[:name.find(".")]:
					continue
			if name in all_files:
				all_files[name].append(path)
			else:
				all_files[name]=[path]
	return all_files
