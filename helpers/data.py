import pandas as pd
import numpy as np
import math
from csv import reader
from helpers.ddbb import list_databases,database

class data():
    """Generic Data class created in order to deal with the different kinds of Data Objects required for the project."""

    def __init__(self, filepath, declared_type_df):
        self.filepath = str(filepath)
        self.declared_type_df = declared_type_df
        self.df = self.read_data()
        self.columns = list(self.df.columns)
        self.n_columns = len(self.df.columns)
        self.type_df = str(self.find_type_of_df())
        self.data_type_valid = self.df_is_numeric()
        if self.type_df != 'test':
            self.df = self.df.sort_values(by=self.df.columns[0], ascending=True)
        
    def read_data(self):
        frame = None
        if self.declared_type_df == 'test':
            frame = pd.read_csv(self.filepath,nrows = 5)
        else:
            frame = pd.read_csv(self.filepath)
        return frame
    
    def df_is_numeric(self):
        temp_data = self.df.apply(lambda s: pd.to_numeric(s, errors="coerce").notnull().all()).to_frame().fillna(False)
        temp_data.columns = ["bool_col"]
        if len(self.df.columns) == temp_data["bool_col"].sum():
            return True
        return False
        
    def find_type_of_df(self):
        switcher={
            2:'test',
            5:'train',
            51:'ideal'
        }
        return switcher.get(self.n_columns,'special')

class ideal(data):
    def __init__(self,filepath,type_df):
        super().__init__(filepath, type_df)

class model(data):
    def __init__(self,filepath,type_df):
        super().__init__(filepath, type_df)
        
    def lestSquareCriterion(self,ideal_df):
        difference = []
        pow = []
        total_sum = []
        ideal_cols_names = [ideal_df.columns[0]]
        ideal_cols = []
        deviation = []
        df_result = pd.DataFrame()
        
        for col_self in self.columns[1:]:
            
            temp_total_sum = 0
            difference.append(0)
            pow.append(0)
            deviation.append(0)
            total_sum.append(0)
            ideal_cols_names.append(ideal_df.columns[1])
            ideal_cols.append(ideal_df.iloc[1])
                        
            for col_ideal in ideal_df.columns[1:]:
                
                temp_self_df = self.df[[self.columns[0],col_self]]
                temp_ideal_df = ideal_df[[ideal_df.columns[0],col_ideal]]
                temp_self_df = temp_self_df.merge(temp_ideal_df,how='left',left_on=temp_self_df.columns[0] ,right_on=temp_ideal_df.columns[0])
                temp_self_df['difference'] = temp_self_df.iloc[:,1]-temp_self_df.iloc[:,2]
                temp_self_df['pow'] = temp_self_df['difference'].pow(2)

                if temp_total_sum == 0:
                    temp_total_sum = temp_self_df['pow'].sum()
                    difference[-1] = temp_self_df['difference']
                    pow[-1] = temp_self_df['pow']
                    total_sum[-1] = temp_total_sum
                    deviation[-1] = abs(max(enumerate(difference[-1]), key = lambda x: abs(x[1]))[1])*math.sqrt(2)
                    ideal_cols_names[-1] = col_ideal
                    ideal_cols[-1] = temp_self_df.iloc[:,[0,2]]

                else:
                    if temp_self_df['pow'].sum() < temp_total_sum:
                        temp_total_sum = temp_self_df['pow'].sum()
                        difference[-1] = temp_self_df['difference']
                        pow[-1] = temp_self_df['pow']
                        total_sum[-1] = temp_total_sum
                        deviation[-1] = abs(max(enumerate(difference[-1]), key = lambda x: abs(x[1]))[1])*math.sqrt(2)
                        ideal_cols_names[-1] = col_ideal
                        ideal_cols[-1] = temp_self_df.iloc[:,[0,2]]
        
        df_result = pd.DataFrame(ideal_df,columns = ideal_cols_names)
        
        Dict = dict({'df':df_result,'ideal_cols_names': ideal_cols_names, 'ideal_cols': ideal_cols,'difference':difference,'pow':pow,'total_sum':total_sum,'deviation':deviation})

        return Dict
        
class test(model):
    def __init__(self,filepath, type_df):
        super().__init__(filepath, type_df)
        
    def addElements(self,df,list):
        return df.append({df.columns[0]:list[0],df.columns[1]:list[1]},ignore_index=True)
    
    def maxDeviationCriterion(self,model,ddbb_object):
        
        df_model_collection = model['df']
        dev_model_collection = model['deviation']
        

        with open(self.filepath, 'r') as test_obj:
            test_reader = reader(test_obj)
            for index,test_row in enumerate(test_reader):
                if index > 0:
                    df =  pd.DataFrame(columns = self.df.columns) 
                    df = self.addElements(df,test_row)
                    for column in df.columns:
                        df[column] = df[column].astype(float)    
                    
                    temp_self_df = df.merge(df_model_collection,how='left',left_on=df.columns[0],right_on=df_model_collection.columns[0])
                    start = -len(df_model_collection.columns)+1
                    end = len(temp_self_df.columns)
                    for temp_index,temp_column in enumerate(temp_self_df.columns[start:end]):
                        temp_self_df['abs_diff'+str(temp_index)] = abs(temp_self_df.iloc[:,1]-temp_self_df.iloc[:,int(2+temp_index)])
                        
                        if temp_self_df['abs_diff'+str(temp_index)][0] <= dev_model_collection[temp_index]:
                            print("New entry in Database")
                            print(temp_self_df)
                            #print("x: "+ str(row[0]))
                            #print("x: "+ str(row[0])+" ,y: " + str(row[1]) +" ,dev_model: "+str(dev_model_collection[i]) +" ,delta: "+str(row[3]) +" ,col: " + str(model_df.columns[1]))
                            
                        
        
        


                    #print("Index: "+str(index))
                    #print(df)
                    #df_model_collection = model['ideal_cols']
                    #dev_model_collection = model['deviation']
            
                    #for model_index, model_df in enumerate(df_model_collection):
                    #    print("Modelo")
                        #print(model_df)
                        #model_df = pd.DataFrame(model_df)
                        #temp_self_df = df.merge(model_df,how='left',left_on=df.columns[0],right_on=model_df.columns[0])
                    #temp_self_df = temp_self_df.dropna()
                    #temp_self_df['abs_diff'] = abs(temp_self_df.iloc[:,1]-temp_self_df.iloc[:,2])
        
                    #for j, row in temp_self_df.iterrows():
        
                    #    if row['abs_diff'] <= dev_model_collection[i]:
                    #        print("Write into database")
                    #        print(row)
                    #        print("x: "+ str(row[0])+" ,y: " + str(row[1]) +" ,dev_model: "+str(dev_model_collection[i]) +" ,delta: "+str(row[3]) +" ,col: " + str(model_df.columns[1]))
                            
