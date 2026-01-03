"""
The point of this is to read through the songlist files and generate a JSON table (or database of some kind?) where each song is only listed once,
regardless of if there are different versions under different names.

"""
from bs4 import BeautifulSoup as bs
from collections import defaultdict

class link:
    def __init__(self,a):
        self.address=a['href']
        self.contents=a.string.strip()
    def __hash__(self):
        return hash(self.address)
    def __lt__(self, rhs):
        if isinstance(rhs, link):
            return self.contents < rhs.contents
        if isinstance(rhs,str):
            return self.contents < rhs
def name_from_list(s):
    return s.strip()[3:]

def sort_links_and_strs(a,b):
    if isinstance(b,link) and isinstance(a,str):
        return not (b<a)
    return a<b
class Song:
    def __init__(self,tr):
        cells = tr.find_all("td")
        self.song=link(cells[0].a)
        self.arist=link(cells[1].a)
        self.album=link(cells[2].a)
        alternates=[]
        if len(cells) < 4:
            return
        if cells[3].text.strip().startswith("See also"):
            self.alternates = list(map(link,cells[3].find_all('a')))
        # elif cells[3].text.strip().startswith("a)"):
            # alternates = list(map(name_from_list,cells[3].strings))
    def __hash__(self):
        if hasattr(self,'alternates'):
            file_under = min([self.song]+self.alternates)
            return hash(file_under)
        return hash(self.song)
    def __repr__(self):
        return f"{self.song.contents} by {self.arist.contents}"

if __name__=="__main__":
    all_songs = defaultdict(list)
    contents = bs(open("songlist-a_1.html"),"html.parser")
    next_song=contents.find("tr").next_sibling.next_sibling.next_sibling
    rows = contents.find_all("tr")[1:]
    for entry in rows:
        s=Song(entry)
        all_songs[s].append(s)
    print(all_songs)