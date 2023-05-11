import pandas as pd
import glob

def ne_report():
    
    # Read in Item List Export
    file_pattern = 'C:\\Users\\ccrin\\Desktop\\working_files\\NE Item List*.csv'
    file_path = glob.glob(file_pattern)[0]
    df = pd.read_csv(file_path)
    
    # Newegg Standalone
    df_standalone = df[(df['Activation Mark']==True) &
            (df['Available Quantity']>0) &
            (df['Item Condition']=='New') &
            (~df['Seller Part #'].str.contains('BNDL_'))]
    

def neb_report():
    
    # Read in Item List Export
    file_pattern = 'C:\\Users\\ccrin\\Desktop\\working_files\\NEB Item List*.csv'
    file_path = glob.glob(file_pattern)[0]
    df = pd.read_csv(file_path)

    # Newegg Business Standalone
    df_standalone = df[(df['Activation Mark']==True) &
            (df['Available Quantity']>0) &
            (df['Item Condition']=='New') &
            (~df['Seller Part #'].str.contains('BNDL_'))]
