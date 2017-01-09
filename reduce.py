#! /usr/bin/python
 
from sys import stdin
import re
 
index = {}
         
for line in stdin:
    word, postings = line.split('\t')
 
    index.setdefault(word, set()) 
                 
    for doc_id in postings.split(','): 
        index[word].add(doc_id.split('\n')[0])

  
for word in index:
    postings_list = list(index[word])
 
    postings = ','.join(postings_list)
    print('%s\t%s' % (word, postings))