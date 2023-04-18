import argparse

# function to read term_info.txt
def read_term_info():
    hash = {}
    with open('term_info.txt', 'r') as f:
        for line in f:
            line = line.split('\t')
            hash[int(line[0])] = [int(line[1]), int(line[2])]
    return hash


# function to read docids.txt
def read_docids():
    hash = {}
    with open('docids.txt', 'r') as f:
        for line in f:
            line = line.split('\t')
            hash[int(line[1])] = int(line[0])
    return hash


# function to read termids.txt

def read_termids():
    hash = {}
    with open('termids.txt', 'r') as f:
        for line in f:
            line = line.split('\t')
            hash[line[1].strip()] = int(line[0])
    return hash


# function to read term_index.txt
def read_term_index():
    hash = {}
    with open('term_index.txt', 'r') as f:
        for line in f:
            line = line.split('\t')
            termid = int(line[0])
            hash[termid] = {}
            for i in range(1, len(line)):
                line[i] = line[i].split(':')
                docid = int(line[i][0])
                hash[termid][docid] = []
                line[i] = line[i][1].split(',')
                for j in range(len(line[i])):
                    hash[termid][docid].append(int(line[i][j]))
    return hash


# function to read doc_index.txt
def read_doc_index():
    hash = {}
    with open('doc_index.txt', 'r') as f:
        for line in f:
            line = line.split('\t')
            docid = int(line[0])
            termid = int(line[1])
            hash[docid] = {}
            hash[docid][termid] = []
            for i in range(2, len(line)):
                hash[docid][termid].append(int(line[i]))
    return hash



# function to get the termid
def get_termid(term):
    hash = read_termids()
    if term in hash:
        return hash[term]
    else:
        return -1
    

# function to get the docid
def get_docid(doc):
    hash = read_docids()
    if doc in hash:
        return hash[doc]
    else:
        return -1
    

# function to get the term frequency in corpus
def get_term_frequency(termid):
    hash = read_term_info()
    return hash[termid][0]


# function to get the number of documents containing term
def get_num_docs(termid):
    hash = read_term_info()
    return hash[termid][1]


# function to get the inverted list offset
def get_inverted_list_offset(termid):
    hash = read_term_index()
    return hash[termid]


# function to get the term frequency in document
def get_term_frequency_in_doc(termid, docid):
    hash = read_doc_index()
    return len(hash[docid][termid])


# function to get the positions
def get_positions(termid, docid):
    hash = read_doc_index()
    return hash[docid][termid]


# function to get the distinct terms
def get_distinct_terms(docid):
    hash = read_doc_index()
    return len(hash[docid])


# function to get the total terms
def get_total_terms(docid):
    hash = read_doc_index()
    total = 0
    for termid in hash[docid]:
        total += len(hash[docid][termid])
    return total

#write main function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--doc', type=str, help='doc name')
    parser.add_argument('--term', type=str, help='term')
    args = parser.parse_args()
    if args.doc and args.term:
        termid = get_termid(args.term)
        docid = get_docid(args.doc)
        if termid == -1 or docid == -1:
            print('Invalid term or doc')
            return
        print('Inverted list for term:', args.term)
        print('In document:', args.doc)
        print('TERMID:', termid)
        print('DOCID:', docid)
        print('Term frequency in document:', get_term_frequency_in_doc(termid, docid))
        print('Positions:', get_positions(termid, docid))
    elif args.doc:
        docid = get_docid(args.doc)
        if docid == -1:
            print('Invalid doc')
            return
        print('Listing for document:', args.doc)
        print('DOCID:', docid)
        print('Distinct terms:', get_distinct_terms(docid))
        print('Total terms:', get_total_terms(docid))
    elif args.term:
        termid = get_termid(args.term)
        if termid == -1:
            print('Invalid term')
            return
        print('Listing for term:', args.term)
        print('TERMID:', termid)
        print('Number of documents containing term:', get_num_docs(termid))
        print('Term frequency in corpus:', get_term_frequency(termid))
        print('Inverted list offset:', get_inverted_list_offset(termid))
    else:
        print('Invalid input')

if __name__ == '__main__':
    main()
    
