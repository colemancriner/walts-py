import pandas as pd
import glob

def amzSonyList():

    file_pattern = 'C:\\Users\\ccrin\\Desktop\\working_files\\Amazon Main All+Listings+Report+*.txt'
    file_path = glob.glob(file_pattern)[0]

    df = pd.read_csv(file_path, delimiter='\t')
    
    df = df[df['status']=='Active']

    df = df[(df['item-name'].str.contains('Sony')) |
            (df['item-name'].str.contains('sony')) |
            (df['item-name'].str.contains('SONY'))]
    
    df = df.drop_duplicates(subset=['asin1'])
    return df

# class to remove ending of skus if applicable
def remove_ending(sku):
    i = 0
    while i < 3:
        if sku.endswith('-SFP'):
            new_sku = sku[:(len(sku)-4)]
        elif sku.endswith('-BOPIS'):
            new_sku = sku[:(len(sku)-6)]
        elif sku.endswith('-FBA'):
            new_sku = sku[:(len(sku)-4)]
        elif sku.endswith('-FBW'):
            new_sku = sku[:(len(sku)-4)]
        elif sku.endswith('-LOCAL'):
            new_sku = sku[:(len(sku)-6)]
        elif sku.endswith('-NEW-OTHER'):
            new_sku = sku[:(len(sku)-10)]
        elif sku.endswith('-USED-LIKE-NEW'):
            new_sku = sku[:(len(sku)-14)]
        else:
            new_sku = sku
        sku = new_sku
        i = i+1
    return new_sku


def report():
    df = amzSonyList()
    df['seller-sku'] = df['seller-sku'].map(lambda sku: remove_ending(sku))
    df = df.loc[:,['seller-sku','asin1','item-name','listing-id']]
    
    # Save active amazon sony SKUs dataframe df to csv file on desktop for editing, emailing, & logging
    df.to_csv('C:\\Users\\ccrin\\Desktop\\ActiveAmzSonySkus.csv', index=None)
    
    # Return dataframe for future app implementation
    return df

report()

