

from helpers.ddbb import list_databases,database
from helpers.data import data,ideal,model,test
from helpers.bokeh_plot import bokeh_plot

import sys
import pandas as pd
from PyQt5.QtCore import QDir,QUrl
from PyQt5.QtWidgets import QDialog,QWidget,QFormLayout,QHBoxLayout,QVBoxLayout
from PyQt5.QtWidgets import QMainWindow, QPushButton,QLineEdit, QFileDialog, QRadioButton
from PyQt5.QtWidgets import QComboBox,QMessageBox,QGridLayout,QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView

from PyQt5.QtWidgets import QDesktopWidget

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Python Programming Assignment")
        self.window=QWidget()
        self.filename="ideal.html"
        self.ddbb_dir_list = []
        self.ddbb_object = []
        self.engine = []
        self.ddbb = []
        
        self.plotdata = []
        self.ideal_data = []
        self.model_data = []
        
        self.l_input_dir=QLabel(self)
        self.l_input_dir.setText("Select DDBB working directory")
        self.input_dir = QLineEdit(self)
        self.input_dir.setEnabled(False)
        self.button_dir = QPushButton(self,text="...")
        self.button_dir.clicked.connect(lambda: self.choose_dir(self.input_dir,"dir"))
        
        self.button_dialog = QPushButton(self, text="New DDBB")
        self.button_dialog.clicked.connect(self.show_dialog)
        self.l_input_ddbb = QLabel(self)
        self.l_input_ddbb.setText("Choose among available DDBBs")
        self.input_ddbb = QComboBox(self)
        #self.input_ddbb.activated[str].connect(self.sel_ddbb)
        
        
        self.l_input_ideal = QLabel(self)
        self.l_input_ideal.setText("Select Ideal Functions dataset")
        self.input_ideal = QLineEdit(self)
        self.input_ideal.setEnabled(False)
        self.input_ideal.textChanged.connect(lambda: self.pd_ideal(self.input_ideal,'ideal'))
        self.button_ideal = QPushButton(self,text="...")
        self.button_ideal.clicked.connect(lambda: self.choose_dir(self.input_ideal))
        
        self.l_input_train = QLabel(self)
        self.l_input_train.setText("Select Train dataset")
        self.input_train = QLineEdit(self)
        self.input_train.setEnabled(False)
        self.input_train.textChanged.connect(lambda: self.pd_ideal(self.input_train,'train'))
        self.button_train = QPushButton(self,text="...")
        self.button_train.clicked.connect(lambda: self.choose_dir(self.input_train))
        
        self.l_input_test = QLabel(self)
        self.l_input_test.setText("Select Test dataset")
        self.input_test = QLineEdit(self)
        self.input_test.setEnabled(False)
        self.input_test.textChanged.connect(lambda: self.pd_ideal(self.input_test,'test'))
        self.button_test = QPushButton(self,text="...")
        self.button_test.clicked.connect(lambda: self.choose_dir(self.input_test))
        
        self.plotdata = WebPage(self.filename)
        self.plotdata.resize(1040, 780)

        
        self.applicationLayout = QVBoxLayout(self)
        directoryLayout = QHBoxLayout()
        databaseLayout = QHBoxLayout()
        idealdataLayout = QHBoxLayout()
        traindataLayout = QHBoxLayout()
        testdataLayout = QHBoxLayout()
        plotLayout = QHBoxLayout()
        radioBLayout = QVBoxLayout()
        
        self.radiobutton_ideal = QRadioButton("Ideal Functions")
        self.radiobutton_ideal.setChecked(True)
        self.radiobutton_ideal.option_choice = "ideal"
        self.radiobutton_ideal.toggled.connect(self.onClicked)
        radioBLayout.addWidget(self.radiobutton_ideal)

        self.radiobutton_train = QRadioButton("Train Dataset")
        self.radiobutton_train.option_choice = "train"
        self.radiobutton_train.toggled.connect(self.onClicked)
        radioBLayout.addWidget(self.radiobutton_train)

        self.radiobutton_test = QRadioButton("Test Dataset")
        self.radiobutton_test.option_choice = "test"
        self.radiobutton_test.toggled.connect(self.onClicked)
        radioBLayout.addWidget(self.radiobutton_test)
        
        directoryLayout.addWidget(self.l_input_dir)
        directoryLayout.addWidget(self.input_dir)
        directoryLayout.addWidget(self.button_dir)
        
        databaseLayout.addWidget(self.button_dialog)
        databaseLayout.addWidget(self.l_input_ddbb)
        databaseLayout.addWidget(self.input_ddbb)
        
        idealdataLayout.addWidget(self.l_input_ideal)
        idealdataLayout.addWidget(self.input_ideal)
        idealdataLayout.addWidget(self.button_ideal)
        
        traindataLayout.addWidget(self.l_input_train)
        traindataLayout.addWidget(self.input_train)
        traindataLayout.addWidget(self.button_train)
        
        testdataLayout.addWidget(self.l_input_test)
        testdataLayout.addWidget(self.input_test)
        testdataLayout.addWidget(self.button_test)
        
        plotLayout.setContentsMargins(0, 0, 0, 0)
        radioBLayout.addStretch(0)
        plotLayout.addLayout(radioBLayout)
        
        self.applicationLayout.addLayout(directoryLayout)
        self.applicationLayout.addLayout(databaseLayout)
        self.applicationLayout.addLayout(idealdataLayout)
        self.applicationLayout.addLayout(traindataLayout)
        self.applicationLayout.addLayout(testdataLayout)
        self.applicationLayout.addLayout(plotLayout)
        self.applicationLayout.addStretch(1)
        self.applicationLayout.addWidget(self.plotdata)
        self.applicationLayout.addStretch(0)
        
        self.window.setLayout(self.applicationLayout)
                
        #sizeScreen = QDesktopWidget().screenGeometry(-1)
        #self.window.setFixedSize(sizeScreen.width()*0.9, sizeScreen.height()*0.9)
        self.window.show()
    
    def choose_dir(self,object_text,mode="file"):
        self.dir = QFileDialog()
        object_text.setEnabled(True)
        dir_response=""
        filter=""
        if mode == "dir":
            dir_response=self.dir.getExistingDirectory(self, 'Select DDBB working directory')
            if dir_response != "":
                self.ddbb_dir_list = list_databases(dir_response)
                self.input_ddbb.clear()
                self.input_ddbb.addItems(self.ddbb_dir_list)
                self.input_ddbb.setCurrentIndex(self.input_ddbb.count() - 1 )
                self.ddbb_object = database(str(dir_response),str(self.input_ddbb.currentText()))
        else:
            dir_response,filter=self.dir.getOpenFileName(self, 'Select csv file',filter='*.csv')
        if dir_response != "":
            object_text.setText(dir_response)
            object_text.setEnabled(False)
            #print(data.read_file(object_text.text()))
    
    def show_dialog(self):
        if self.input_dir.text():
            dialog = Dialog(self)
            temp_engine = ""
            if str(dialog.ddbb_full_name) != "" and self.ddbb_dir_list.count(str(dialog.ddbb_full_name)) == 0:
                self.ddbb_dir_list.append(str(dialog.ddbb_full_name))
                self.input_ddbb.clear()
                self.input_ddbb.addItems(self.ddbb_dir_list)
                self.input_ddbb.setCurrentIndex(self.input_ddbb.count() - 1 )
                #jima 08_12_2020
                self.ddbb_object = database(str(self.input_dir.text()),str(self.input_ddbb.currentText()))
                self.ddbb = self.ddbb_object.recreate_ddbb(self.ddbb_object.ddbb_path,self.ddbb_object.engine)
                QMessageBox.information(self,"Information","New database "+str(dialog.ddbb_full_name)+ " has been created")
                return True
            else:
                QMessageBox.warning(self, "Warning","You cannot create duplicate DDBBs")
        else:
            QMessageBox.warning(self, "Warning","You need to choose a DDBB working directory")
        return False
    
    def sel_ddbb(self):
        print("Hi database selection")
        #jima 8_12_2020
        self.ddbb_object = database(str(self.input_dir.text()),str(self.input_ddbb.currentText()))
        print("Bye database selection")
        #print(self.input_ddbb.currentText())
        
    def pd_ideal(self,object,type_df=''):
        if object.text():
            df_object = data(object.text(),type_df)
            if(type_df != df_object.type_df):
                QMessageBox.warning(self, "Warning","Check your csv choice. The number of columns doesn't match with the expected lenght for this kind of data. Data will still be available")
            else:
                if df_object.data_type_valid:
                    #Escribir un try/catch para escritura en base de datos, seguramente en ddbb.py
                    self.ddbb_object.load_to_ddbb(df_object.df,df_object.type_df,self.ddbb_object.engine)
                    self.filename=str(type_df)+".html"
                    datafromquery = self.ddbb_object.read_from_ddbb(query="SELECT * FROM " + df_object.type_df,con = self.ddbb_object.engine)
                    if type_df in ['ideal','train']:
                        if type_df == 'ideal':
                            bokeh_plot(datafromquery)
                            self.ideal_data = ideal(object.text(),type_df)
                            self.radiobutton_ideal.setChecked(True)
                        else:
                            bokeh_plot(datafromquery,2,self.filename)
                            self.model_data = model(object.text(),type_df)
                            self.radiobutton_train.setChecked(True)
                    else:
                            if self.model_data != [] and self.ideal_data != []:
                                print("READY")
                                output_model = self.model_data.lestSquareCriterion(self.ideal_data.df)
                                #print(output_model['df'].columns)
                                self.test_data = test(object.text(),type_df)
                                self.test_data.maxDeviationCriterion(output_model)
                                
                                prueba = self.test_data.lestSquareCriterion(output_model['df'])
                                #print((prueba))
                                #print(prueba)
                                #prueba = self.test_data.lestSquareCriterion(self.ideal_data)
                                #for model_df in output_model['ideal_cols']:
                                #    prueba = self.test_data.lestSquareCriterion(model_df)
                                    #print(prueba)
                                #print(prueba)
                                
                            else:
                                print("Load files")
                            
                            bokeh_plot(datafromquery,1,self.filename)
                            
                            self.test_data = df_object
                            self.radiobutton_test.setChecked(True)
                    self.plotdata.load_new_chart(self.filename)
                else:
                    print("Please, review the data contained in the provided file. Some columns may contain non-numerica data")

    def onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.filename="test.html"
            if radioButton.option_choice == "ideal":
                #self.ideal_data = self.ddbb_object.read_from_ddbb(query="SELECT * FROM " + radioButton.option_choice,con = self.ddbb_object.engine)
                self.filename='ideal.html'
            elif radioButton.option_choice == "train":
                #self.train_data = self.ddbb_object.read_from_ddbb(query="SELECT * FROM " + radioButton.option_choice,con = self.ddbb_object.engine)
                self.filename='train.html'
            self.plotdata.load_new_chart(self.filename)
            print("Option is %s" % (radioButton.option_choice))


class Dialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(Dialog, self).__init__(*args, **kwargs)
        self.ddbb_full_name = ""
        self.setWindowTitle("Creating New Database")
        self.setFixedSize(400, 200)
        
        self.combo_ext_list=QComboBox(self)
        self.combo_ext_list.addItem(".db")
        self.text_dbname = QLineEdit(self)
        
        self.formLayout = QFormLayout(self)
        self.formLayout.addRow("New Database Name:",self.text_dbname)
        self.formLayout.addRow("Database Extension",self.combo_ext_list)
        
        self.bttn_save= QPushButton("Save")
        self.bttn_save.clicked.connect(self.onSave)
        self.bttn_cancel= QPushButton("Cancel")
        self.bttn_cancel.clicked.connect(self.onCancel)
        self.formLayout.addRow(self.bttn_save,self.bttn_cancel)
        self.setLayout(self.formLayout)
        self.exec_()
        
    def onSave(self):
        if self.text_dbname.text() == "":
            QMessageBox.warning(self, "Warning","Insert a new database name")
            return
        
        self.ddbb_full_name =str(self.text_dbname.text())+str(self.combo_ext_list.currentText())
        self.close()
        return self.ddbb_full_name

    def onCancel(self):
        QMessageBox.warning(self, "Warning","No New Database had been created")
        self.close()

class WebPage(QWebEngineView):
    def __init__(self,filename=""):
        QWebEngineView.__init__(self)
        path = QDir.current().filePath(filename)
        self.load(QUrl.fromLocalFile(path))
        self.loadFinished.connect(self._on_load_finished)
    
    def load_new_chart(self,filename):
        path = QDir.current().filePath(filename)
        self.load(QUrl.fromLocalFile(path))
        self.loadFinished.connect(self._on_load_finished)

    def _on_load_finished(self):
        print("Finished Loading")
