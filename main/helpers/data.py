import pandas as pd
import math
from ddbb import list_databases,database

class data():
    """Generic Data class created in order to deal with the different kinds of Data Objects required for the project."""

    def __init__(self, filepath, declared_type_df):
        self.filepath = str(filepath)
        self.df = pd.read_csv(filepath)
        self.columns = list(self.df.columns)
        self.n_columns = len(self.df.columns)
        self.type_df = str(self.find_type_of_df(self.n_columns))
        self.data_type_valid = self.df_is_numeric(self.df)
        if self.type_df != 'test':
            self.df = self.df.sort_values(by=self.df.columns[0], ascending=True)
        
    def df_is_numeric(self,df):
        temp_data = df.apply(lambda s: pd.to_numeric(s, errors="coerce").notnull().all()).to_frame().fillna(False)
        temp_data.columns = ["bool_col"]
        if len(df.columns) == temp_data["bool_col"].sum():
            return True
        return False
        
    def find_type_of_df(self,len_columns):
        switcher={
            2:'test',
            5:'train',
            51:'ideal'
        }
        return switcher.get(len_columns,'special')

class ideal(data):
    def __init__(self, filepath, declared_type_df):
        super().__init__(filepath, declared_type_df)

class model(data):
    def __init__(self, filepath, declared_type_df):
        super().__init__(filepath, declared_type_df)
        
    def lestSquareCriterion(self,ideal_df):
        difference = []
        pow = []
        total_sum = []
        ideal_cols_names = [ideal_df.columns[0]]
        ideal_cols = []
        deviation = []
        print(type(ideal_df))
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
    def __init__(self, filepath, declared_type_df):
        super().__init__(filepath, declared_type_df)
    
    def maxDeviationCriterion(self,model):
        df = pd.DataFrame(self.df)
        df_model_collection = model['ideal_cols']
        dev_model_collection = model['deviation']

        for i, model_df in enumerate(df_model_collection):
        
            model_df = pd.DataFrame(model_df)
            temp_self_df = df.merge(model_df,how='left',left_on=df.columns[0],right_on=model_df.columns[0])
            temp_self_df = temp_self_df.dropna()
            temp_self_df['abs_diff'] = abs(temp_self_df.iloc[:,1]-temp_self_df.iloc[:,2])

            for j, row in temp_self_df.iterrows():
                print("Write into database")
                print(row)
                print("x: "+ str(row[0])+" ,y: " + str(row[1]) + " ,delta: "+str(row[3]) +" ,col: " + str(model_df.columns[1]))
                if row['abs_diff'] > dev_model_collection[i]:
                    break
