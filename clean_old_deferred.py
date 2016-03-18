# -*- coding: utf-8 -*-
"""


clean up old deferred



"""


#%%

MERGER = 'Account ID'
NO_MATCH = 'fucked up if u see this'
NO_MATCH_FILL = 'fucked up if u see this'

        #%% 1 :: modules

import pandas as pd
from Lightspeed.conversion import convert_date_from_annuals
from lightspeed.structure  import keep_right_skus_and_classify_the_inv, \
                                  merge_annual_inv_and_mapper, \
                                  create_mapper_to_retailID, \
                                  slice_df_by_last_month_long
                                  
from Lightspeed.validation import read_csv_w_col_validation_only_firsts

from config import *

#%% fct starts here

def clean_old_deferred():

            #%% 1 :: data
    
    df_old_def_raw = read_csv_w_col_validation_only_firsts(
                        PATH_OLD_DEFERRED,
                        COLUMNS_OLD_DEFERRED)
    
            #%% 2 :: 2 clean-up
    
    # 2.1 create mapper
    df_mapper = create_mapper_to_retailID(MERGER)
    
    # 2.2 slice after last month
    df_old_def = slice_df_by_last_month_long(df_old_def_raw)
    
    # 2.3 keep cloud year and cloud month related SKUS and classify the invoices accordingly
    df_old_def = keep_right_skus_and_classify_the_inv(df_old_def)
    
    # 2.4 add type column
    df_old_def.type = 'annual: old deferred'
    
    # 2.5 add invoice month columns
    df_old_def.insert(2,INV_MONTH,'2015-04')
    
    # 2.6 drop uncessary col
    df_old_def = df_old_def.drop('Invoice Line Item Name',1)\
                           .drop(SKUS,1)
                               
    # 2.7 rename the columns properly                 
    df_old_def = df_old_def.rename(columns = lambda x: convert_date_from_annuals(x))
    
    df_old_def_final = merge_annual_inv_and_mapper(df_old_def,df_mapper,MERGER,NO_MATCH,NO_MATCH_FILL)
         
    
    #%% save
    
    df_old_def_final.to_csv(PATH_OLD_DEFERRED_C, index = False)
    



