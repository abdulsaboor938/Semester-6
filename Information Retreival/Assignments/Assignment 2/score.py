import os
import sys
import argparse
import string
import time
import shutil
import numpy as np

def load_index_paths():
    '''
    Returns doc_index.txt & term_index.txt paths
    '''
    index_dir = os.path.join("index_inverter")
    tokenizer_dir = os.path.join("tokenizer")
    
    doc_index = os.path.join(tokenizer_dir, "doc_index.txt")
    term_index = os.path.join(index_dir, "term_index.txt")
    
    return doc_index, term_index

def load_data_paths():
    '''
    Returns doc_ids.txt, term_ids.txt, and term_info.txt paths
    '''
    
    index_dir = os.path.join("index_inverter")
    tokenizer_dir = os.path.join("tokenizer")
    
    doc_ids = os.path.join(tokenizer_dir, 'doc_ids.txt')
    term_ids = os.path.join(tokenizer_dir, "term_ids.txt")
    term_info = os.path.join(index_dir, "term_info.txt")    
    
    return doc_ids, term_ids, term_info
    
def load_data_index_files():
    '''Function to get necessary data files into memory
    
    Returns:
    term_id, doc_id, doc_index, 
    and term_info dictionaries
    '''
    doc_index_path, term_index_path = load_index_paths()
    doc_ids_path, term_ids_path, term_info_path = load_data_paths()
    
    doc_ids = dict()
    doc_index = dict()
    
    term_ids = dict()
    term_info = dict()
    term_index = dict()
    with open(term_ids_path, mode='r', encoding='utf-8') as f:
        for line in f:
            row = line.strip().split()
            t_id = int(row[0])
            t_term = row[1]
            term_ids[t_term] = t_id
            
    with open(doc_ids_path, mode='r', encoding='utf-8') as f:
        for line in f:
            row = line.strip().split()
            d_id = int(row[0]) # doc id
            d_name = row[1] # doc name
            doc_ids[d_name] = d_id

    with open(doc_index_path, mode= 'r', encoding= 'utf-8') as f:
        for line in f:
            row = line.strip().split()
            d_id = int(row[0])
            t_id = int(row[1])
            t_pos = list(map(int, row[2:]))

            if d_id not in doc_index:
                doc_index[d_id] = dict()
            
            doc_index[d_id][t_id] = t_pos
    
    with open(term_info_path, mode='r', encoding='utf-8') as f:
        for line in f:
            row = line.strip().split()
            t_id = int(row[0])
            t_offset = int(row[1])
            t_corpus_freq = int(row[2])
            t_total_docs = int(row[3])
            term_info[t_id] = {"offset" : t_offset, 
                               "corpus_freq" : t_corpus_freq, 
                               "doc_freq" : t_total_docs}
            
    return doc_ids, term_ids, doc_index, term_info

def initialize_urdu_stopwords():
    ''' A function that returns a set of stopwords for the urdu language froma file
    
    Returns:
        set: The stopwords
    '''
    
    urdu_stopwords = set()
    with open('urdu_stopwords.txt', 'r', encoding= 'utf-8') as f:
        for line in f:
            urdu_stopwords.add(line.strip())
    
    puntuation_set = set([char for char in string.punctuation])
    urdu_stopwords = urdu_stopwords.union(puntuation_set)
    urdu_stopwords.update(['’', '‘', '۔', '؟', '؛', '،', '٪', '،'])
    return urdu_stopwords

def clean_tokenize_text(text, urdu_stopwords):
    ''' Cleans and processes urdu text into a usable form
    
    Args:
        string (str): string to be processed
        urdu_stopwords (str|set): a set of stopwords or delims to remove
    
    Returns:
        list: text processed and tokenized
    '''
    
    delims = '’‘۔؟؛،٪،\n '
    for delim in delims:
        text = text.replace(delim, " ")
    tokens = text.split()
    tokens = [word for word in tokens if not word in urdu_stopwords and not (('a' <= word[0] <= 'z') or ('A' <= word[0] <= 'Z'))]
    return tokens

def get_term_index(term, term_info):
    _, term_index_path = load_index_paths()
    offset = None
    
    info = term_info[term]
    try:
        offset = info["offset"]
    except:
        pass
    
    
    if offset == None:
        pass
    
    term_index = dict()
    with open(term_index_path, mode= 'r', encoding= 'utf-8') as f:
        f.seek(offset)
        line = f.readline()
        row = line.strip().split()
        total_entries = len(row)
        
        delta_decoded_doc_id = None
        delta_decoded_term_pos = None
        i = 1
        while(i < total_entries):
            # Get encoded values
            encoded_doc_id = int(row[i].split(':')[0])
            encoded_pos = int(row[i].split(':')[1])
            
            if delta_decoded_doc_id is None:
                delta_decoded_doc_id = encoded_doc_id
            else:
                delta_decoded_doc_id += encoded_doc_id
            
            if delta_decoded_doc_id not in term_index:
                term_index[delta_decoded_doc_id] = list()
                term_index[delta_decoded_doc_id].append(encoded_pos)
                delta_decoded_term_pos = encoded_pos

            i += 1
            while(i < total_entries):
                encoded_doc_id = int(row[i].split(':')[0])
                if(encoded_doc_id != 0):
                    break
                
                encoded_pos = int(row[i].split(':')[1])
                delta_decoded_term_pos = delta_decoded_term_pos + encoded_pos
                term_index[delta_decoded_doc_id].append(delta_decoded_term_pos)
                i += 1
        
        return term_index
                

def tf_idf(query_list, doc_index, term_info):
    total_docs = len(set(doc_index.keys()))
    tf_idf_scores = dict() 
    
    total_queries = len(query_list)
    query_count = 0
    print()
    for query in query_list:
        query_count += 1   
        print(f"Calculating tf-idf: {query_count} / {total_queries}", end= '\r')
        idf_dict = dict()
        tf_dict = doc_index.copy()

        vec_query = query["Vector-Query"]
        query_id = query["id"]

        # idf
        for term in vec_query:
            if term in term_info:
                idf_dict[term] = np.log(total_docs/term_info[term]["doc_freq"])
            else:
                df_dict[term] = 0
        # tf
        for doc in tf_dict:
            for term in tf_dict[doc]:
                if term in vec_query:
                    try:
                        tf_dict[doc][term] = 1 + np.log(len(doc_index[doc][term]))
                    except:
                        tf_dict[doc][term] = 1
                else:
                    tf_dict[doc][term] = 0
        
        for doc in doc_index:
            tf_idf_sum = 0
            for term in doc_index[doc]:
                if term in vec_query:
                    idf = idf_dict[term]
                    tf = tf_dict[doc][term]
                    
                    tf_idf = np.multiply(tf, idf)
                    tf_idf_sum = np.add(tf_idf_sum, tf_idf)
            
            if query_id not in tf_idf_scores:
                tf_idf_scores[query_id] = list()
            
            entry = (doc, tf_idf_sum)
            tf_idf_scores[query_id].append(entry)
            
        tf_idf_scores[query_id] = sorted(tf_idf_scores[query_id], key= lambda x: x[1], reverse= True)
    
    # write to file
    
    tf_idf_path = os.path.join('tf-idf','tf_idf_ranks.txt')
    if os.path.exists(tf_idf_path):
        os.remove(tf_idf_path)
    f = open(tf_idf_path, mode= 'w')
    
    print(f"Calculating tf-idf: {query_count} / {total_queries} COMPLETED")
    query_count = 0
    print()
    for query in query_list:
        query_count += 1
        print(f"Writing result to file: {query_count} / {total_queries}", end= '\r')
        topic = query["id"]
        rank = 1
        for doc, score in bm25_scores[topic]:
            f_entry = f"{topic}\t{doc}\t{rank}\t{score}\n"
            f.write(f_entry)
            rank += 1
            
    print(f"Writing result to file: {query_count} / {total_queries} COMPLETED")
    f.close()
    
def okapi_bm25(query_list, doc_index, term_info):
    total_docs = len(set(doc_index.keys()))
    bm25_scores = dict() 
    
    total_queries = len(query_list)
    query_count = 0
    print()
    for query in query_list:
        query_count += 1   
        print(f"Calculating bm25: {query_count} / {total_queries}", end= '\r')
        df_dict = dict()
        tf_dict = doc_index.copy()

        vec_query = query["Vector-Query"]
        query_id = query["id"]

        
        # df
        for term in vec_query:
            if term in term_info:
                df_dict[term] = term_info[term]["doc_freq"]
            else:
                df_dict[term] = 0
        # tf
        for doc in tf_dict:
            for term in tf_dict[doc]:
                if term in vec_query:
                    tf_dict[doc][term] = len(doc_index[doc][term])
                else:
                    tf_dict[doc][term] = 0
        
        total_terms = len(term_info)
        avg_doc_len = total_terms/total_docs
        
        k1 = 1.2
        k2 = 750
        b = 0.75
        
        for doc in doc_index:
            bm25_sum = 0.0
            doc_len = 0
            for term in doc_index[doc]:
                try:
                    doc_len += len(doc_index[doc][term])
                except:
                    doc_len += 0
            K = k1 * ((1-b) + b*(doc_len/ avg_doc_len))
            
            for term in doc_index[doc]:
                if term in vec_query:
                    df = df_dict[term]
                    tf = tf_dict[doc][term]
                    
                    x1 = np.log((total_docs + 0.5) / df + 0.5)
                    x2 = ((1 + k1) * tf)/(K + tf)
                    x3 = ((1 + k2))/(k2 + 1)
                    
                    term_score = x1 + x2 + x3
                    bm25_sum += term_score                
                    
            
            if query_id not in bm25_scores:
                bm25_scores[query_id] = list()
            
            entry = (doc, bm25_sum)
            bm25_scores[query_id].append(entry)
            
        bm25_scores[query_id] = sorted(bm25_scores[query_id], key= lambda x: x[1], reverse= True)
    
    # write to file
    bm25_path = os.path.join('bm25','bm25_ranks.txt')
    if os.path.exists(bm25_path):
        os.remove(bm25_path)
    f = open(bm25_path, mode= 'w')
    
    print(f"Calculating bm25: {query_count} / {total_queries} COMPLETED")
    query_count = 0
    print()
    for query in query_list:
        query_count += 1
        print(f"Writing result to file: {query_count} / {total_queries}", end= '\r')
        topic = query["id"]
        rank = 1
        for doc, score in bm25_scores[topic]:
            f_entry = f"{topic}\t{doc}\t{rank}\t{score}\n"
            f.write(f_entry)
            rank += 1
            
    print(f"Writing result to file: {query_count} / {total_queries} COMPLETED")
    f.close()

def dirichlet_smoothing(query_list, doc_index, term_info):
    total_docs = len(set(doc_index.keys()))
    ds_scores = dict() 
    
    total_queries = len(query_list)
    query_count = 0
    
    total_terms = len(term_info)
    avg_doc_len = total_terms/total_docs
    
    total_words = 0
    # get total words
    for term in term_info:
        corpus_freq = term_info[term]["corpus_freq"]
        total_words += corpus_freq
    
    print()
    for query in query_list:
        query_count += 1   
        print(f"Calculating dirichlet smoothing: {query_count} / {total_queries}", end= '\r')
        tf_dict = doc_index.copy()
        
        vec_query = query["Vector-Query"]
        query_id = query["id"]
        
        # tf
        for doc in tf_dict:
            for term in tf_dict[doc]:
                if term in vec_query:
                    try:
                        tf_dict[doc][term] = 1 + np.log(len(doc_index[doc][term]))
                    except:
                        tf_dict[doc][term] = 1
                else:
                    tf_dict[doc][term] = 0
        
        # background probabilities
        bgp_product = 1
        for term in term_info:
            if term in vec_query:
                corpus_freq = term_info[term]["corpus_freq"]
                p = corpus_freq/total_words
                bgp_product *= p
        
        # ml estimates + ds score
        for doc in tf_dict:
            ds_score = None
            doc_len = len(tf_dict[doc])
            for term in tf_dict[doc]:
                tf = tf_dict[doc][term]
                mle_score = np.divide(tf,doc_len)
                
                x1 = np.multiply(doc_len/(doc_len + avg_doc_len), mle_score)
                x2 = np.multiply(avg_doc_len/(doc_len + avg_doc_len), bgp_product)
                
                ds_score = x1 + x2
        
            if query_id not in ds_scores:
                ds_scores[query_id] = list()
            
            entry = (doc, ds_score)
            ds_scores[query_id].append(entry)
        
        # print(ds_scores[query_id])
        ds_scores[query_id] = sorted(ds_scores[query_id], key= lambda x: x[1], reverse= True)
    
    # write to file
    ds_path = os.path.join('ds','dirichlet_smoothing_ranks.txt')
    if os.path.exists(ds_path):
        os.remove(ds_path)
    f = open(ds_path, mode= 'w')
    
    print(f"Calculating dirichlet smoothing: {query_count} / {total_queries} COMPLETED")
    query_count = 0
    print()
    for query in query_list:
        query_count += 1
        print(f"Writing result to file: {query_count} / {total_queries}", end= '\r')
        topic = query["id"]
        rank = 1
        for doc, score in ds_scores[topic]:
            f_entry = f"{topic}\t{doc}\t{rank}\t{score}\n"
            f.write(f_entry)
            rank += 1
            
    print(f"Writing result to file: {query_count} / {total_queries} COMPLETED")
    f.close()



def main():
    QRELS = os.path.join('resources', 'qrels.csv ')
    QUERIES = os.path.join("resources", "queries.csv")
    urdu_stopwords = initialize_urdu_stopwords()
    query_list = list()

    parser = argparse.ArgumentParser()
    parser.add_argument("-S", "--score", help= "Will score the given documents on the passed algorithm. -- TF-IDF [tf-idf] -- BM25 [bm25] -- Dirichlet Smoothing [ds]--")

    args = parser.parse_args()

    # Retrieving all queries feom file
    with open(QUERIES, mode='r', encoding= 'utf-8') as f:
        for line in f.readlines():
            # Each query and its info will be stored as a dictionary into a list
            query_dict = dict()

            line = line.strip().split('\t')

            query_dict["id"] = int(line[0])
            query_dict["Domain"] = line[1]
            query_dict["Topic-English"] = line[2]

            # clean the query the same way text cleaning was performed on the docs
            cleaned_query = clean_tokenize_text(line[3], urdu_stopwords= urdu_stopwords)
            query_dict["Topic-Urdu"] = cleaned_query

            query_list.append(query_dict)

    doc_ids, term_ids, doc_index, term_info = load_data_index_files()
    
    # Converting query into number representation
    for query in query_list:
        urdu_query = query["Topic-Urdu"]
        vec_query = list()
        
        for word in urdu_query:
            try:
                enc = term_ids[word]
                vec_query.append(enc)
            except:
                # if word not currently in corpus
                term_ids[word] = len(term_ids)
                enc = term_ids[word]
                vec_query.append(enc)
        query["Vector-Query"] = vec_query
    
    function_map = {
        "tf-idf": tf_idf,
        "bm25": okapi_bm25,
        "ds": dirichlet_smoothing
    }    
    
    if args.score not in ["tf-idf", "bm25", "ds"]:
        print("Please select a valid scoring function")
        sys.exit()
    
    if not os.path.exists(args.score):
        os.mkdir(path=args.score)
    else:
        shutil.rmtree(args.score)
        os.mkdir(path=args.score)
    
    func = args.score
    function_map[func](query_list, doc_index, term_info)
    
    
    
if __name__ == "__main__":
    main()