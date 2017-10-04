#!/usr/bin/env python3

import sys, os, requests, time, json
from hashlib import md5

cachefolder = 'cache/'
sleepy = 1
verbose = True

def get(url):
    f = cachefolder + md5(bytes(url, 'utf-8')).hexdigest() # cache file
    if os.path.isfile(f):
        with open(f) as ff:
            return ff.read()
    else:
        if verbose:
            sys.stderr.write('URL {} is not cached!\n'.format(url))

        req = requests.get(url, allow_redirects=False)
        if req.status_code == 301:
            return False

        req.raise_for_status()
        ff = open(f, 'w')
        ff.write(req.text)
        ff.close()
        time.sleep(sleepy)

        return req.text

def post(url, data):
    f = cachefolder + md5(bytes(url + data['id'] + str(data['pg']), 'utf-8')).hexdigest() # cache file
    if os.path.isfile(f):
        with open(f) as ff:
            return json.load(ff)
    else:
        if verbose:
            sys.stderr.write('URL {} with author id={};pg={} ({}) is not cached!\n'.format(url, data['id'], str(data['pg']), f))
        req = requests.post(url, allow_redirects=False, json=data)
        if req.status_code == 301:
            return False

        req.raise_for_status()
        ff = open(f, 'w')
        ff.write(req.text)
        ff.close()
        time.sleep(sleepy)

        return req.json()

