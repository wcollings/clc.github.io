import os
from bs4 import BeautifulSoup as bs
from functools import reduce

bad_links=[]
for root,dirs,files in os.walk("."):
	for file in files:
		if not "html" in file:
			continue
		path=os.path.join(root,file)
		s=bs(open(path), 'html.parser')
		links=s.find_all("a")
		for link in links:
			rel=os.path.join(root, link["href"])
			#rel=os.path.relpath(link["href"], start=path)
			if not os.path.exists(rel):
				bad_links.append([rel,path,link.sourcepos])
print(bad_links)