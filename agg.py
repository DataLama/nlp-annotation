import schedule
import json
import sqlite3
import pandas as pd
import sqlite3
from datetime import datetime


def reader(table, p_id):
    with sqlite3.connect('/doccano/app/db.sqlite3') as conn:
        cur = conn.cursor()
        sql = f'SELECT * FROM {table} WHERE project_id={p_id};'
        return pd.read_sql_query(sql, conn)
    
    
def job(p_id):
    #### read tables subsetted by projects
    api_label = reader('api_label', p_id)
    api_document = reader('api_document', p_id) 
    with sqlite3.connect('/doccano/app/db.sqlite3') as conn:
        cur = conn.cursor()
        sql = f'SELECT * FROM api_documentannotation;'
        api_documentannotation = pd.read_sql_query(sql, conn)
    
    #### merge and select and pivot (api_label, api_documentannotation) -> labeled_doc
    labeled_doc = pd.merge(api_documentannotation, api_label, left_on ='label_id', right_on = 'id').loc[:,['document_id','updated_at_x','text']].sort_values('document_id') # merge and select
    labels = labeled_doc.pivot(index='document_id',columns='text',values='updated_at_x').applymap(lambda x:0 if type(x)==float else 1)
    updated_at = labeled_doc.pivot(index='document_id',columns='text',values='updated_at_x').apply(lambda x: x.dropna().max(),axis=1)
    
    ## split labels
    check = labels.loc[:,['Check']]
    multilabel = labels.loc[:,['MultiLabel']]
    c1 = labels.loc[:,[x for x in labels.columns if 'c1' in x]]
    c2 = labels.loc[:,[x for x in labels.columns if 'c2' in x]]
    
    # concat dfs
    df_list = [check, multilabel, c1, c2] 
    # concat updates
    df_list = [pd.concat((df,updated_at), axis = 1) for df in df_list]
    
    #### merge and select (labeled_doc, api_document)
    document_doc = pd.concat((api_document.loc[:,['id','text']], api_document.meta.apply(lambda x: json.loads(x)['CUR_SEQNO'])),axis=1)
    df_list = [pd.merge(df, document_doc, right_on='id', left_index=True).drop('id', axis=1).iloc[:,[-1,-2]+list(range(df.shape[1]))] for df in df_list]
    df_list = [df.rename(mapper={'meta':'CUR_SEQNO',0:'updated_at'},axis=1) for df in df_list]

    
    #########----------------------------- change this directoreis.
    df_list[0].loc[df_list[0].Check==1].to_csv(f'/data/ANNOTATION/jhna/Check-{datetime.now().strftime("%m-%d")}.csv',index=False) # check
    df_list[1].loc[df_list[1].MultiLabel==1].to_csv(f'/data/ANNOTATION/jhna/MultiLabel-{datetime.now().strftime("%m-%d")}.csv',index=False) # multilabel
    df_list[2].to_csv(f'/data/ANNOTATION/jhna/c1-{datetime.now().strftime("%m-%d")}.csv',index=False) # c1
    df_list[3].to_csv(f'/data/ANNOTATION/jhna/c2-{datetime.now().strftime("%m-%d")}.csv',index=False) # c2
    print('SUCCESS!!!')
    
project_num = 1 # 프로젝트가 다를 경우 수정!!
    
if __name__ == '__main__':
    job(project_num)