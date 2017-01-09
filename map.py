#! /usr/bin/python
 
from sys import stdin, stdout
import re
from stemming.porter2 import stem

fLine = True
for line in stdin:
    if fLine:
        doc_id, content = line.split('\t')
        fLine = False
    else:
        content = line


    words = re.findall(r'\w+', content)
                 
    for word in words:
        print("%s\t%s" % (stem(word.lower()), doc_id))
