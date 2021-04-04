import os

all_files={}
def splitall(path):
	if not "/" in path and not "\\" in path:
		return [path]
	allparts = []
	while 1:
		parts = os.path.split(path)
		if parts[0] == path:  # sentinel for absolute paths
			allparts.insert(0, parts[0])
			break
		elif parts[1] == path:  # sentinel for relative paths
			allparts.insert(0, parts[1])
			break
		else:
			path = parts[0]
			allparts.insert(0, parts[1])
	return allparts

def find_path(to_find, album=None):
	if to_find.startswith("@@"):
		return
	path=splitall(to_find)
	if path[0]==to_find:
		path=[".",album,to_find]
	if not path[-1] in all_files:
		#print("I couldn't find a file named {}, maybe try to re-scrape it or add it yourself".format(path[-1]))
		return -1
	matches=all_files[path[-1]]
	for result in matches:
		if path[1] in result[1]:
			if len(result) > 2:
				new_path= "../../{}/{}/{}".format(result[1],result[2],path[-1])
			else: #It's most likely trying to link to a puirt or a compilation
				new_path= "../../{}/{}".format(result[1],path[-1])
			return new_path
