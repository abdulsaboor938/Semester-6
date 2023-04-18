# implementing the ranking function with command line

import sys
import re

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
        # getting the tf-idf for each complet query
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

# ------------------------------------- Start of system arguments -------------------------------------
try:
    if(sys.argv[1] == "--score" and sys.argv[2] == 'TF-IDF'): # call the tfidf function
        get_ranked_tf_idf()

    elif(sys.argv[1] == "--score" and sys.argv[2] == 'BM25'): # call the bm25 function
        get_ranked_bm25()
    
except:
    print("Invalid command line arguments")
    sys.exit(0)