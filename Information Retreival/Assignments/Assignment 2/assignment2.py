# implementing the ranking function with command line

import sys
import re
import os

# creating a standalone function to get the ranked dataframe for all the queries
# creating a standalone function to get the ranked dataframe for all the queries
def get_ranked_tf_idf():
    
    # -------------------------------------
    # creating a dictionary for the stop words
    stop_words={}
    with open('/Users/carbon/Documents/Semester 6/Information Retreival/Assignments/Assignment 1/Urdu stopwords.txt','r') as f:
        for line in f:
            stop_words[line.strip()]=1

    # -------------------------------------
    queries = [
        'مجرم کو پھانسی دے دی گئی',
        'احتجاجی  دھرنے, جلوس اور ریلیاں',
        'انسداد تمباکو نوشی کے اقدامات اور آگاہی',
        'وکلاء کی ہڑتال اور ریلیاں',
        'خفیہ ایجنسیاں اور جاسوس',
        'احتساب عدالت کے مقدمات',
        'بچوں کے خلاف تشدد اور اغوا',
        'عورتوں پر ظلم و تشدد , قتل اور اغوا',
        'انسانوں کی اسمگلنگ اور انسداد انسانی سمگلنگ کے اقدامات',
        'مزدور طبقے کی خوشحالی کے اقدامات'
    ]

    # converting to a dictionary with keys as index and values as queries
    queries = {index: query for index, query in enumerate(queries)}
    queries

    # removing the stop words from the queries
    for q_id, query in queries.items():
        query = query.split()
        query = [word for word in query if word not in stop_words]
        
        # removing punctuation
        query = [word.strip(',?') for word in query]

        # removing empty strings
        query = [word for word in query if word != '']
        
        queries[q_id] = query

    # -------------------------------------
    # creating a hash table from the doc_index file as follows:
    # key: doc_id&term_id
    # value: term frequency

    hashmap = {}
    with open('/Users/carbon/Documents/Semester 6/Information Retreival/Assignments/Assignment 1/doc_index.txt') as f:
        for line in f:
            line = line.strip().split()
            hashmap [line[0] + '&' + line[1]] = int(len(line[2:]))

    # -------------------------------------
    # creating a list of all the documents
    with open('/Users/carbon/Documents/Semester 6/Information Retreival/Assignments/Assignment 1/docids.txt') as f:
        docs = [int(line.strip().split('\t')[-1]) for line in f.readlines()]
    total_docs = len(docs)

    # -------------------------------------
    # creating a dictionary for all the term ids
    term_ids = {}
    with open('/Users/carbon/Documents/Semester 6/Information Retreival/Assignments/Assignment 1/termids.txt') as f:
        for line in f:
            line = line.strip().split('\t')
            term_ids[line[1]] = int(line[0])
    
    # -------------------------------------
    # getting IDF for each term from term_info.txt
    term_idf = {}
    with open('/Users/carbon/Documents/Semester 6/Information Retreival/Assignments/Assignment 1/term_info.txt') as f:
        for line in f:
            line = line.strip().split('\t')
            term_idf[int(line[0])] = int(line[-1])
    
    # -------------------------------------
    # function to calculate the idf of a term
    def get_idf(term):
        import math
        try:
            result = term_idf[term_ids[term]]
        except:
            result = 0
        # calculating the idf
        if result == 0:
            idf = 0
        else:
            idf = math.log(total_docs / result)
        return idf
    # creating the query_idf dictionary
    query_idf = {}
    for q_id, query in queries.items():
        for word in query:
            query_idf[word] = get_idf(word)    

    # -------------------------------------
    # getting teh tf-idf for each complet query
    def get_tf_idf(query, doc_id):
        tf_idf = 0
        for term in query:
            try:
                tf = hashmap[str(doc_id) + '&' + str(term_ids[term])]
                tf_idf += tf * query_idf[term]
            except:
                pass
        return tf_idf
    
    # -------------------------------------
    import time
    import pandas as pd

    # function to give a ranked dataframe for a given query
    def get_ranked_df(query,qid):
        df = pd.DataFrame(columns=['query_id', 'doc_id', 'tf-idf', 'time'])
        for doc_id in docs:
            start = time.time()
            tf_idf = get_tf_idf(query, doc_id)
            end = time.time()
            
            # adding the data to the dataframe by concatenating
            df = pd.concat([df, pd.DataFrame([[qid, doc_id, tf_idf, end-start]], columns=['query_id', 'doc_id', 'tf-idf', 'time'])])
        print(query)
        
        # sort by query_id and tf-idf
        df.sort_values(by=['tf-idf'], ascending=False, inplace=True)

        # add a rank column
        df['rank'] = df.groupby('query_id').cumcount() + 1
        return df
    
    # -------------------------------------
    for q_id, query in queries.items():
        df = get_ranked_df(query, q_id)
        print(df.head(5),"\n")

    # writing the results to a file
    with open('/Users/carbon/Documents/Semester 6/Information Retreival/Assignments/Assignment 1/tfidf.txt', 'w') as f:
        for q_id, query in queries.items():
            df = get_ranked_df(query, q_id)
            for index, row in df.iterrows():
                f.write(str(row['query_id']) + ' Q0 ' + str(row['doc_id']) + ' ' + str(row['rank']) + ' ' + str(row['tf-idf']) + ' Exp\n')

# ranking tfidf ends here

# -------------------------------------

# implementing the BM25 ranking
# applying the BM25 algorithm
def get_ranked_bm25():
        
        # -------------------------------------
        # creating a dictionary for the stop words
        stop_words={}
        with open('/Users/carbon/Documents/Semester 6/Information Retreival/Assignments/Assignment 1/Urdu stopwords.txt','r') as f:
            for line in f:
                stop_words[line.strip()]=1
    
        # -------------------------------------
        queries = [
            'مجرم کو پھانسی دے دی گئی',
            'احتجاجی  دھرنے, جلوس اور ریلیاں',
            'انسداد تمباکو نوشی کے اقدامات اور آگاہی',
            'وکلاء کی ہڑتال اور ریلیاں',
            'خفیہ ایجنسیاں اور جاسوس',
            'احتساب عدالت کے مقدمات',
            'بچوں کے خلاف تشدد اور اغوا',
            'عورتوں پر ظلم و تشدد , قتل اور اغوا',
            'انسانوں کی اسمگلنگ اور انسداد انسانی سمگلنگ کے اقدامات',
            'مزدور طبقے کی خوشحالی کے اقدامات'
        ]
    
        # converting to a dictionary with keys as index and values as queries
        queries = {index: query for index, query in enumerate(queries)}
        queries
    
        # removing the stop words from the queries
        for q_id, query in queries.items():
            query = query.split()
            query = [word for word in query if word not in stop_words]
            
            # removing punctuation
            query = [word.strip(',?') for word in query]
    
            # removing empty strings
            query = [word for word in query if word != '']
            
            queries[q_id] = query
    
        # -------------------------------------
        # creating a hash table from the doc_index file as follows: 
        # key: doc_id&term_id
        # value: term frequency

        hashmap = {}
        with open('/Users/carbon/Documents/Semester 6/Information Retreival/Assignments/Assignment 1/doc_index.txt') as f:
            for line in f:
                line = line.strip().split()
                hashmap [line[0] + '&' + line[1]] = int(len(line[2:]))

        # -------------------------------------
        # creating a list of all the documents
        with open('/Users/carbon/Documents/Semester 6/Information Retreival/Assignments/Assignment 1/docids.txt') as f:
            docs = [int(line.strip().split('\t')[-1]) for line in f.readlines()]
        total_docs = len(docs)

        # -------------------------------------
        # creating a dictionary for all the term ids
        term_ids = {}
        with open('/Users/carbon/Documents/Semester 6/Information Retreival/Assignments/Assignment 1/termids.txt') as f:
            for line in f:
                line = line.strip().split('\t')
                term_ids[line[1]] = int(line[0])

        # -------------------------------------
        # getting IDF for each term from term_info.txt
        term_idf = {}
        with open('/Users/carbon/Documents/Semester 6/Information Retreival/Assignments/Assignment 1/term_info.txt') as f:
            for line in f:
                line = line.strip().split('\t')
                term_idf[int(line[0])] = int(line[-1])

        # -------------------------------------
        # function to calculate the idf of a term
        def get_idf(term):
            import math
            try:
                result = term_idf[term_ids[term]]
            except:
                result = 0
            # calculating the idf
            if result == 0:
                idf = 0
            else:
                idf = math.log(total_docs / result)
            return idf
        
        # creating the query_idf dictionary
        query_idf = {}
        for q_id, query in queries.items():
            for word in query:
                query_idf[word] = get_idf(word)

        # -------------------------------------
        # getting the tf-idf for each complete query
        def get_tf_idf(query, doc_id):
            tf_idf = 0
            for term in query:
                try:
                    tf = hashmap[str(doc_id) + '&' + str(term_ids[term])]
                    tf_idf += tf * query_idf[term]
                except:
                    pass
            return tf_idf
        
        # -------------------------------------
        import time
        import pandas as pd

        # function to give a ranked dataframe for a given query
        def get_ranked_df(query,qid):
            df = pd.DataFrame(columns=['query_id', 'doc_id', 'bm25', 'time'])
            for doc_id in docs:
                start = time.time()
                bm25 = get_tf_idf(query, doc_id)
                end = time.time()
                
                # adding the data to the dataframe by concatenating
                df = pd.concat([df, pd.DataFrame([[qid, doc_id, bm25, end-start]], columns=['query_id', 'doc_id', 'bm25', 'time'])])
            print(query)
            
            # sort by query_id and bm25
            df.sort_values(by=['bm25'], ascending=False, inplace=True)

            # add a rank column
            df['rank'] = df.groupby('query_id').cumcount() + 1
            return df
        
        # -------------------------------------
        for q_id, query in queries.items():
            df = get_ranked_df(query, q_id)
            print(df.head(5),"\n")

        # writing the output to a file
        with open('/Users/carbon/Documents/Semester 6/Information Retreival/Assignments/Assignment 1/bm25.txt', 'w') as f:
            for q_id, query in queries.items():
                df = get_ranked_df(query, q_id)
                for index, row in df.iterrows():
                    f.write(str(row['query_id']) + ' Q0 ' + str(row['doc_id']) + ' ' + str(row['rank']) + ' ' + str(row['bm25']) + ' Exp\n')

# ------------------------------------- End of BM25 -------------------------------------
# ------------------------------------- Start of drichlet smoothing -------------------------------------
def dirichlet_smoothing():
    doc_index = dict()
    term_info = dict()
    query_list = list()

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

# ------------------------------------- Start of system arguments -------------------------------------
try:
    if(sys.argv[1] == "--score" and sys.argv[2] == 'TF-IDF'): # call the tfidf function
        get_ranked_tf_idf()

    elif(sys.argv[1] == "--score" and sys.argv[2] == 'BM25'): # call the bm25 function
        get_ranked_bm25()
    elif(sys.argv[1] == "--score" and sys.argv[2] == 'Dirichlet'):
        dirichlet_smoothing()
except:
    print("Invalid command line arguments")
    sys.exit(0)