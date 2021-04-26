from bs4 import BeautifulSoup as bs
import json

links={}
s=bs(open("artists.html", encoding="UTF-8"), "html.parser")
t=s.find("table",{"id":"head_t"})
for a in t.find_all("a"):
	val=a.get_text().strip()
	if val[0]=='\t':
		val=val[1:]
	if val[0]==' ':
		val=val[1:]
	key=a["href"]
	key=key[:key.find("/")]
	links[key]=val

s=dict(sorted(links.items(), key = lambda x:x[0]))
third=len(s)/3
lc=dict(s.items()[:third])
mc=dict(s.items()[third:2*third])
rc=dict(s.items()[2*third:])

json.dump([lc,mc,rc],open("js/artists.json", 'w', encoding="UTF-8"), ensure_ascii=False)