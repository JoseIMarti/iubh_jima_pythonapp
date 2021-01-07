from bokeh.plotting import figure,save,output_file
from bokeh.layouts import column,row,gridplot
from bokeh.models import Band,ColumnDataSource

import pandas as pd
import math

class bokeh_plot():
    def __init__(self,df_object,n_charts_per_row=5,filename='ideal.html',df_ideal='', **kwargs):
        self.df_object = df_object
        self.df_ideal = df_ideal
        self.filename = filename
        first_col_ind = 1
        output_model_cols = None
        delta = pd.DataFrame()
        diff_df = pd.DataFrame()
        output_model_df = pd.DataFrame()
        output_model_dev = None
        output_model_cols = None
        if 'type_df' in kwargs:
            first_col_ind = 0
            delta = kwargs.get('delta',"default value")
            delta = delta.reset_index()
            diff_df = delta
            output_model_cols = kwargs.get('output_model',"default value")['ideal_cols_names']
            output_model_df = kwargs.get('output_model',"default value")['df']
            output_model_dev =  kwargs.get('output_model',"default value")['deviation']

        
        stringline = ""
        row_list = []
        layout_list = []
        for count,item in enumerate(df_object.columns[first_col_ind:], start=1):
            stringline=stringline+"p"+str(count)+' = figure(plot_width=240, plot_height=200, title="'+"x" +" vs "+item+'")\n'
            stringline=stringline+"p"+str(count)+'.xgrid.grid_line_color = None\n'
            stringline=stringline+"p"+str(count)+'.circle(x="'+"x"+'", y="'+item+'", size=5, alpha=0.4, source=df_object)\n'
            if not delta.empty:
                temp_bands = df_object[item].to_frame()
                temp_bands = temp_bands.merge(delta[['x',item]],how='left',left_on='x', right_on='x')
                temp_bands = temp_bands.merge(output_model_df[['x',item]], how='left',left_on='x', right_on='x')
                index=output_model_cols.index(item)-1
                newcolname = str(item)+str('_delta')

                temp_bands.columns = ['x', newcolname, 'delta',item]
                diff_df[item] = temp_bands[item]
                diff_df["upper"+str(item)]=temp_bands[item]+math.sqrt(2)*output_model_dev[index]
                diff_df["lower"+str(item)]=temp_bands[item]-math.sqrt(2)*output_model_dev[index]
                diff_df[newcolname] = temp_bands[newcolname]
                diff_df['dev'+str(count)] = temp_bands[newcolname] - temp_bands['delta']

                stringline=stringline+"p"+str(count)+'.segment(x0="x",x1="x",y0="'+newcolname+'",y1="dev'+str(count)+'", source=diff_df,color="#F4A582")\n'
                stringline=stringline+"p"+str(count)+'.line(x="'+"x"+'", y ="'+item+'", alpha=0.8, source=diff_df,color="#F4A582")\n'
                stringline=stringline+"p"+str(count)+'.line(x="'+"x"+'", y ="'+"lower"+str(item)+'", alpha=0.8, source=diff_df,color="green")\n'
                stringline=stringline+"p"+str(count)+'.line(x="'+"x"+'", y ="'+"upper"+str(item)+'", alpha=0.8, source=diff_df,color="red")\n'
                

            if (((count % n_charts_per_row) == 0) or (int(n_charts_per_row)==len(df_object.columns[1:]))):
                lrow_list = list(range(int(count-n_charts_per_row+1),int(count+1),1))
                for element in lrow_list:
                    row_list.append(str("p"+str(element)))
                row_list.append(str("]"))
            if (((int(count-1) % n_charts_per_row) == 0) and (1!=len(df_object.columns[1:]))):
                row_list.append(str(str("row") +str(count) +str(" = [")))
                layout_list.append(str(str("row") +str(count)))
            elif 1==len(df_object.columns[1:]):
                row_list.insert(0,str(str("row") +str(count) +str(" = [")))
                layout_list.append(str(str("row") +str(count)))
        
        row_list = ','.join(map("'{0}'".format, row_list))
        row_list = row_list.replace("[',","[").replace(",']'","]\n").replace(",'row","row").replace("'row","row").replace("'","")

        layout_list="layout =gridplot([" + ','.join(map("'{0}'".format, layout_list)) +"])\n"
        layout_list=layout_list.replace("'","")
        stringline=stringline+row_list
        stringline=stringline+layout_list
        stringline=stringline+"output_file('"+str(filename)+"')\n"
        stringline=stringline+"save(layout)"
        print(stringline)
        exec(stringline)
