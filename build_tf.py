#!/usr/bin/python

from stemming.porter2 import stem
import os
import json, re

os.system("mkdir tf")

def parse_document(doc_name):
    with open(doc_name, 'r') as doc:
        content = doc.read();

    list_of_words = re.findall(r'\w+', content)
    list_of_words = [stem(word) for word in list_of_words]

    doc_dict = {}
    for w in list_of_words:
      doc_dict[w] = doc_dict.get(w, 0.) + 1.0

    length = float(len(list_of_words))

    with open('tf/' + doc_name.split('/')[-1].split('.')[0] + '.json', 'w') as fp:
        json.dump([length, doc_dict], fp)

for file in os.listdir("articles"):
    parse_document("articles/" + file)