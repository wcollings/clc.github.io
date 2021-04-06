import os
import json

ds={}
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
json.dump(ds,open("dir_struct.json", 'w'))
