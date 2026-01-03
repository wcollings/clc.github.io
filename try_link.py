from bs4 import BeautifulSoup as bs
from os import path, walk, chdir
from linking import split_path

def try_link(fname):
	if path.exists(fname):
		return fname,False
	path_base,fname_base=path.split(fname)
	for root,dirs,files in walk(path_base):
		for name in files:
			if name==fname_base:
				return path.join(root,name),True
	fname="../"+fname
	if path.exists(fname):
		return fname,False
	# fname = anuna/behind/behind.html
	# path_base = anuna/behind
	# fname_base = behind.html
	path_base,fname_base=path.split(fname)
	parent_folder =split_path(fname)[-2]
	if parent_folder in fname_base:
		return path.join(path_base,"index.html"),True
	for root,dirs,files in walk(path_base):
		for name in files:
			if name==fname_base:
				return path.join(root,name),True
	else:
		print(f'WARNING: could not find a link for "{fname}"',end="")
		raise Exception()


ignore=['altan','amhlaoibh']
files_to_try=[]
base_dir = path.realpath('.')
for root,dirs,files in walk("."):
	for name in files:
		# print(path.splitext(name))
		if path.splitext(name)[1]=='.html':
			files_to_try.append(path.join(root,name))
	# for name in dirs:
	# 	print(path.join(root,name))
for file in files_to_try:
	write_f=False
	new_dir,fp=path.split(file)
	chdir(new_dir)
	f=open(fp,'r')
	soup=bs(f,'html.parser')
	f.close()
	parent=split_path(file)[-2]
	for link in soup.find_all('a'):
		p=link['href']
		lis=p.split('?')
		f1=lis[0]
		args=None
		if len(lis) > 1:
			args=lis[0]
		if path.splitext(f1)[0]==parent:
			link['href']="index.html"
			write_f=True
			continue
		try:
			new_loc,new_link=try_link(f1)
			write_f|=new_link
			if args is not None:
				new_loc+="?"+args
			link['href']=new_loc
		except:
			print(f' in file "{f1}"')
	if write_f:
		f=open(fp,'w')
		f.write(soup.prettify())
	chdir(base_dir)
