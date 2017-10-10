import requests
from bs4 import BeautifulSoup
import re
import time

filename = "Test"

def get_wiki(wikipage):
    file = open(filename, "w")
    r = requests.get('https://en.wikipedia.org'+wikipage)
    content = BeautifulSoup(r.content, 'html.parser')
    if 'Page not found' not in content:
#        print(wikipage)
        for item in content.select('td > ul > li > a'):
            file.write(re.sub(r'(\[[\d]*\])', '', item.text)+"\n")
    file.close()




def list_of_lists():
    request = requests.get('https://en.wikipedia.org/wiki/Category:Lists_of_musicians_by_genre')
    soup = BeautifulSoup(request.content, 'html.parser')
    lists = soup.find_all('li')

    for item in lists:
        item = str(item)
        if 'List of' in item:
            if 'List of grime' not in item:
                ref = item.split('\"')
                global filename
                filename = str(ref[3]).replace(" ", "_")
                get_wiki(ref[1])
    #        time.sleep(2)
#            title = item.split('')
#            print(filename)
#            get_wiki(str(ref))
#            print(item)



list_of_lists()
# get_wiki('/wiki/List_of_doom_metal_bands')