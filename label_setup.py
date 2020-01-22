import numpy as np
import pandas as pd
import sqlite3 
from sqlalchemy import create_engine
from datetime import datetime

#### function
def api_label_update(voc_class, db , p_Num):
    print(f'Set the labels for project{p_Num}')
    #### load api_label
    with sqlite3.connect('/doccano/app/db.sqlite3') as conn:
        cur = conn.cursor()
        sql = 'SELECT * FROM api_label;'
        api_label = pd.read_sql_query(sql, conn) 
    
    #### UPDATES
    # 현재 시간
    NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 기본 label 정의 
    updates = [('MultiLabel',None, None,'#b34a8d','#ffffff',NOW, NOW, p_Num),
                   ('Check',None, None,'#d31d1a', '#ffffff',NOW, NOW, p_Num)]

    # 분류1 관련 label 추가 
    updates += [(f'c1-{l}', None, None, '#0cb2c6', '#000000', NOW, NOW,p_Num) for l in voc_class.분류1.unique()]
    # 분류2 관련 label 추가 
    updates += [(f'c2-{l}', None, None, '#b0ac3f', '#000000', NOW, NOW,p_Num) for l in voc_class.분류2.unique()]
    # id 추가 후 df 변환
    updates = pd.DataFrame([(i+1,*x) for i,x in enumerate(updates)])
    updates.columns = api_label.columns
    
    #### INSERT DATA
    engine = create_engine(f"sqlite:///{db}")
    updates.to_sql(name = 'api_label',con=engine,if_exists='append', index=False)
    print(f'SUCCESS!')
    
    
    
#### Define variables
voc_class = pd.read_csv('상담VOC_분류체계.csv')
db = '/doccano/app/db.sqlite3'
p_num = 1  # 새로운 프로젝트 생성시 p_num을 변경.

# ####----------------------------- 클래스 일부만 사용할 경우 -----------------------------
# sub_class = voc_class.loc[voc_class.분류1.apply(lambda x: '제품' in x)].reset_index(drop=True)
# ####-------------------------------------------------------------------------------


# run
if __name__ == '__main__':
    api_label_update(voc_class, db, p_num)
#     api_label_update(sub_class, db, p_num)
