# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import FinanceDataReader as fdr
import pandas as pd
from datetime import datetime

class excel:
    def kospi_stock_price(self):
    
        data = pd.read_excel('d:\\kospi_list.xlsx')

        code_list = data['종목코드'].tolist()
        code_list = [str(item).zfill(6) for item in code_list]
        name_list = data['종목명'].tolist()

        # 코스피 상장종목 전체
        stock_dic = dict(list(zip(code_list,name_list)))

        for code in stock_dic.keys():
            df  = fdr.DataReader(code,'2019-01-01')
            print(code,stock_dic[code])
            df['Code'],df['Name'] = code,stock_dic[code]
            df = df[['Code','Name','Open','High','Low','Volume','Close']]
    
            #df.to_excel('d:\\data_set\\kospi\\'+ stock_dic[code] +'.xlsx',engine = 'xlsxwriter')
            print(df)
            
    

    def kosdaq_stock_price(self, start_date ,end_date):
        self.start_date = start_date
        self.end_date = end_date
        data = pd.read_excel('d:\\kosdaq_list.xlsx')

        code_list = data['종목코드'].tolist()
        code_list = [str(item).zfill(6) for item in code_list]
        name_list = data['종목명'].tolist()

        # 코스피 상장종목 전체
        stock_dic = dict(list(zip(code_list,name_list)))

        for code in stock_dic.keys():
            df  = fdr.DataReader(code,start_date,end_date)
            print(code,stock_dic[code])
            df['Code'],df['Name'] = code,stock_dic[code]
            df = df[['Code','Name','Open','High','Low','Volume','Close']]    
            #df.to_excel('d:\\data_set\\kosdaq\\'+ stock_dic[code] +'.xlsx',engine = 'xlsxwriter')
            print(df)

        


