from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pathlib import Path
import pandas as pd

Base = declarative_base()

class database():
    def __init__(self, ddbb_path = '', dbname = 'ppython.db', echo = True):
        self.dbname = dbname
        self.ddbb_path = '//'+ddbb_path+'/'+dbname
        self.url = 'sqlite:'+self.ddbb_path
        self.engine = create_engine(self.url, echo = echo)
        print(self.engine)
        
    def recreate_ddbb(self,ddbb_path,engine):
        if Path(ddbb_path).exists():
            Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        return True
        
    def load_to_ddbb(self,df,table_name,engine,if_exists='replace',index=False,chunksize=400):
        return df.to_sql(table_name,engine,if_exists = if_exists,index = index,chunksize = chunksize)
    
    def read_from_ddbb(self,con,query=""):
        return pd.read_sql(query,con)
    
def list_databases(dir,ext=".db"):
    import os
    ddbb=[]
    if dir != "":
        for file in os.listdir(dir):
            if file.endswith(ext):
                ddbb.append(file)
        return ddbb
