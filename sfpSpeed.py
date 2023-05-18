import pandas as pd
import glob
import numpy as np

def report():
    # Read in Speed Report Download
    file_pattern = 'C:\\Users\\ccrin\\Desktop\\working_files\\SFP Speed Report*.tsv'
    file_path = glob.glob(file_pattern)[0]
    df = pd.read_csv(file_path, sep='\t')
    
    twoday_rate = []
    
    for index, row in df.iterrows():
        
        if row['Total standard-size detail page views']==0:
            rate = row['>2 day oversize detail page views'] / row['Total oversize detail page views']
            twoday_rate.append(rate)
        elif row['Total oversize detail page views']==0:
            rate = row['>2 day standard-size detail page views'] / row['Total standard-size detail page views']
            twoday_rate.append(rate)
        else:
            twoday_rate.append(0)
    
    try:
        assert len(twoday_rate) == len(df), 'twoday_rate list length ' + str(len(twoday_rate)) + ' is not the same length as df ' + str(len(df))
        df['>2day rate'] = twoday_rate
    except Exception as err:
        print(err)
    

    df_standard = df[(df['Total standard-size detail page views'] > 12) &
                     (df['>2day rate'] > 0.3)]
    df_standard = df_standard.sort_values(by='>2day rate', ascending=False)
    df_standard = df_standard.head()
    df_standard = df_standard.loc[:,['ASIN','Total standard-size detail page views','<= 1day standard-size detail page views','<= 2day standard-size detail page views','>2 day standard-size detail page views','>2day rate']]


    df_oversize = df[(df['Total oversize detail page views'] > 50) &
                     (df['>2day rate'] > 0.3)]
    df_oversize = df_oversize.sort_values(by='>2day rate', ascending=False)
    df_oversize = df_oversize.head()
    df_oversize = df_oversize.loc[:,['ASIN','Total oversize detail page views','<= 1day oversize detail page views','<= 2day oversize detail page views','>2 day oversize detail page views','>2day rate']]


    # create an excel writer object
    with pd.ExcelWriter("C:\\Users\\ccrin\\Desktop\\SFP Speed Report.xlsx") as writer:
    
        # use to_excel function and specify the sheet_name and index
        # to store the dataframe in specified sheet
        df.to_excel(writer, sheet_name='SFP Speed Report', index=False)
        df_standard.to_excel(writer, sheet_name='Standard', index=False)
        df_oversize.to_excel(writer, sheet_name='Oversize', index=False)

        










