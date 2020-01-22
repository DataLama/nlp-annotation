import json
import numpy as np
import pandas as pd
import sqlite3 
from sqlalchemy import create_engine
from datetime import datetime

#### function
def api_document_update(data_dir, db, p_Num):
    print(f'Set the document for project{p_Num}')
    #### load_dataset using for uploading
    dataset = pd.read_csv(data_dir)
    dataset = dataset.loc[dataset.CUR_SEQNO.drop_duplicates().index].reset_index(drop=True) #CUR_CTT 중복 제거
    dataset = dataset.loc[~dataset.CUR_CTT.isna()].reset_index(drop=True) # VOC NA제거.
    
    #### get data from DB
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        sql = 'SELECT * FROM api_document;'
        api_doc = pd.read_sql_query(sql, conn) 
        
    #### UPDATE
    updates = pd.DataFrame(columns=api_doc.columns)
    updates.id = range(1,1+len(dataset)) if len(api_doc) == 0 else range(api_doc.id.iloc[-1]+1, api_doc.id.iloc[-1]+1+dataset.shape[0]) # id는 [기존 디비의 마지막+1, 새로운 데이터의 수)
    updates.text = dataset.CUR_CTT
    updates.meta = [dataset.iloc[i][['YEAR','MONTH','CUR_SEQNO','CLASS','CLASS2','CLASS3','CLASS4','기타사항']].to_json(force_ascii=False) for i in range(len(dataset))]
    updates.created_at = [datetime.now().strftime("%Y-%m-%d %H:%M:%S") for i in range(updates.shape[0])]
    updates.updated_at = [datetime.now().strftime("%Y-%m-%d %H:%M:%S") for i in range(updates.shape[0])]
    updates.project_id = [p_Num]*updates.shape[0]
    updates.annotations_approved_by_id = [None]*updates.shape[0]
    
    ## type conversion
    updates.id = updates.id.astype(np.int32)
    updates.project_id = updates.project_id.astype(np.int32)
    
    #### INSERT DATA
    engine = create_engine(f"sqlite:///{db}")
    updates.to_sql(name = 'api_document',con=engine,if_exists='append', index=False)
    
    print(f'{data_dir.split("/")[-1]} is successfully uploaded to api_document')
    
    
    
####----------------------------- Define variables -----------------------------
data_dir = './dataset/product.csv' #라벨할 데이터가 바뀌면 변경.
db = '/doccano/app/db.sqlite3'
p_num = 1 #새로운 프로젝트 생성시 p_num을 변경.
####----------------------------------------------------------------------------

# run
if __name__ == '__main__':
    api_document_update(data_dir, db, p_num)