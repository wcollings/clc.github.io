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
			if "compilations" in root:
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

def get_dir_struct(songs_only=False):
	ds={}
	for root,dirs,files in os.walk("."):
		for dir in dirs:
			if ".git" in root:
				continue
			if ".idea" in root:
				continue
			if dir in ignore_folders:
				continue
			r=root[2:]
			if r in ds:
				ds[r].append(dir)
			else:
				ds[r]=[dir]
			if r=='':
				if not dir in ds:
					ds[dir]={}
			else:
				if not r in ds:
					ds[r]={}
				ds[r]={dir}
		for file in files:
			if file in ignore_files:
				continue
			if not ".html" in file:
				continue
			if "index" in file:
				continue
			if root==".":
				continue
			path=g.splitall(root)
			ds[path[1]][path[2]]
			continue

	print(ds)

#get_dir_struct()
print(get_folders())