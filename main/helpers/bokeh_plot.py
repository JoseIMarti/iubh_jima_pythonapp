from bokeh.plotting import figure,save,output_file
from bokeh.layouts import column,row,gridplot
import pandas as pd

class bokeh_plot():
    def __init__(self,df_object,n_charts_per_row=5,filename='ideal.html',df_ideal='', *args, **kwargs):
        self.df_object = df_object
        self.df_ideal = df_ideal
        self.filename = filename
        stringline = ""
        row_list = []
        layout_list = []
        for count,item in enumerate(df_object.columns[1:], start=1):
            stringline=stringline+"p"+str(count)+' = figure(plot_width=240, plot_height=200, title="'+"x" +" vs "+item+'")\n'
            stringline=stringline+"p"+str(count)+'.xgrid.grid_line_color = None\n'
            stringline=stringline+"p"+str(count)+'.circle(x="'+"x"+'", y="'+item+'", size=5, alpha=0.4, source=df_object)\n'

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
        exec(stringline)
