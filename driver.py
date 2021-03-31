import htmldoc as hd
import os
hd.failed_files=[]
for root,dirs,files in os.walk("."):
	for file in files:
		h=hd.htmldoc(os.path.join(root,file))
		h.write()
print(hd.failed_files)