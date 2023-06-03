import pandas as pd
import glob


def walmart_audit():

    # Read in Active Listings Report
    file_pattern = 'C:\\Users\\ccrin\\Desktop\\working_files\\WM Item Report*.csv'
    file_path = glob.glob(file_pattern)[0]
    df = pd.read_csv(file_path)

    df = df[(df['Condition']=='NEW') &
            (df['Available quantity']>0)]
    df_counts = len(df)
    return pd.DataFrame({'eBay': [df_counts]})








