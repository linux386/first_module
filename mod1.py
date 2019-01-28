# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import FinanceDataReader as fdr
import pandas as pd
from bs4 import BeautifulSoup
import datetime as date
from urllib.request import urlopen

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

        
    def get_money_trend():
        folder_adress = 'd:\\'
        file_name = 'pre_mondy_trend.xlsx'
        
        url = 'http://finance.naver.com/sise/sise_deposit.nhn?&page='
        source = urlopen(url).read()
        source = BeautifulSoup(source,'lxml')
        last = source.find('td',class_='pgRR').find('a')['href']
        last = last.split('&')[1]
        last = last.split('=')[1]
        last = int(last)
    
        Data = pd.DataFrame(columns = ['고객예탁금', '신용잔고','주식형 펀드','혼합형 펀드','채권형 펀드'])

        # 날짜를 받을 리스트
        date_list = []
        
        # 값을 받을 사전
        dictionary = {'고객예탁금': [],'신용잔고': [],'주식형 펀드': [],'혼합형 펀드': [],'채권형 펀드': []}

        # dictionary key 인덱싱을 위한 리스트
        name_list = ['고객예탁금','신용잔고','주식형 펀드','혼합형 펀드','채권형 펀드']

        # count mask
        mask = [0,1,3,5,7,9]
    
        for i in range(1,last+5):
            source = urlopen(url+ str(i)).read()
            source = BeautifulSoup(source,'lxml')

            tbody = source.find('div',{'id':'wrap'}).find('div',{'class':'box_type_m'})
            trs = tbody.find_all('tr')

            for tr in trs:
                tds = tr.find_all('td')
                count = 0
                for td in tds:
                    # 변화량 제외하고 잔고량만 가져오기
                    if not td.text.strip() == 0:
                        if len(td.text.strip()) >= 4:
            
                            if count == 0:
                                date_ = td.text.strip().replace('.','-')
                        
                                if not date_ in date_list:
                                    date_list.append(date_)
                            
                                else:
                                    print(str(i-1) + '번째 페이지에서 크롤링 종료')
                                
                                    data = pd.DataFrame(dictionary,index = date_list)
                                    data.to_csv(folder_adress + '/money_trend.csv')
    
                                    return data

                            elif count in mask:
                                temp = int((count-1)/2)
                                dictionary[name_list[temp]].append(td.text.strip())
        
                        count += 1
            
                # 누락된 값을 발견하면 (펀드 자료에 누락된 값이 존재함)
                if len(dictionary['고객예탁금']) != len(dictionary['주식형 펀드']):
                    print(str(i)+ '번째 페이지에서 누락된 값 발생')
                    print('누락된 데이터를 제거합니다')
                    
                    date_list.pop(-1)
                    dictionary['고객예탁금'].pop(-1)
                    dictionary['신용잔고'].pop(-1)
                
            print(str(i) + '번째 페이지 크롤링 완료')
