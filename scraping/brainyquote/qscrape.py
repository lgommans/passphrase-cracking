#! /usr/bin/python3

import sys  # Get argument
import requests  # Get HTML
import bs4  # Parsing HTML
import argparse  # Command line argument parsing
import subprocess
import os

from cacher import get, post

from datetime import datetime  # Date/Time Information


def ArgParser():
    description = 'The Easy to use Quote Search'
    parser = argparse.ArgumentParser(prog='./getquote.py',
                                     usage='%(prog)s AUTHOR [options]',
                                     description=description)

    parser.add_argument('author', metavar='AUTHOR', nargs='*',
                        help='Search for quotes from AUTHOR')
    
    return parser


def GetQuote(author):
    results = []
    author_id = None 
    last_page = None

    print('Searching for {}...'.format(author))
    response = get('https://www.brainyquote.com/authors/{}'.format(author))
    QuoteObject = bs4.BeautifulSoup(response, 'html.parser')

    info = QuoteObject.select('.bio-under > a')
    cats = [] # categories
    for i in info:
        if 'profession' in i.get('href') or 'nationality' in i.get('href'):
            cats.append(i.getText())

    quotes = QuoteObject.select('#quotesList a')

    for quote in quotes:
        if quote.get('title') == 'view quote' and 'b-qt' in quote.get('class'):
            results.append(quote)

    for line in response.split('\n'):
        if 'PG_DM_ID' in line:
            author_id = line[10:-2]
        if 'LPAGE' in line:
            last_page = line[8:-1]

    for html_page in range(3, int(last_page) + 1):
        payload = {'pg':html_page, 'typ':'author', 'id':author_id}
        response = post('https://www.brainyquote.com/api/inf', payload)
        
        QuoteObject = bs4.BeautifulSoup(response['content'], 'html.parser')
        quotes = QuoteObject.select('a')

        for quote in quotes:
            if quote.get('title') == 'view quote' and 'b-qt' in quote.get('class'):
                results.append(quote)

    return cats, results


def PrintQuotes(quotes, author, cats):
    output_filename = '{}'.format(author) + '.txt'
    output_file = open(output_filename, 'w')
    output_file.write(','.join(cats) + '\n')

    for i in range(len(quotes)):
        output_file.write(quotes[i].getText() + '\n')


def Main():
    parser = ArgParser()
    args = parser.parse_args(sys.argv[1:])
    author = ' '.join(args.author)

    # Account for empty string
    if author == '':
        parser.print_help()
    else:
        cats, quotes = GetQuote(author)
        PrintQuotes(quotes, author, cats)
        print('Success!')


if __name__ == '__main__':
    Main()


