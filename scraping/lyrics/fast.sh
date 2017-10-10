#!/bin/bash

cat artistclean.txt | parallel -j 4 python3 scrape.py {}
