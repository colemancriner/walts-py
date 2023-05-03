import pandas as pd
import glob


# Amazon Main listing counts
def amazon_main():
    file_pattern = 'C:\\Users\\ccrin\\Desktop\\working_files\\Amazon Main All+Listings+Report+*.txt'
    file_path = glob.glob(file_pattern)[0]

    df = pd.read_csv(file_path, delimiter='\t')
    
    # replace NaN values in quantity with -1 for FBA SKUs
    df['quantity'] = df['quantity'].fillna(-1)

    #==========================================================================
    
    # filter the rows for SFP Bundles
    sfp_bndl_condition = (df['status'] == 'Active') & \
                (df['item-condition'] == 11) & \
                (df['quantity'] > 0) & \
                (df['seller-sku'].str.startswith('BNDL_')) & \
                (df['seller-sku'].str.endswith('-SFP'))
    
    sfp_bndl_filtered_df = df[sfp_bndl_condition]
    
    # get the total number of rows that match the criteria
    sfp_bndl_num_rows = len(sfp_bndl_filtered_df)
    
    #==========================================================================
    
    # filter the rows for SFP Standalone
    sfp_standalone_condition = (df['status'] == 'Active') & \
                (df['item-condition'] == 11) & \
                (df['quantity'] > 0) & \
                (~df['seller-sku'].str.startswith('BNDL_')) & \
                (df['seller-sku'].str.endswith('-SFP'))
    
    sfp_standalone_filtered_df = df[sfp_standalone_condition]
    
    # get the total number of rows that match the criteria
    sfp_standalone_num_rows = len(sfp_standalone_filtered_df)
    
    #==========================================================================
    
    # filter the rows for LOCAL Bundles
    local_bndl_condition = (df['status'] == 'Active') & \
                (df['item-condition'] == 11) & \
                (df['quantity'] > 0) & \
                (df['seller-sku'].str.startswith('BNDL_')) & \
                (df['seller-sku'].str.endswith('-LOCAL'))
    
    local_bndl_filtered_df = df[local_bndl_condition]
    
    # get the total number of rows that match the criteria
    local_bndl_num_rows = len(local_bndl_filtered_df)
    
    #==========================================================================
    
    # filter the rows for LOCAL Standalone
    local_standalone_condition = (df['status'] == 'Active') & \
                (df['item-condition'] == 11) & \
                (df['quantity'] > 0) & \
                (~df['seller-sku'].str.startswith('BNDL_')) & \
                (df['seller-sku'].str.endswith('-LOCAL'))
    
    local_standalone_filtered_df = df[local_standalone_condition]
    
    # get the total number of rows that match the criteria
    local_standalone_num_rows = len(local_standalone_filtered_df)
    
    #==========================================================================
    
    # filter the rows for BOPIS
    bopis_condition = (df['status'] == 'Active') & \
                (df['item-condition'] == 11) & \
                (df['quantity'] > 0) & \
                (df['seller-sku'].str.endswith('-BOPIS'))
    
    bopis_filtered_df = df[bopis_condition]
    
    # get the total number of rows that match the criteria
    bopis_num_rows = len(bopis_filtered_df)
    
    #==========================================================================
    
    # filter the rows for FBA Bundles
    fba_bndl_condition = (df['status'] == 'Active') & \
                (df['item-condition'] == 11) & \
                (df['quantity'] == -1) & \
                (df['seller-sku'].str.startswith('BNDL_'))
    
    fba_bndl_filtered_df = df[fba_bndl_condition]
    
    # get the total number of rows that match the criteria
    fba_bndl_num_rows = len(fba_bndl_filtered_df)
    
    #==========================================================================
    
    # filter the rows for FBA Standalone
    fba_standalone_condition = (df['status'] == 'Active') & \
                (df['item-condition'] == 11) & \
                (df['quantity'] == -1) & \
                (~df['seller-sku'].str.startswith('BNDL_'))
    
    fba_standalone_filtered_df = df[fba_standalone_condition]
    
    # get the total number of rows that match the criteria
    fba_standalone_num_rows = len(fba_standalone_filtered_df)
    
    # Prepare df of counts to return
    counts_df = pd.DataFrame({
        'SFP - Standalone': [sfp_standalone_num_rows],
        'SFP - Bundles': [sfp_bndl_num_rows],
        'BOPIS': [bopis_num_rows],
        'FBA - Standalone': [fba_standalone_num_rows],
        'FBA - Bundles': [fba_bndl_num_rows],
        'LOCAL - Standalone': [local_standalone_num_rows],
        'LOCAL - Bundles': [local_bndl_num_rows]})
    return counts_df
#==============================================================================
#==============================================================================
#==============================================================================
# Amazon Home listing counts
def amazon_home():
    file_pattern = 'C:\\Users\\ccrin\\Desktop\\working_files\\Amazon Home All+Listings+Report+*.txt'
    file_path = glob.glob(file_pattern)[0]

    df = pd.read_csv(file_path, delimiter='\t')
    
    # replace NaN values in quantity with -1 for FBA SKUs
    df['quantity'] = df['quantity'].fillna(-1)

    #==========================================================================
    
    # filter the rows for SFP Bundles
    home_bndl_condition = (df['status'] == 'Active') & \
                (df['item-condition'] == 11) & \
                (df['quantity'] > 0) & \
                (df['seller-sku'].str.startswith('BNDL_'))
    
    home_bndl_filtered_df = df[home_bndl_condition]
    
    # get the total number of rows that match the criteria
    home_bndl_num_rows = len(home_bndl_filtered_df)
    
    #==========================================================================
    
    # filter the rows for SFP Standalone
    home_standalone_condition = (df['status'] == 'Active') & \
                (df['item-condition'] == 11) & \
                (df['quantity'] > 0) & \
                (~df['seller-sku'].str.startswith('BNDL_'))
    
    home_standalone_filtered_df = df[home_standalone_condition]
    
    # get the total number of rows that match the criteria
    home_standalone_num_rows = len(home_standalone_filtered_df)
    
    #==========================================================================
    
    # Prepare df of counts to return
    counts_df = pd.DataFrame({
        'HOME - Standalone': [home_standalone_num_rows],
        'HOME - Bundles': [home_bndl_num_rows]})
    return counts_df
#==============================================================================
#==============================================================================
#==============================================================================
# Walmart listing counts
def walmart():
    
    # Read in Item Report
    file_pattern = 'C:\\Users\\ccrin\\Desktop\\working_files\\WM Item Report*.csv'
    file_path = glob.glob(file_pattern)[0]
    df_item = pd.read_csv(file_path)
    
    # Read in Inventory Report
    file_pattern = 'C:\\Users\\ccrin\\Desktop\\working_files\\WM Inventory Report*.csv'
    file_path = glob.glob(file_pattern)[0]
    df_inventory = pd.read_csv(file_path)
    
    #======================================================================
    
    # Clean DataFrames and join
    df_inventory = df_inventory.groupby('SKU')['AvailToSell Quantity'].agg([sum,max,min])
    df_inventory = df_inventory.rename(columns={'sum': 'Quantity'})
    
    df = df_item.join(df_inventory, on='SKU', how='inner')
    df = df[(df['Quantity']>=1) &
            (df['Publish Status']=='PUBLISHED') &
            (df['Lifecycle Status']=='ACTIVE')]
    df_bundles = len(df[df['SKU'].str.contains('BNDL_')])
    df_standalone = len(df[(~df['SKU'].str.contains('BNDL_'))])
    return pd.DataFrame({
        'Walmart - Bundles': [df_bundles],
        'Walmart - Standalone': [df_standalone]})
#==============================================================================
#==============================================================================
#==============================================================================
# MAIN FUNCTION
def main():

    # Define variables
    amz_main_counts = None
    amz_home_counts = None
    wm_counts = None

    # Amazon Main Listing Counts
    try:
        amz_main_counts = amazon_main()
    except Exception as err:
        print(str(err))

    # Amazon Home Listing Counts
    try:
        amz_home_counts = amazon_home()
    except Exception as err:
        print(str(err))

    # Walmart Listing Counts
    try:
        wm_counts = walmart()
    except Exception as err:
        print(str(err))
        
    # Combine DataFrames
    df = pd.DataFrame({})
    if len(amz_main_counts)>0:
        df = pd.concat([df,amz_main_counts], axis=1)
    if len(amz_home_counts)>0:
        df = pd.concat([df,amz_home_counts], axis=1)
    if len(amz_main_counts)>0:
        df = pd.concat([df,wm_counts], axis=1)
    df.to_csv('C:\\Users\\ccrin\\Desktop\\MPListingCounts.csv', index=None)

    print('MAIN DRIVER')






#==========================================================================================
#==========================================================================================
#==========================================================================================


main()

