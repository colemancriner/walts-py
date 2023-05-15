import pandas as pd
import glob

def ne_report():
    
    # Read in Item List Export
    file_pattern = 'C:\\Users\\ccrin\\Desktop\\working_files\\NE Item List*.csv'
    file_path = glob.glob(file_pattern)[0]
    df = pd.read_csv(file_path)
    
    # Newegg errors
    df_errors = df[(df['Activation Mark']==False) &
            (df['Available Quantity']>0)]
    
    df_errors['Restricted Msg'] = ['' for i in df_errors['Activation Mark']]
    df_errors['Errors'] = ['' for i in df_errors['Activation Mark']]
    df_errors = df_errors.loc[:,['Seller Part #','Restricted Msg','Errors']]


    # create an excel writer object
    with pd.ExcelWriter("C:\\Users\\ccrin\\Desktop\\NE Catalog Report.xlsx") as writer:
    
        # use to_excel function and specify the sheet_name and index
        # to store the dataframe in specified sheet
        df.to_excel(writer, sheet_name='Item List', index=False)
        df_errors.to_excel(writer, sheet_name='Errors', index=False)
    

def neb_report():
    
    # Read in Item List Export
    file_pattern = 'C:\\Users\\ccrin\\Desktop\\working_files\\NEB Item List*.csv'
    file_path = glob.glob(file_pattern)[0]
    df = pd.read_csv(file_path)

    # Newegg Business errors
    df_errors = df[(df['Activation Mark']==False) &
            (df['Available Quantity']>0)]
    
    df_errors['Restricted Msg'] = ['' for i in df_errors['Activation Mark']]
    df_errors['Errors'] = ['' for i in df_errors['Activation Mark']]
    df_errors = df_errors.loc[:,['Seller Part #','Restricted Msg','Errors']]

    # create an excel writer object
    with pd.ExcelWriter("C:\\Users\\ccrin\\Desktop\\NEB Catalog Report.xlsx") as writer:
    
        # use to_excel function and specify the sheet_name and index
        # to store the dataframe in specified sheet
        df.to_excel(writer, sheet_name='Item List', index=False)
        df_errors.to_excel(writer, sheet_name='Errors', index=False)
    
