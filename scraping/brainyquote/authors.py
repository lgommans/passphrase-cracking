#!/usr/bin/env python3

import bs4, sys
from cacher import get

baseurl = 'https://www.brainyquote.com/authors/'
verbose = True

for c in range(ord('a'), ord('z') + 1):
    for i in range(1, 20):
        if i == 1:
            i = ''
        else:
            i = str(i)

        html = get(baseurl + chr(c) + i)
        if html == False:
            if verbose:
                sys.stderr.write('Reached end of letter {} after {} pages.\n'.format(chr(c), i))
            break

        dom = bs4.BeautifulSoup(html, 'html.parser')
        thingies = dom.select('.table.table-hover.table-bordered > tbody > tr > td > a')
        for thingy in thingies:
            print(thingy.get('href') + '\t' + thingy.string)

