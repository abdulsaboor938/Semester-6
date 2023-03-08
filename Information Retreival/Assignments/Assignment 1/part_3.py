# this is an implementation of command line arguemnts
# take an argument and print it out

import sys
import re

try:
    if(sys.argv[1] == "--doc" and len(sys.argv) <4):
        print(f"\nlisting for document: {sys.argv[2].split('.')[0]}")
        
        with open('docids.txt') as f:
            docids = f.read().splitlines()

        # storing in a dictionary
        docids_dict = {}
        for i in range(len(docids)):
            key, val = docids[i].split('\t')
            docids_dict[int(val)] = int(key)

        print(f"DOCID: {docids_dict[int(sys.argv[2].split('.')[0])]}")

        with open(f"Documents/{sys.argv[2]}") as f:
            text = f.read()

        try:
            # only selecting text beteen <TEXT> and </TEXT>
            text = text.split('<TEXT>')[1].split('</TEXT>')[0]
        except IndexError:
            pass
        try:
            text=text.split('comment')[0]
        except IndexError:
            pass

        # removing all the punctuations
        text = re.sub(r'[^\w\s]', '', text)

        arr = [i.strip() for i in text.split(' ')]

        print(f"Distinct Terms: {len(set(arr))}")
        print(f"Total Terms: {len(arr)}\n")

    if(sys.argv[1] == "--term" and len(sys.argv) <4):
        term = sys.argv[2]

        print(f"\nlisting for term: {term}")

        # term id
        with open('termids.txt') as f:
            termids = f.read()
        for i in termids.splitlines():
            key, val = i.split('\t')
            if val == term:
                print(f"TERMID: {int(key)}")
            break

        check = key
        # Number of documents containing the term
        with open('term_info.txt') as f:
            term_info = f.read()

        for i in term_info.splitlines():
            term,offset,occur,doc = i.split('\t')
            if term == check:
                print(f"Number of documents containing the term: {int(doc)}")
                print(f"Term frequency in corpus: {int(occur)}")
                print(f"Inverted list offset: {int(offset)}\n")

    if(sys.argv[1] == "--term" and sys.argv[3] == "--doc"):
        doc = sys.argv[4]
        term = sys.argv[2]

        print(f"\nInverted list for term: {term}")
        print(f"In document: {doc}")

        # term id
        with open('termids.txt') as f:
            termids = f.read()
        for i in termids.splitlines():
            termid, val = i.split('\t')
            if val == term:
                print(f"TERMID: {int(termid)}")
            break

        # doc id
        doc = doc.split('.')[0]
        with open('docids.txt') as f:
            docids = f.read()
        for i in docids.splitlines():
            key, val = i.split('\t')
            if val == doc:
                print(f"DOCID: {int(key)}")
            break

        # frequency of term in document
        with open('doc_index.txt') as f:
            doc_index = f.read()
        for i in doc_index.splitlines():
            i=i.split('\t')
            if(i[0]==key and int(i[1]==termid)):
                print(f"Term frequency in document: {int(i[2])}")
                print(f"Term positions: ",end='')
                for j in i[2:]:
                    print(j,end=',')
                print(f"\n")
                break
except:
    pass