import os
import pandas as pd
import numpy as np

def load_score_values():
    doc_ids_path = os.path.join("tokenizer", "doc_ids.txt")
    doc_ids_dict = dict()
    with open(doc_ids_path, mode='r', encoding='utf-8') as f:
        for line in f:
            row = line.strip().split()
            d_id = int(row[0]) # doc id
            d_name = row[1] # doc name
            doc_ids_dict[d_id] = int(d_name.split(".")[0])

    
    tf_idf_path = os.path.join("tf-idf", "tf_idf_ranks.txt")
    bm25_path = os.path.join("bm25", "bm25_ranks.txt")
    ds_path = os.path.join("ds", "dirichlet_smoothing_ranks.txt")
    
    path_list = [tf_idf_path, bm25_path, ds_path]
    
    tf_idf_ranks = pd.DataFrame()
    bm25_ranks = pd.DataFrame()
    ds_ranks = pd.DataFrame()
    
    rank_dict = {
        tf_idf_path: tf_idf_ranks,
        bm25_path: bm25_ranks,
        ds_path: ds_ranks
    }
    
    for path in path_list:
        topic_list = list()
        doc_id_list = list()
        rank_list = list()
        score_list = list()
        with open(path, mode= 'r') as f:
            doc_count = 0
            curr_topic = 1
            for line in f:
                
                
                row = line.strip().split()
                
                topic = int(row[0])
                
                if(doc_count == 50 and topic == curr_topic):
                    continue
                elif(doc_count == 50 and not topic == curr_topic):
                    doc_count = 0
                    curr_topic = topic
                
                doc_id = int(row[1])
                doc_id = doc_ids_dict[doc_id]
                rank = int(row[2])
                score = float(row[3])

                topic_list.append(topic)
                doc_id_list.append(doc_id)
                rank_list.append(rank)
                score_list.append(score)
                doc_count += 1
            
        rank_dict[path]["query"] = topic_list
        rank_dict[path]["doc_id"] = doc_id_list
        rank_dict[path]["rank"] = rank_list
        rank_dict[path]["score"] = score_list
        
        score_func_dict = {
            "tf-idf": tf_idf_ranks,
            "bm25": bm25_ranks,
            "ds": ds_ranks
        }
        
    return score_func_dict
        
def load_qrels():
    qrels_path = os.path.join("resources", "qrels.xlsx")
    qrels = pd.read_excel(qrels_path, None)
    
    for sheet in qrels:
        df = qrels[sheet]
        del df["Irrelevant Doc"]
        del df["Marginally relevant Doc"]
        del df["Fairly relevant Doc"]
        del df["Highly relevant Doc"]

        is_relevant = df["Doc Relevancy"] > 2
        df["Is Relevant"] = is_relevant        
        
        del df["Doc Relevancy"]
    return qrels

def classify_scores(qrels, score_func_dict):
    updated_dict = dict()
    
    for score_func in score_func_dict:
        print(f"\nFunction: {score_func}")
        rank_df = score_func_dict[score_func]
        is_rel = [False] * len(rank_df)
        
        for sheet in qrels:
            print(f"Sheet {sheet}")
            qrel_df = qrels[sheet]
            qrel_id = qrel_df["Topic Id"].iloc[0]
            
            qid_filter = rank_df["query"] == qrel_id
            set1 = set(rank_df[qid_filter]["doc_id"])
            set2 = set(qrel_df["Doc Id"])
            
            common_values = set1.intersection(set2)
            mask = qrel_df["Doc Id"].isin(common_values)
            filtered_qrel = qrel_df[mask]
            
            for index, row in rank_df.iterrows():
                qrel_row = filtered_qrel.loc[filtered_qrel["Doc Id"] == row["doc_id"]]
                if len(qrel_row) != 0:
                    if(qrel_row["Is Relevant"].iloc[0]):
                        is_rel[index] = True
        
            rank_df["is_rel"] = is_rel
            updated_dict[score_func] = rank_df
    print()
    return updated_dict
    
def mean_average_precision(true_series, pred_series, k=None):
    true_bool = true_series.astype(bool)
    pred_bool = pred_series.astype(bool)
    
    df = pd.DataFrame({'true': true_bool, 'pred': pred_bool})
    # df.sort_values(by='pred', ascending=False, inplace=True)
    df = df.fillna(False)
    
    if k is not None:
        p_at_k = np.sum(df['true'].values[:k]) / k
        return p_at_k
    
    precision = []
    recall = []
    relevant_count = 0
    for i, (_, row) in enumerate(df.iterrows()):
        if row['true']:
            relevant_count += 1
        precision.append(relevant_count / (i + 1))
        recall.append(relevant_count / true_bool.sum())
    
    
    ap = np.sum(np.array(precision) * np.array(df['true'])) / true_bool.sum()
    # print(np.array(precision), np.array(df['true']))
    map_score = np.mean(ap)

    return map_score


def report_eval(qrels, score_vals):
    q_ids = set(score_vals['ds']["query"])
    q_ids = list(sorted(list(q_ids)))
    
    report_path = os.path.join("Report.txt")
    if os.path.exists(report_path):
        os.remove(report_path)
     
    f = open(report_path, mode= 'w')
    
    q_id = 0
    for sheet in qrels:
        q = q_ids[q_id]
        q_id+=1
        qrel = qrels[sheet].loc[qrels[sheet]["Topic Id"] == q]
        df_true = qrel["Is Relevant"]
        f.write(f"------- Query: {q} -------\n\n")
        for func in score_vals:
            rank = score_vals[func]
            df_pred = rank["is_rel"]
            
            pa5 = mean_average_precision(df_true, df_pred, 5)
            pa10 = mean_average_precision(df_true, df_pred, 10)
            pa20 = mean_average_precision(df_true, df_pred, 20)
            pa30 = mean_average_precision(df_true, df_pred, 30)
            map_val = mean_average_precision(df_true, df_pred)
            
            entry = f"{func}\nP@5: {pa5}\nP@10: {pa10}\nP@20: {pa20}\nP@30: {pa30}\nMAP: {map_val}\n\n"
            f.write(entry)
    
    f.close()           
            
            
            
        
        
    
if __name__ == "__main__":
    qrels = load_qrels()
    score_vals = load_score_values()
    score_vals = classify_scores(qrels, score_vals)
    report_eval(qrels, score_vals)    
    