#!/usr/bin/env bash

find $@ -type f | while read line; do pypy pp-count.py "$line" -f; done

