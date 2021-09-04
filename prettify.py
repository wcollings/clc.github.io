'''
This just runs through every file and refactors it if it's HTML
'''
from bs4 import BeautifulSoup as bs
import os

for root,dirs,files in os.walk("."):
	for name in files:
		if not ".html" in name:
			continue
		lines=open(os.path.join(root,name)).readlines()
		line=''.join(lines)
		s=bs(line)
		pretty=s.prettify()
		with open(os.path.join(root,name), 'w') as f:
			f.write(pretty)
		line=''
		print(os.path.join(root,name))
	#for name in dirs:
		#print(os.path.join(root,name))
